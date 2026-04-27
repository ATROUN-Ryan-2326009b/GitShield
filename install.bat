@echo off
echo ==================================
echo Installing GitShield (Windows)
echo ==================================

REM Vérifier Python
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python not found.
    echo Install Python from https://www.python.org/downloads/
    pause
    exit /b
)

REM Installer pipx si absent
python -m pip show pipx >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Installing pipx...
    python -m pip install --user pipx
)

REM Ajouter pipx au PATH via PowerShell
echo Adding pipx to PATH...

powershell -Command ^
"$path = [Environment]::GetEnvironmentVariable('Path','User'); ^
$target = '$env:USERPROFILE\.local\bin'; ^
if ($path -notlike '*'+$target+'*') { ^
    [Environment]::SetEnvironmentVariable('Path', $path + ';' + $target, 'User') ^
}"

REM Installer GitShield
echo Installing GitShield...
python -m pipx install . --force

echo.
echo ==================================
echo GitShield installed successfully
echo ==================================
echo.
echo Restart your terminal or run:
echo   refreshenv (if using Chocolatey)
echo.
echo Then run:
echo   gitshield

pause