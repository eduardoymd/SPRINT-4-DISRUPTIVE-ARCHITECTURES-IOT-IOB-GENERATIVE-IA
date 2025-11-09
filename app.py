import tempfile
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import cv2
import yaml
import sqlite3
import sqlalchemy as sa

try:
    import oracledb
except Exception:
    oracledb = None


def pick_device_prefer_cuda():
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass
    return "cpu"


st.set_page_config(page_title="Motorcycle Detection Dashboard", layout="wide", page_icon="🏍️")

@st.cache_data
def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
CFG = load_config()

st.title("Motorcycle Detection Dashboard (dashboardPro)")
st.sidebar.header("Controls")

conf = st.sidebar.slider("Confidence", 0.1, 0.95, float(CFG.get("conf", 0.5)), 0.05)
iou = st.sidebar.slider("IoU", 0.1, 0.9, float(CFG.get("iou", 0.45)), 0.05)
imgsz = st.sidebar.slider("Image size", 320, 1280, int(CFG.get("imgsz", 640)), 32)
process_mode = st.sidebar.radio("Mode", ["Upload video", "Batch folder"])
video_file = st.sidebar.file_uploader("Upload video", type=["mp4", "avi", "mov", "mkv"]) if process_mode == "Upload video" else None
run_btn = st.sidebar.button("Run Detection")

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None

MODEL_PATH = CFG.get("model_path", "models/best.pt")


def connect_oracle_sqlalchemy():
    """Return SQLAlchemy engine if Oracle is configured and reachable."""
    ORACLE_CFG = CFG.get("oracle", {})
    if not ORACLE_CFG.get("enabled", False):
        return None
    try:
        oracle_url = f"oracle+oracledb://{ORACLE_CFG['user']}:{ORACLE_CFG['password']}@{ORACLE_CFG['dsn']}/{ORACLE_CFG['sid']}"
        engine = sa.create_engine(oracle_url)
        with engine.connect() as conn:
            conn.execute(sa.text("SELECT 1 FROM DUAL"))
        return engine
    except Exception as e:
        st.warning(f"Oracle connection failed; fallback to SQLite. Error: {e}")
        return None


def ensure_sqlite(db_path):
    p = Path(db_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p))
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS TB_MOTOS (
            ID_MOTO INTEGER PRIMARY KEY AUTOINCREMENT,
            OBJ_ID INTEGER,
            FRAME INTEGER,
            CONF REAL,
            X1 REAL, Y1 REAL, X2 REAL, Y2 REAL,
            DATA_PROCESSAMENTO TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    return conn


def export_excel(df, path):
    try:
        with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="detections")
            workbook = writer.book
            worksheet = writer.sheets["detections"]
            header_format = workbook.add_format(
                {'bold': True, 'text_wrap': True, 'fg_color': '#34D231', 'font_color': '#040405'}
            )
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            for i, col in enumerate(df.columns):
                col_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, col_width)
    except Exception as e:
        st.warning("Excel export failed: " + str(e))



def fake_process_video(in_path):
    import random
    cap = cv2.VideoCapture(str(in_path))
    frames = int(cap.get(cv2.CROP_PROP_FRAME_COUNT) or 0)
    results = []
    for f in range(min(frames, 200)):
        n = random.randint(0, 2)
        for i in range(n):
            results.append({"frame": f, "obj_id": i, "conf": round(random.uniform(0.5, 0.95), 2),
                            "x1": 100, "y1": 100, "x2": 200, "y2": 200})
    cap.release()
    return pd.DataFrame(results)


def process_video_file(path):
    if YOLO is None or not Path(MODEL_PATH).exists():
        st.info("YOLO not installed or model missing. Running demo detections.")
        df = fake_process_video(path)
        return df, None

    device = pick_device_prefer_cuda()
    model = YOLO(MODEL_PATH)
    cap = cv2.VideoCapture(str(path))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # stable codec
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out_path = Path("outputs") / (Path(path).stem + "_annotated.mp4")
    vw = cv2.VideoWriter(str(out_path), fourcc, fps, (W, H))
    all_rows = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model.predict(source=frame[..., ::-1], conf=conf, iou=iou, imgsz=imgsz,
                                device=device, verbose=False)
        res = results[0]
        if res.boxes is None or res.boxes.data is None:
            vw.write(frame)
            frame_idx += 1
            continue

        xyxy = res.boxes.xyxy.cpu().numpy()
        confs = res.boxes.conf.cpu().numpy()
        for i in range(len(confs)):
            x1, y1, x2, y2 = map(int, xyxy[i])
            all_rows.append({
                "frame": frame_idx,
                "obj_id": i,
                "conf": float(confs[i]),
                "x1": x1, "y1": y1, "x2": x2, "y2": y2
            })
            cv2.rectangle(frame, (x1, y1), (x2, y2), (52, 210, 49), 2)
        vw.write(frame)
        frame_idx += 1

    cap.release()
    vw.release()
    return pd.DataFrame(all_rows), out_path



if process_mode == "Upload video" and video_file is not None and run_btn:
    tdir = tempfile.mkdtemp()
    in_path = Path(tdir) / video_file.name
    with open(in_path, "wb") as f:
        f.write(video_file.read())

    df, annotated = process_video_file(in_path)

    st.markdown(
        f"<div style='background-color:#005A23;padding:15px;border-radius:12px;margin-bottom:15px;text-align:center;'>"
        f"<span style='font-size:22px;color:#34D231;font-weight:bold;'>🏍️ Total Motorcycles Detected: {len(df)}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

    if annotated and Path(annotated).exists():
        try:
            st.video(str(annotated))
        except Exception:
            st.info(f"Video saved at: `{annotated}` (open manually)")


    csv_path = Path("outputs") / (in_path.stem + "_detections.csv")
    df.to_csv(csv_path, index=False)
    xlsx_path = Path("outputs") / (in_path.stem + "_detections.xlsx")
    export_excel(df, xlsx_path)

    st.download_button("Download CSV", data=csv_path.read_bytes(),
                       file_name=csv_path.name, mime="text/csv")
    st.download_button("Download Excel", data=xlsx_path.read_bytes(),
                       file_name=xlsx_path.name,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


#Salva no Banco de Dados - (Oracle SQL)
    engine = connect_oracle_sqlalchemy()
    table_name = CFG["oracle"]["table"].upper()
    if engine is not None:
        try:
            df.to_sql(table_name, engine, if_exists="append", index=False)
            st.success("Results saved to Oracle — check the History tab for full details.")
        except Exception as e:
            st.warning("Failed saving to Oracle: " + str(e))
    else:
        conn_sqlite = ensure_sqlite(CFG.get("sqlite_path", "outputs/results.db"))
        if not df.empty:
            df.to_sql("TB_MOTOS", conn_sqlite, if_exists="append", index=False)
        st.success("Results saved to SQLite — check the History tab for full details.")


st.header("Detection History")
engine = connect_oracle_sqlalchemy()
history_df = None

if engine is not None:
    try:
        history_df = pd.read_sql(
            f"SELECT * FROM {CFG['oracle']['table'].upper()} ORDER BY DATA_PROCESSAMENTO DESC", engine)
    except Exception as e:
        st.warning("Oracle read failed: " + str(e))
        history_df = None

if history_df is None:
    conn_sqlite = ensure_sqlite(CFG.get("sqlite_path", "outputs/results.db"))
    try:
        history_df = pd.read_sql("SELECT * FROM TB_MOTOS ORDER BY DATA_PROCESSAMENTO DESC", conn_sqlite)
    except Exception:
        history_df = pd.DataFrame()

if not history_df.empty:
    st.metric("Total records", len(history_df))
    st.dataframe(history_df.head(200), width='stretch')
    try:
        df_plot = history_df.copy()
        df_plot["DATA_PROCESSAMENTO"] = pd.to_datetime(df_plot["DATA_PROCESSAMENTO"])
        daily = df_plot.groupby(df_plot["DATA_PROCESSAMENTO"].dt.date).size().reset_index(name="count")
        fig = px.line(daily, x="DATA_PROCESSAMENTO", y="count", title="Detections over time", markers=True)
        st.plotly_chart(fig, width='stretch')
    except Exception:
        pass
else:
    st.info("No history records found.")
