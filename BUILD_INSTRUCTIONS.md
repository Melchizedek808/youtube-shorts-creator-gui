# Build Instructions for YouTube Shorts Creator Windows

## Overview

This document provides step-by-step instructions for building the YouTube Shorts Creator Windows executable from source code.

---

## Prerequisites

### Required Software

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - ⚠️ During installation, check "Add Python to PATH"

2. **Git** (optional, for cloning)
   - Download from: https://git-scm.com/downloads

3. **Visual C++ Redistributable** (Windows)
   - Usually already installed on Windows 10/11
   - If needed: https://aka.ms/vs/17/release/vc_redist.x64.exe

### System Requirements

- **OS**: Windows 10/11 64-bit (for building Windows executable)
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB free space
- **Internet**: Required for downloading dependencies

---

## Step-by-Step Build Process

### 1. Get the Source Code

**Option A: Download ZIP**
```
1. Download the source code ZIP
2. Extract to a folder (e.g., C:\Projects\youtube-shorts-creator-windows)
```

**Option B: Clone with Git**
```bash
git clone https://github.com/yourusername/youtube-shorts-creator-windows.git
cd youtube-shorts-creator-windows
```

### 2. Open Command Prompt

1. Press `Win + R`
2. Type `cmd` and press Enter
3. Navigate to the project folder:
   ```bash
   cd C:\Projects\youtube-shorts-creator-windows
   ```

### 3. Verify Python Installation

```bash
python --version
```

Should show: `Python 3.8.x` or higher

If not found:
- Reinstall Python with "Add to PATH" checked
- Or use `py` instead of `python`

### 4. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Your prompt should now show (venv)
```

### 5. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- moviepy (video editing)
- openai-whisper (speech-to-text)
- numpy, Pillow, imageio (video processing)
- pyinstaller (executable builder)

**Expected time**: 5-10 minutes

### 6. Test the Application (Optional but Recommended)

Before building, test that it works:

```bash
python shorts_creator_gui.py
```

The GUI should open. If it does, you're ready to build!
Close the app and continue.

### 7. Build the Executable

**Option A: Folder Build (Recommended)**

```bash
build_windows.bat
```

**Option B: Single File Build**

```bash
pyinstaller build_onefile.spec --clean
```

**Expected time**: 5-10 minutes

The script will:
1. Collect all dependencies
2. Bundle Python runtime
3. Create standalone executable
4. Package everything in `dist` folder

### 8. Find Your Executable

After successful build:

```
dist/
└── YouTube Shorts Creator/
    ├── YouTube Shorts Creator.exe  ← Your executable!
    ├── (many dependency DLLs and files)
```

### 9. Test the Executable

```bash
cd dist
"YouTube Shorts Creator.exe"
```

The application should launch without errors!

### 10. Package for Distribution (Optional)

**Create ZIP for users:**

1. Right-click `dist\YouTube Shorts Creator` folder
2. Select "Send to" → "Compressed (zipped) folder"
3. Rename to: `YouTube-Shorts-Creator-v2.0-Windows.zip`

**Or use 7-Zip:**

```bash
7z a -r YouTube-Shorts-Creator-v2.0-Windows.zip "dist\YouTube Shorts Creator"
```

---

## Troubleshooting

### Problem: "python is not recognized"

**Solution**:
1. Reinstall Python with "Add to PATH" checked
2. Or use `py` instead of `python` in all commands

### Problem: pip install fails

**Solution**:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Try again
pip install -r requirements.txt
```

### Problem: PyInstaller fails with ImportError

**Solution**:
- Add missing module to `hiddenimports` in `build.spec`
- Reinstall the module: `pip install --force-reinstall <module_name>`

### Problem: Built exe won't start

**Solution**:
- Build with console mode to see errors:
  - Edit `build.spec`: Change `console=False` to `console=True`
  - Rebuild: `pyinstaller build.spec --clean`
- Check Windows Event Viewer for crash logs

### Problem: Antivirus deletes exe

**Solution**:
- Add exception in your antivirus
- This is a false positive (common with PyInstaller)
- Consider code-signing the exe (requires certificate)

### Problem: "Module not found" when running exe

**Solution**:
- The module needs to be added to `hiddenimports` in `build.spec`
- Add the module name, rebuild

### Problem: Very large exe size (>1GB)

**Solution**:
- This is normal for first build (includes Whisper models)
- Use UPX compression (already enabled in build.spec)
- Consider folder build instead of single-file

---

## Build Optimization

### Reduce Build Time

1. **Use folder build** instead of single-file (faster)
2. **Don't clean** every time:
   ```bash
   pyinstaller build.spec  # Without --clean
   ```
3. **Exclude unused modules** in build.spec

### Reduce File Size

1. **Already optimized** with UPX compression
2. **Remove unused Whisper models** (advanced)
3. **Use folder build** (smaller than single-file)

---

## Advanced: Customizing the Build

### Change App Icon

1. Create or download an icon file: `icon.ico`
2. Place in project root
3. Edit `build.spec`: Icon line is already configured
4. Rebuild

### Change App Name

Edit `build.spec`:
```python
name='Your Custom Name'
```

### Add Hidden Imports

If you add new features with new dependencies:

Edit `build.spec`:
```python
hiddenimports = [
    # ... existing imports ...
    'your_new_module',
]
```

### Console vs Windowed Mode

**Show console** (for debugging):
```python
console=True
```

**Hide console** (for release):
```python
console=False
```

---

## Build on Different Platforms

### Building on Linux (for testing)

```bash
# Install dependencies
pip3 install -r requirements.txt

# Build
./build_linux.sh

# Run
./dist/YouTube\ Shorts\ Creator/YouTube\ Shorts\ Creator
```

**Note**: Linux builds won't run on Windows. You must build on Windows for Windows.

### Cross-Platform Builds

❌ **Not possible** with PyInstaller

- Must build on Windows for Windows
- Must build on Linux for Linux  
- Must build on macOS for macOS

Consider using:
- GitHub Actions for automated builds
- Virtual machines for cross-platform building

---

## Automated Builds (CI/CD)

### GitHub Actions Example

Create `.github/workflows/build.yml`:

```yaml
name: Build Windows Executable

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Build with PyInstaller
      run: pyinstaller build.spec --clean
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: youtube-shorts-creator-windows
        path: dist/YouTube Shorts Creator
```

---

## Distribution Checklist

Before releasing to users:

- [ ] Test on clean Windows 10 machine
- [ ] Test on clean Windows 11 machine
- [ ] Test with antivirus enabled
- [ ] Test all three caption modes
- [ ] Test with various video formats
- [ ] Create release notes
- [ ] Create GitHub release
- [ ] Upload ZIP file
- [ ] Update version numbers
- [ ] Tag the release in git

---

## Support

If you encounter build issues:

1. Check this guide thoroughly
2. Search existing GitHub issues
3. Create new issue with:
   - Python version (`python --version`)
   - Windows version
   - Full error message
   - Steps to reproduce

---

## Success! 🎉

You now have a standalone Windows executable that you can distribute to users!

**Next steps**:
1. Test thoroughly on different machines
2. Create a GitHub release
3. Share with users
4. Collect feedback

Happy building! 🚀
