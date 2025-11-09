
#!/bin/bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
echo "Please install PyTorch appropriate for your system before continuing: https://pytorch.org/get-started/locally/"
pip install -r requirements.txt
streamlit run app.py
