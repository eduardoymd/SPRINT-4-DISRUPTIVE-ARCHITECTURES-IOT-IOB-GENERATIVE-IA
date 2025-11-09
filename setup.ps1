python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
Write-Host "Please install PyTorch appropriate for your system before continuing: https://pytorch.org/get-started/locally/"
pip install -r requirements.txt
streamlit run app.py
