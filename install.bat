@echo off
echo Installing GitShield...

python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .

echo.
echo GitShield installed successfully!
echo You can now run:
echo   gitshield
echo or:
echo   GitShield

pause