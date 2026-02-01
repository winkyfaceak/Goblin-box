# PowerShell installer for Windows
Param()
Set-StrictMode -Version Latest

Write-Output "Creating venv and installing requirements..."

$python = (Get-Command python -ErrorAction SilentlyContinue).Path
if (-not $python) {
  Write-Error "Python not found. Install Python 3.10+ and re-run."
  exit 1
}

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip setuptools wheel
python -m pip install certifi

$env:SSL_CERT_FILE = python - <<'PY'
import certifi, sys
print(certifi.where())
PY

try {
  python -m pip install -r requirements.txt
  Write-Output "Requirements installed."
} catch {
  Write-Error "pip install failed. Consider installing dependencies via conda/mamba or follow llvmlite/torch platform instructions."
  exit 1
}

Write-Output "Installation complete. Activate with: .\.venv\Scripts\Activate.ps1"

# File: start.sh
#!/usr/bin/env bash
# small runner that ensures certifi's CA bundle is used
set -euo pipefail
# Activate venv if present
if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
export SSL_CERT_FILE="$(python -c 'import certifi; print(certifi.where())')"
python main.py