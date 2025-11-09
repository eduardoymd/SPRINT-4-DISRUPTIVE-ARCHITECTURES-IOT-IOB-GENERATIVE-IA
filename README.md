
# dashboardPro — Motorcycle Detection Dashboard (YOLOv8 + Streamlit)

Minimalist Mottu-inspired dark dashboard to run YOLOv8 motorcycle detection on videos,
track motorcycles, count entries/exits and persist results to Oracle (with SQLite fallback).

![logo](assets/logo_mottu.png)

## Features

- Video upload or batch processing from a folder
- YOLOv8 inference (use your pretrained `models/best.pt`)
- Tracking (object IDs), counting line and optional ROI
- Export detection results to CSV, Excel (.xlsx) and persist to Oracle DB
- Detection history page reading from Oracle (or SQLite fallback)
- Dark Mottu-inspired theme (colors: #040405, #34D231, #005A23)
- Dockerfile and setup scripts for quick start

## Quick start

1. Put your trained model at: `models/best.pt` or update `config.yaml`.
2. (Optional) Initialize Oracle schema: run `database/init_oracle.sql` in your Oracle environment.
3. Create virtualenv, install deps and run:

```bash
# Linux / macOS
bash setup.sh

# Windows PowerShell
.\setup.ps1
```

## Config

Edit `config.yaml` to tune model path, oracle credentials and folders. Note: password is masked in the distributed config; replace the `*****MASKED*****` value with your real password.

## Files of interest

- `app.py` — main Streamlit application (English UI)
- `config.yaml` — configuration file (model path, DB, colors)
- `database/init_oracle.sql` — create table and insert a sample record
- `assets/` — logo and preview images (minimalist placeholders)
- `models/` — place your `best.pt` here
- `outputs/` — generated CSV/Excel/annotated videos
- `setup.sh` / `setup.ps1` — quick setup scripts for Linux/Windows
- `Dockerfile` — to build a container image (ensure PyTorch appropriate install)

## Notes

- For full GPU performance, install PyTorch matching your CUDA version manually before installing requirements.
- The app gracefully falls back to SQLite if Oracle connection fails.
- The included demo mode runs fake detections if YOLO or model file is missing — useful for testing the UI without GPU/training artifacts.
