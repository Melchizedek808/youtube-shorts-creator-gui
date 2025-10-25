
# YouTube Shorts Creator v2.0 - Windows Edition

🎬 **Create professional split-screen reaction videos with automatic captions in minutes!**

A user-friendly Windows application that creates YouTube Shorts (9:16 vertical videos) with split-screen layout, automatic speech-to-text captions, and background music.

![Windows GUI Application](https://img.shields.io/badge/Platform-Windows-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- **🎥 Split-Screen Layout**: Original video on top (60%), your reaction on bottom (40%)
- **🤖 Auto-Captions**: AI-powered speech-to-text transcription using Whisper
- **💬 Custom Captions**: Add your own text captions
- **🎵 Background Music**: Automatically mixed with your reaction audio
- **📱 YouTube Shorts Ready**: Perfect 9:16 vertical format (1080x1920)
- **🖥️ User-Friendly GUI**: No coding required!
- **📦 Standalone Executable**: No Python installation needed

---

## 📥 Download & Installation

### For Windows Users (Recommended)

1. **Download** the latest release from the [Releases](https://github.com/yourusername/youtube-shorts-creator/releases) page
2. **Extract** the ZIP file to your desired location (e.g., Desktop or Documents)
3. **Run** `YouTube Shorts Creator.exe`
4. That's it! No installation required.

### System Requirements

- **OS**: Windows 10 or Windows 11 (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space (for the app + temporary video processing)
- **Processor**: Any modern CPU (faster = quicker video processing)

---

## 🚀 Quick Start Guide

### Step 1: Select Your Videos

1. **Original Video (Top)**: Click "Browse..." to select the main content video
   - This will be placed on the top 60% of the screen
   - Audio will be muted (only visuals used)

2. **Reaction Video (Bottom)**: Select your reaction video
   - This will be placed on the bottom 40% of the screen
   - Your voice/audio will be kept and transcribed for captions

3. **Background Music**: Select your music file
   - Will be automatically reduced to 30% volume
   - Supports: MP3, WAV, M4A, AAC, OGG, FLAC

### Step 2: Choose Caption Mode

**🤖 Auto (Speech-to-Text)** - *Recommended*
- Automatically transcribes speech from your reaction video
- Creates synchronized, dynamic captions
- Choose Whisper model:
  - **Tiny**: Fastest, good for clear speech
  - **Base**: Recommended - good balance of speed and accuracy
  - **Small**: Better accuracy, slower processing
  - **Medium/Large**: Best accuracy, very slow

**✍️ Manual Text**
- Type your own caption text (e.g., "THE DOG MAN")
- Caption appears throughout the entire video
- Good for static text overlays

**❌ No Captions**
- Skip captions entirely
- Just split-screen video with audio

### Step 3: Select Output Location

- Click "Browse..." next to "Save As"
- Choose where to save your YouTube Short
- Default: Desktop/youtube_short.mp4

### Step 4: Create!

1. Click **"🚀 Create YouTube Short"**
2. Wait 2-10 minutes (depending on video length and settings)
3. Monitor progress in the console output
4. Done! Your video will automatically open in File Explorer

---

## 📖 Detailed Usage Examples

### Example 1: Gaming Reaction Video

```
1. Original Video: gaming_footage.mp4 (gameplay clip)
2. Reaction Video: my_reaction.mp4 (you reacting to gameplay)
3. Background Music: epic_music.mp3
4. Caption Mode: Auto (Speech-to-Text) - Base model
5. Output: gaming_short.mp4

Result: Split-screen gaming short with your commentary transcribed as captions!
```

### Example 2: Horror Movie Reaction

```
1. Original Video: scary_movie_clip.mp4
2. Reaction Video: scared_reaction.mp4
3. Background Music: suspense_music.mp3
4. Caption Mode: Auto (Speech-to-Text) - Small model (better accuracy for screams/whispers)
5. Output: scary_short.mp4

Result: Horror reaction short with accurate captions of your reactions!
```

### Example 3: Product Review with Custom Caption

```
1. Original Video: product_demo.mp4
2. Reaction Video: review_footage.mp4
3. Background Music: upbeat_music.mp3
4. Caption Mode: Manual Text - "GAME CHANGER"
5. Output: product_review_short.mp4

Result: Product review with static "GAME CHANGER" caption!
```

---

## 🎨 Output Specifications

Your finished YouTube Short will have:

- **Resolution**: 1080x1920 (9:16 vertical)
- **Frame Rate**: 30 FPS
- **Video Codec**: H.264 (MP4)
- **Audio Codec**: AAC
- **Bitrate**: 8000k (high quality)
- **Audio Mixing**:
  - Reaction audio: 100% volume
  - Background music: 30% volume
  - Original video: Muted

- **Caption Styling** (when enabled):
  - Yellow/gold background (#FFD700)
  - Black text in bold Arial
  - 90% screen width
  - Positioned in center divider bar

---

## 💡 Tips & Best Practices

### Video Quality
- ✅ Use high-quality source videos (720p or 1080p)
- ✅ Ensure reaction video has clear audio for better transcription
- ✅ Keep videos under 60 seconds for best YouTube Shorts performance

### Auto-Captions
- 🎤 Speak clearly and at a moderate pace
- 🔇 Minimize background noise in your reaction video
- ⚡ Use "Base" model for most cases (good speed + accuracy)
- 🎯 Use "Small" model if transcription quality is poor
- 🚀 Use "Tiny" model for very fast processing (clear speech only)

### Music Selection
- 🎵 Choose music that matches your content mood
- 📢 Don't worry about music volume - automatically adjusted to 30%
- ⚠️ Ensure you have rights to use the music (copyright-free music recommended)

### Performance
- ⏱️ First run may be slower (downloading Whisper model)
- 💾 Auto-captions require 1-10GB disk space for AI models
- 🖥️ Close other heavy applications during processing
- 📊 Processing time ≈ 2-5x your video length

---

## ❓ Troubleshooting

### App won't start
- **Issue**: Double-clicking the .exe does nothing
- **Solution**: 
  - Check if Windows Defender blocked it (right-click > Properties > Unblock)
  - Run as Administrator
  - Make sure you extracted ALL files from the ZIP (don't run from inside ZIP)

### Video processing fails
- **Issue**: Error during video creation
- **Solutions**:
  - Ensure all 3 files (original, reaction, music) are valid video/audio files
  - Check that files aren't corrupted (try opening them in VLC)
  - Make sure you have enough disk space (at least 5GB free)
  - Try a different output location (e.g., Desktop instead of C:\Program Files)

### Auto-captions not working
- **Issue**: No captions appear or transcription fails
- **Solutions**:
  - Switch to "Tiny" or "Base" Whisper model (faster, more reliable)
  - Check that reaction video has audible speech
  - Try using manual caption mode as a fallback
  - Ensure you have 2-5GB free disk space for AI model

### Slow processing
- **Issue**: Taking forever to create video
- **Solutions**:
  - Use "Tiny" or "Base" Whisper model (fastest)
  - Close other applications to free up RAM
  - Use shorter video clips (under 60 seconds)
  - Disable auto-captions if not needed

### Application crashes
- **Issue**: App closes unexpectedly
- **Solutions**:
  - Check console output for error messages before crash
  - Try with smaller/shorter video files first
  - Restart your computer to free up memory
  - Run the app as Administrator

---

## 🔧 Advanced: Building from Source

### For Developers

If you want to build the Windows executable yourself:

#### Prerequisites
- Python 3.8 or higher
- Git

#### Build Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/youtube-shorts-creator-windows.git
cd youtube-shorts-creator-windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Build executable
# On Windows:
build_windows.bat

# On Linux (for testing):
./build_linux.sh

# 4. Find your executable
cd dist
```

The build process takes 5-10 minutes and creates a `dist` folder with your executable.

#### Running from Source (without building)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the GUI
python shorts_creator_gui.py
```

---

## 📂 Project Structure

```
youtube-shorts-creator-windows/
├── shorts_creator_gui.py          # Main GUI application
├── shorts_creator_core.py         # Core video processing logic
├── requirements.txt               # Python dependencies
├── build.spec                     # PyInstaller spec (folder build)
├── build_onefile.spec            # PyInstaller spec (single file)
├── build_windows.bat             # Windows build script
├── build_linux.sh                # Linux build script (for testing)
├── README.md                      # This file
├── WINDOWS_USER_GUIDE.md         # Simplified guide for end users
└── .gitignore                    # Git ignore patterns
```

---

## 🐛 Known Issues

1. **First Run Slow**: First time using auto-captions downloads ~100MB-1GB AI model
2. **Console Shows**: Currently console window may flash briefly on startup (harmless)
3. **Large File Sizes**: Whisper models require significant disk space (1-10GB)
4. **No Real-time Progress**: Progress bar is indeterminate (no percentage shown)

---

## 🗺️ Roadmap

Future improvements planned:

- [ ] Real-time progress percentage
- [ ] Video preview before processing
- [ ] Batch processing (multiple videos at once)
- [ ] Custom caption colors and fonts
- [ ] More layout options (side-by-side, picture-in-picture)
- [ ] Direct YouTube upload integration
- [ ] Watermark support
- [ ] Transition effects

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **OpenAI Whisper** - Amazing speech recognition AI
- **MoviePy** - Powerful video editing library
- **Tkinter** - Built-in Python GUI framework
- **PyInstaller** - Python to executable converter

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/youtube-shorts-creator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/youtube-shorts-creator/discussions)
- **Email**: your.email@example.com

---

## ⭐ Show Your Support

If this tool helped you create amazing YouTube Shorts, please:
- ⭐ Star this repository
- 🐦 Share it on social media
- 💬 Tell your content creator friends!

---

**Made with ❤️ for content creators everywhere**

Happy creating! 🎬✨
