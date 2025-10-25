
@echo off
REM Build script for Windows executable
REM This creates a standalone Windows .exe file

echo ================================================
echo YouTube Shorts Creator - Windows Build Script
echo ================================================
echo.

echo [1/4] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [3/4] Building executable with PyInstaller...
echo This may take 5-10 minutes...
pyinstaller build.spec --clean
if %errorlevel% neq 0 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

echo.
echo [4/4] Cleaning up...
rmdir /s /q build
del /q *.log

echo.
echo ================================================
echo SUCCESS! Executable created in 'dist' folder
echo ================================================
echo.
echo Location: dist\YouTube Shorts Creator.exe
echo.
echo You can now distribute the entire 'dist' folder
echo to other Windows users. They can run the .exe
echo without installing Python or any dependencies!
echo.
pause
