
#!/usr/bin/env python3
"""
YouTube Shorts Creator - Windows GUI Application
User-friendly interface for creating split-screen reaction videos with auto-captions
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
import os
from pathlib import Path
import queue
from datetime import datetime

# Import the core shorts creator logic
from shorts_creator_core import ShortsCreator


class TextRedirector:
    """Redirect stdout/stderr to GUI text widget"""
    def __init__(self, text_widget, tag="stdout"):
        self.text_widget = text_widget
        self.tag = tag

    def write(self, text):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, text, (self.tag,))
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')
        self.text_widget.update_idletasks()

    def flush(self):
        pass


class ShortsCreatorGUI:
    """Main GUI application for YouTube Shorts Creator"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Shorts Creator v2.0 - Windows Edition")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        # Set icon (if available)
        try:
            if sys.platform == 'win32':
                self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Variables for file paths
        self.original_video_path = tk.StringVar()
        self.reaction_video_path = tk.StringVar()
        self.music_path = tk.StringVar()
        self.output_path = tk.StringVar(value=str(Path.home() / "Desktop" / "youtube_short.mp4"))
        
        # Caption settings
        self.caption_mode = tk.StringVar(value="auto")  # auto, manual, none
        self.manual_caption_text = tk.StringVar()
        self.whisper_model = tk.StringVar(value="base")
        
        # Processing flag
        self.is_processing = False
        
        # Create UI
        self._create_widgets()
        
        # Redirect stdout to console
        sys.stdout = TextRedirector(self.console, "stdout")
        sys.stderr = TextRedirector(self.console, "stderr")
        
        # Print welcome message
        self._print_welcome()
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # ===== HEADER =====
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame,
            text="🎬 YouTube Shorts Creator",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Create split-screen reaction videos with automatic captions",
            font=("Arial", 9)
        )
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
        
        # ===== FILE SELECTION SECTION =====
        files_frame = ttk.LabelFrame(main_frame, text="📁 Video Files", padding="10")
        files_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        files_frame.columnconfigure(1, weight=1)
        
        # Original Video
        ttk.Label(files_frame, text="Original Video (Top):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(files_frame, textvariable=self.original_video_path).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(files_frame, text="Browse...", command=self._browse_original_video).grid(row=0, column=2)
        
        # Reaction Video
        ttk.Label(files_frame, text="Reaction Video (Bottom):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(files_frame, textvariable=self.reaction_video_path).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(files_frame, text="Browse...", command=self._browse_reaction_video).grid(row=1, column=2)
        
        # Background Music
        ttk.Label(files_frame, text="Background Music:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(files_frame, textvariable=self.music_path).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(files_frame, text="Browse...", command=self._browse_music).grid(row=2, column=2)
        
        # ===== CAPTION SETTINGS SECTION =====
        caption_frame = ttk.LabelFrame(main_frame, text="💬 Caption Settings", padding="10")
        caption_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        caption_frame.columnconfigure(1, weight=1)
        
        # Caption Mode Selection
        ttk.Label(caption_frame, text="Caption Mode:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        caption_mode_frame = ttk.Frame(caption_frame)
        caption_mode_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(
            caption_mode_frame,
            text="🤖 Auto (Speech-to-Text)",
            variable=self.caption_mode,
            value="auto",
            command=self._update_caption_options
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            caption_mode_frame,
            text="✍️ Manual Text",
            variable=self.caption_mode,
            value="manual",
            command=self._update_caption_options
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            caption_mode_frame,
            text="❌ No Captions",
            variable=self.caption_mode,
            value="none",
            command=self._update_caption_options
        ).pack(side=tk.LEFT, padx=5)
        
        # Whisper Model Selection (for auto captions)
        self.whisper_label = ttk.Label(caption_frame, text="Whisper Model:")
        self.whisper_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.whisper_combo = ttk.Combobox(
            caption_frame,
            textvariable=self.whisper_model,
            values=["tiny (fastest)", "base (recommended)", "small (better accuracy)", "medium (slow)", "large (very slow)"],
            state="readonly",
            width=25
        )
        self.whisper_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.whisper_combo.current(1)  # Default to "base"
        
        # Manual Caption Text Entry
        self.manual_caption_label = ttk.Label(caption_frame, text="Caption Text:")
        self.manual_caption_entry = ttk.Entry(caption_frame, textvariable=self.manual_caption_text, width=50)
        
        # Info labels
        self.caption_info_label = ttk.Label(
            caption_frame,
            text="ℹ️ Auto mode: Transcribes speech from reaction video and creates synced captions",
            font=("Arial", 8),
            foreground="gray"
        )
        self.caption_info_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # ===== OUTPUT SECTION =====
        output_frame = ttk.LabelFrame(main_frame, text="💾 Output Settings", padding="10")
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Save As:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(output_frame, textvariable=self.output_path).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(output_frame, text="Browse...", command=self._browse_output).grid(row=0, column=2)
        
        # ===== PROGRESS SECTION =====
        progress_frame = ttk.LabelFrame(main_frame, text="⚙️ Processing", padding="10")
        progress_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(progress_frame, text="Ready to create your YouTube Short!", font=("Arial", 9))
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # ===== CONSOLE OUTPUT =====
        console_frame = ttk.LabelFrame(main_frame, text="📋 Console Output", padding="10")
        console_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        
        main_frame.rowconfigure(5, weight=1)  # Make console expandable
        
        # Scrolled text widget for console output
        self.console = scrolledtext.ScrolledText(
            console_frame,
            height=12,
            width=80,
            state='disabled',
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.console.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Console controls
        console_controls = ttk.Frame(console_frame)
        console_controls.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        ttk.Button(console_controls, text="Clear Console", command=self._clear_console).pack(side=tk.LEFT)
        
        # ===== ACTION BUTTONS =====
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.create_button = ttk.Button(
            button_frame,
            text="🚀 Create YouTube Short",
            command=self._create_short,
            style="Accent.TButton"
        )
        self.create_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(
            button_frame,
            text="❌ Cancel",
            command=self._cancel_processing,
            state='disabled'
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="❓ Help",
            command=self._show_help
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="📂 Open Output Folder",
            command=self._open_output_folder
        ).pack(side=tk.RIGHT, padx=5)
        
        # Configure styles
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass
    
    def _update_caption_options(self):
        """Update UI based on selected caption mode"""
        mode = self.caption_mode.get()
        
        if mode == "auto":
            # Show Whisper model selection
            self.whisper_label.grid(row=1, column=0, sticky=tk.W, pady=5)
            self.whisper_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
            
            # Hide manual caption entry
            self.manual_caption_label.grid_remove()
            self.manual_caption_entry.grid_remove()
            
            # Update info label
            self.caption_info_label.config(
                text="ℹ️ Auto mode: Transcribes speech from reaction video and creates synced captions"
            )
            self.caption_info_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
            
        elif mode == "manual":
            # Hide Whisper model selection
            self.whisper_label.grid_remove()
            self.whisper_combo.grid_remove()
            
            # Show manual caption entry
            self.manual_caption_label.grid(row=1, column=0, sticky=tk.W, pady=5)
            self.manual_caption_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
            
            # Update info label
            self.caption_info_label.config(
                text="ℹ️ Manual mode: Enter your custom caption text (e.g., 'THE DOG MAN')"
            )
            self.caption_info_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
            
        else:  # none
            # Hide both
            self.whisper_label.grid_remove()
            self.whisper_combo.grid_remove()
            self.manual_caption_label.grid_remove()
            self.manual_caption_entry.grid_remove()
            
            # Update info label
            self.caption_info_label.config(
                text="ℹ️ No captions will be added to the video"
            )
            self.caption_info_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    def _browse_original_video(self):
        """Browse for original video file"""
        filename = filedialog.askopenfilename(
            title="Select Original Video",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.original_video_path.set(filename)
    
    def _browse_reaction_video(self):
        """Browse for reaction video file"""
        filename = filedialog.askopenfilename(
            title="Select Reaction Video",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.reaction_video_path.set(filename)
    
    def _browse_music(self):
        """Browse for background music file"""
        filename = filedialog.askopenfilename(
            title="Select Background Music",
            filetypes=[
                ("Audio files", "*.mp3 *.wav *.m4a *.aac *.ogg *.flac"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.music_path.set(filename)
    
    def _browse_output(self):
        """Browse for output file location"""
        filename = filedialog.asksaveasfilename(
            title="Save YouTube Short As",
            defaultextension=".mp4",
            filetypes=[
                ("MP4 video", "*.mp4"),
                ("All files", "*.*")
            ],
            initialfile="youtube_short.mp4"
        )
        if filename:
            self.output_path.set(filename)
    
    def _clear_console(self):
        """Clear console output"""
        self.console.configure(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.configure(state='disabled')
    
    def _open_output_folder(self):
        """Open the output folder in file explorer"""
        output_file = self.output_path.get()
        if output_file:
            output_dir = Path(output_file).parent
            if output_dir.exists():
                os.startfile(output_dir) if sys.platform == 'win32' else os.system(f'open "{output_dir}"')
            else:
                # Open Desktop as fallback
                desktop = Path.home() / "Desktop"
                os.startfile(desktop) if sys.platform == 'win32' else os.system(f'open "{desktop}"')
    
    def _validate_inputs(self):
        """Validate all user inputs before processing"""
        errors = []
        
        # Check required files
        if not self.original_video_path.get():
            errors.append("• Please select an original video")
        elif not Path(self.original_video_path.get()).exists():
            errors.append("• Original video file not found")
        
        if not self.reaction_video_path.get():
            errors.append("• Please select a reaction video")
        elif not Path(self.reaction_video_path.get()).exists():
            errors.append("• Reaction video file not found")
        
        if not self.music_path.get():
            errors.append("• Please select background music")
        elif not Path(self.music_path.get()).exists():
            errors.append("• Music file not found")
        
        # Check manual caption text if in manual mode
        if self.caption_mode.get() == "manual" and not self.manual_caption_text.get().strip():
            errors.append("• Please enter caption text or switch to Auto/No Captions mode")
        
        # Check output path
        if not self.output_path.get():
            errors.append("• Please specify an output file location")
        
        if errors:
            messagebox.showerror(
                "Input Error",
                "Please fix the following issues:\n\n" + "\n".join(errors)
            )
            return False
        
        return True
    
    def _create_short(self):
        """Start the video creation process"""
        if self.is_processing:
            messagebox.showwarning("Already Processing", "A video is already being created. Please wait.")
            return
        
        # Validate inputs
        if not self._validate_inputs():
            return
        
        # Confirm before processing
        response = messagebox.askyesno(
            "Create YouTube Short",
            "Ready to create your YouTube Short!\n\n"
            "This may take several minutes depending on video length.\n\n"
            "Continue?"
        )
        
        if not response:
            return
        
        # Disable create button and enable cancel
        self.create_button.config(state='disabled')
        self.cancel_button.config(state='normal')
        self.is_processing = True
        
        # Start progress bar
        self.progress_bar.start()
        self.status_label.config(text="Processing... Please wait")
        
        # Clear console
        self._clear_console()
        
        # Start processing in separate thread
        thread = threading.Thread(target=self._process_video, daemon=True)
        thread.start()
    
    def _process_video(self):
        """Process the video (runs in separate thread)"""
        try:
            print("=" * 70)
            print(f"🎬 YouTube Shorts Creator - Started at {datetime.now().strftime('%H:%M:%S')}")
            print("=" * 70)
            print()
            
            # Get caption settings
            caption_text = None
            auto_captions = False
            whisper_model = "base"
            
            mode = self.caption_mode.get()
            if mode == "auto":
                auto_captions = True
                # Extract model name from selection (e.g., "base (recommended)" -> "base")
                whisper_model = self.whisper_model.get().split()[0]
            elif mode == "manual":
                caption_text = self.manual_caption_text.get().strip()
            
            # Create shorts creator instance
            creator = ShortsCreator(
                original_video_path=self.original_video_path.get(),
                reaction_video_path=self.reaction_video_path.get(),
                music_path=self.music_path.get(),
                caption_text=caption_text,
                auto_captions=auto_captions,
                whisper_model=whisper_model,
                output_path=self.output_path.get()
            )
            
            # Create the short
            creator.create_short()
            
            print()
            print("=" * 70)
            print("✅ SUCCESS! Your YouTube Short is ready!")
            print("=" * 70)
            
            # Update UI on success
            self.root.after(0, self._processing_complete, True)
            
        except Exception as e:
            print()
            print("=" * 70)
            print(f"❌ ERROR: {str(e)}")
            print("=" * 70)
            
            # Update UI on error
            self.root.after(0, self._processing_complete, False, str(e))
    
    def _processing_complete(self, success, error_message=None):
        """Called when processing is complete"""
        self.is_processing = False
        self.progress_bar.stop()
        self.create_button.config(state='normal')
        self.cancel_button.config(state='disabled')
        
        if success:
            self.status_label.config(text="✅ Video created successfully!")
            
            response = messagebox.showinfo(
                "Success!",
                f"Your YouTube Short has been created successfully!\n\n"
                f"Location: {self.output_path.get()}\n\n"
                f"Would you like to open the output folder?"
            )
            
            # Auto-open output folder
            self._open_output_folder()
            
        else:
            self.status_label.config(text="❌ Error occurred during processing")
            messagebox.showerror(
                "Error",
                f"An error occurred while creating the video:\n\n{error_message}\n\n"
                "Check the console output for more details."
            )
    
    def _cancel_processing(self):
        """Cancel the current processing (not fully implemented due to threading limitations)"""
        response = messagebox.askyesno(
            "Cancel Processing",
            "Note: The processing cannot be stopped immediately due to video encoding.\n\n"
            "You can close this window, but the process will continue in the background.\n\n"
            "Close the application?"
        )
        
        if response:
            self.root.quit()
    
    def _show_help(self):
        """Show help dialog"""
        help_text = """
YouTube Shorts Creator - Help

📁 VIDEO FILES
• Original Video: The main video content (will be placed on top, muted)
• Reaction Video: Your reaction video (will be placed on bottom, with audio)
• Background Music: Music to play in the background (at 30% volume)

💬 CAPTION MODES
• Auto (Speech-to-Text): Automatically transcribes speech from your reaction 
  video and creates synchronized captions. Choose a Whisper model:
  - tiny: Fastest, lowest accuracy
  - base: Good balance (recommended)
  - small: Better accuracy, slower
  - medium/large: Best accuracy, very slow

• Manual Text: Enter your own caption text to display throughout the video
  Example: "THE DOG MAN"

• No Captions: Create video without any captions

🎬 OUTPUT
The final video will be:
• 9:16 vertical format (1080x1920, perfect for YouTube Shorts)
• Split-screen with original video on top, reaction on bottom
• Yellow captions with black text (if enabled)
• Audio: Reaction + Background Music (original video is muted)

⏱️ PROCESSING TIME
Video creation typically takes 2-10 minutes depending on:
• Video length
• Caption mode (auto-captions take longer)
• Computer speed

💡 TIPS
• Use high-quality video files for best results
• Ensure your reaction video has clear audio for auto-captions
• Background music will be automatically reduced to 30% volume
• The original video's audio is always muted
• All three files (original, reaction, music) will be trimmed to match 
  the shortest duration

🐛 TROUBLESHOOTING
• If auto-captions fail: Try the "tiny" or "base" Whisper model
• If the app freezes: It's likely still processing - check console output
• If videos look stretched: The tool automatically crops to fit 9:16 format

For more information, visit the project GitHub page.
        """
        
        # Create help window
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - YouTube Shorts Creator")
        help_window.geometry("700x600")
        
        # Help text widget
        help_text_widget = scrolledtext.ScrolledText(
            help_window,
            wrap=tk.WORD,
            font=("Arial", 10),
            padx=10,
            pady=10
        )
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.config(state='disabled')
        
        # Close button
        ttk.Button(
            help_window,
            text="Close",
            command=help_window.destroy
        ).pack(pady=10)
    
    def _print_welcome(self):
        """Print welcome message to console"""
        welcome = """
╔════════════════════════════════════════════════════════════════════╗
║       YouTube Shorts Creator v2.0 - Windows Edition                ║
║                 🎬 Create Amazing Shorts! 🎬                       ║
╚════════════════════════════════════════════════════════════════════╝

Welcome! This tool creates split-screen reaction videos with automatic captions.

📋 QUICK START:
1. Select your original video, reaction video, and background music
2. Choose caption mode (Auto recommended for speech-to-text)
3. Select output location
4. Click "Create YouTube Short" and wait

Console output will appear here during processing.

"""
        print(welcome)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ShortsCreatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
