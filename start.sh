#! /usr/bin/bash

# =======================================
# Helper fn to print to console
# =======================================
printInfo() {
  echo ""
  echo "========================================="
  echo "[INFO] $1"
  echo "========================================="
}

# =======================================
# Grab the latest code from the repo
# =======================================
printInfo "Pulling from Git repo"
git checkout main;
git pull;


# =======================================
# Install requirements
# =======================================
printInfo "Installing requirements"
python3 -m pip install -r requirements.txt


# =======================================
# Run the basestation script
# =======================================
printInfo "Starting basestation"
python3 ./basestation.py