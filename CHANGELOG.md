
# Changelog

All notable changes to YouTube Shorts Creator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-25

### Added - Windows GUI Edition
- 🖥️ Complete Windows GUI application using Tkinter
- 📦 Standalone executable build with PyInstaller
- 💬 Three caption modes: Auto (Speech-to-Text), Manual, and None
- 🤖 Automatic speech transcription using OpenAI Whisper
- 🎨 Modern, user-friendly interface
- 📊 Real-time console output in GUI
- ⚙️ Configurable Whisper model selection (tiny/base/small/medium/large)
- 📁 File browser dialogs for easy file selection
- ✅ Comprehensive input validation
- 📈 Progress indication during processing
- 📂 Auto-open output folder on completion
- ❓ Built-in help system
- 🐛 Detailed error messages and troubleshooting

### Documentation
- 📖 Comprehensive README.md with features and usage
- 📋 WINDOWS_USER_GUIDE.md for non-technical users
- 👨‍💻 DEVELOPER_GUIDE.md for contributors
- 📝 CHANGELOG.md for version tracking
- 📄 MIT LICENSE

### Build System
- 🔨 Windows batch build script (build_windows.bat)
- 🐧 Linux build script for testing (build_linux.sh)
- 📦 PyInstaller spec files (folder and single-file builds)
- 📋 Complete requirements.txt

### Developer Tools
- 🔧 Separated core logic (shorts_creator_core.py) from GUI
- 🎯 Modular architecture for easy maintenance
- 📝 Comprehensive code documentation
- 🔐 Input validation and error handling

## [1.0.0] - 2025-10-25

### Initial Release - Command Line Version
- 🎬 Split-screen video creation (9:16 vertical format)
- 🎥 Original video (top 60%) + Reaction video (bottom 40%)
- 🎵 Background music integration (30% volume)
- 💬 Manual caption support
- 🖤 Black divider bar with yellow captions
- 🔇 Automatic muting of original video
- ⚙️ Command-line interface
- 📊 1080x1920 output (perfect for YouTube Shorts)

---

## Future Roadmap

### Planned for v2.1.0
- [ ] Real-time progress percentage
- [ ] Video preview window
- [ ] Custom caption colors in GUI
- [ ] Multiple font options
- [ ] Batch processing UI

### Planned for v3.0.0
- [ ] Direct YouTube upload integration
- [ ] Multiple layout templates
- [ ] Transition effects
- [ ] Picture-in-picture mode
- [ ] Watermark support
- [ ] Video trimming in GUI
