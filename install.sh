#!/usr/bin/env bash
set -euo pipefail
printf "Installer: creating venv and installing requirements\n"

PY=$(command -v python3 || command -v python)
if [ -z "$PY" ]; then
  echo "No python found. Install Python 3.10+ and re-run."
  exit 1
fi

# create venv
$PY -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install certifi

# export cert bundle for the current shell/install commands
# shellcheck disable=SC2155
export SSL_CERT_FILE="$(python -c 'import certifi; print(certifi.where())')"
echo "Using SSL_CERT_FILE=$SSL_CERT_FILE"

# try to install requirements; capture failure to provide hints
if python -m pip install -r requirements.txt; then
  echo "Python requirements installed."
else
  echo "pip install failed. Common causes:"
  echo " - llvmlite/numba failed to build (missing LLVM or wrong LLVM version)."
  echo " - torch requires platform-specific wheels (install from https://pytorch.org)."
  echo ""
  echo "Suggested next steps (pick one):"
  echo " 1) Install system LLVM (macOS Intel example):"
  echo "     brew install llvm@20"
  echo "     export PATH=\"\$(brew --prefix llvm@20)/bin:\$PATH\""
  echo "     export LLVM_CONFIG=\"\$(brew --prefix llvm@20)/bin/llvm-config\""
  echo "     python -m pip install -r requirements.txt"
  echo " 2) Use conda/mamba for prebuilt binaries:"
  echo "     mamba create -n dictation python=3.12 -y"
  echo "     mamba activate dictation"
  echo "     mamba install -c conda-forge llvmlite numba pytorch -y"
  echo "     python -m pip install openai-whisper sounddevice certifi"
  exit 1
fi

echo "Installation complete. Activate the venv with: source .venv/bin/activate"
