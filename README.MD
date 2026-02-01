# Quick install (Unix)
1. Clone the repo.
2. Run `./install.sh`
3. Activate: `source .venv/bin/activate`
4. Run: `./start.sh`

# Windows (PowerShell)
1. Clone the repo.
2. Run `.\install.ps1` in an elevated PowerShell if needed.
3. Activate: `.\.venv\Scripts\Activate.ps1`
4. Run: `python main.py`

# Notes
- If `pip install` fails on `llvmlite`/`numba`, use conda/mamba to get prebuilt binaries.
- For `torch`, follow the official selector at https://pytorch.org/get-started/locally/ to get the correct wheel for the target OS/GPU.
- The `start.sh` ensures `SSL_CERT_FILE` uses `certifi` so model downloads succeed.