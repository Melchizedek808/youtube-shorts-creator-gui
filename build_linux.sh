
#!/bin/bash
# Build script for Linux (for testing on Linux before building on Windows)

echo "================================================"
echo "YouTube Shorts Creator - Build Script"
echo "================================================"
echo ""

echo "[1/4] Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python3 is not installed"
    exit 1
fi

echo ""
echo "[2/4] Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[3/4] Building with PyInstaller..."
echo "This may take 5-10 minutes..."
pyinstaller build.spec --clean
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to build"
    exit 1
fi

echo ""
echo "[4/4] Cleaning up..."
rm -rf build
rm -f *.log

echo ""
echo "================================================"
echo "SUCCESS! Application built in 'dist' folder"
echo "================================================"
echo ""
echo "Location: dist/YouTube Shorts Creator/"
echo ""
