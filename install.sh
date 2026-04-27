#!/bin/bash

echo "Installing GitShield..."

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e .

echo ""
echo "GitShield installed successfully!"
echo "You can now run:"
echo "  gitshield"
echo "or:"
echo "  GitShield"