
#!/usr/bin/env python3
"""
YouTube Shorts Creator - Core Logic
Creates vertical 9:16 videos with reaction overlay and automatic styled captions
"""

import tempfile
from pathlib import Path
from moviepy.editor import (
    VideoFileClip, AudioFileClip, CompositeVideoClip, 
    ColorClip, TextClip, CompositeAudioClip
)
from moviepy.video.fx import resize
import whisper
import warnings

# Suppress Whisper warnings
warnings.filterwarnings("ignore", category=UserWarning, module="whisper")


class ShortsCreator:
    """Creates YouTube Shorts with split-screen layout"""
    
    # Video dimensions for YouTube Shorts (9:16 vertical)
    WIDTH = 1080
    HEIGHT = 1920
    
    # Layout proportions
    TOP_VIDEO_HEIGHT_RATIO = 0.60  # Original video takes 60%
    BOTTOM_VIDEO_HEIGHT_RATIO = 0.40  # Reaction takes 40%
    
    # Divider and caption styling
    DIVIDER_HEIGHT = 120  # Black divider bar height
    CAPTION_BG_COLOR = (255, 215, 0)  # Yellow/gold
    CAPTION_TEXT_COLOR = 'black'
    CAPTION_FONT = 'Arial-Bold'
    CAPTION_FONT_SIZE = 50
    
    def __init__(self, original_video_path, reaction_video_path, 
                 music_path, caption_text=None, auto_captions=True, 
                 whisper_model='base', output_path='output.mp4'):
        """
        Initialize the Shorts Creator
        
        Args:
            original_video_path: Path to the original video (will be muted)
            reaction_video_path: Path to the reaction video (with audio)
            music_path: Path to background music
            caption_text: Optional manual caption text (overrides auto-captions)
            auto_captions: Enable automatic speech-to-text captions (default: True)
            whisper_model: Whisper model size (tiny/base/small/medium/large, default: base)
            output_path: Output file path
        """
        self.original_video_path = Path(original_video_path)
        self.reaction_video_path = Path(reaction_video_path)
        self.music_path = Path(music_path)
        self.caption_text = caption_text
        self.auto_captions = auto_captions
        self.whisper_model = whisper_model
        self.output_path = Path(output_path)
        
        # Validate input files exist
        self._validate_inputs()
        
    def _validate_inputs(self):
        """Check that all input files exist"""
        for file_path in [self.original_video_path, self.reaction_video_path, self.music_path]:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
    
    def _transcribe_audio(self, video_path):
        """
        Transcribe audio from video using Whisper
        Returns list of word segments with timestamps
        """
        print(f"🎤 Transcribing audio with Whisper ({self.whisper_model} model)...")
        print("   ⏳ This may take a minute...")
        
        # Load Whisper model
        model = whisper.load_model(self.whisper_model)
        
        # Transcribe with word-level timestamps
        result = model.transcribe(
            str(video_path),
            word_timestamps=True,
            language='en'  # You can make this configurable
        )
        
        # Extract word-level segments
        word_segments = []
        for segment in result['segments']:
            if 'words' in segment:
                for word in segment['words']:
                    word_segments.append({
                        'word': word['word'].strip(),
                        'start': word['start'],
                        'end': word['end']
                    })
        
        print(f"   ✓ Transcribed {len(word_segments)} words")
        return word_segments
    
    def _chunk_words(self, word_segments, words_per_caption=4):
        """
        Group words into chunks of 3-5 words for better readability
        Returns list of caption chunks with start/end times
        """
        chunks = []
        current_chunk = []
        
        for word_seg in word_segments:
            current_chunk.append(word_seg)
            
            # Create chunk when we have enough words
            if len(current_chunk) >= words_per_caption:
                chunk_text = ' '.join([w['word'] for w in current_chunk])
                chunks.append({
                    'text': chunk_text.upper(),  # All caps for style
                    'start': current_chunk[0]['start'],
                    'end': current_chunk[-1]['end']
                })
                current_chunk = []
        
        # Add remaining words as final chunk
        if current_chunk:
            chunk_text = ' '.join([w['word'] for w in current_chunk])
            chunks.append({
                'text': chunk_text.upper(),
                'start': current_chunk[0]['start'],
                'end': current_chunk[-1]['end']
            })
        
        print(f"   ✓ Created {len(chunks)} caption segments")
        return chunks
    
    def create_short(self):
        """Main method to create the YouTube Short"""
        print("🎬 Loading videos...")
        
        # Load videos
        original_clip = VideoFileClip(str(self.original_video_path))
        reaction_clip = VideoFileClip(str(self.reaction_video_path))
        
        # Get the shortest duration to sync everything
        duration = min(original_clip.duration, reaction_clip.duration)
        
        print(f"📏 Video duration: {duration:.2f} seconds")
        
        # Trim videos to match duration
        original_clip = original_clip.subclip(0, duration)
        reaction_clip = reaction_clip.subclip(0, duration)
        
        print("🔇 Muting original video (only using reaction audio + music)...")
        # IMPORTANT: Remove audio from original video
        original_clip = original_clip.without_audio()
        
        print("📐 Creating layout...")
        # Calculate dimensions for video sections
        top_section_height = int(self.HEIGHT * self.TOP_VIDEO_HEIGHT_RATIO) - self.DIVIDER_HEIGHT // 2
        bottom_section_height = int(self.HEIGHT * self.BOTTOM_VIDEO_HEIGHT_RATIO) - self.DIVIDER_HEIGHT // 2
        
        # Resize and position original video (top)
        original_resized = self._resize_and_crop(original_clip, self.WIDTH, top_section_height)
        original_resized = original_resized.set_position(('center', 0))
        
        # Resize and position reaction video (bottom)
        reaction_resized = self._resize_and_crop(reaction_clip, self.WIDTH, bottom_section_height)
        bottom_y_position = self.HEIGHT - bottom_section_height
        reaction_resized = reaction_resized.set_position(('center', bottom_y_position))
        
        # Create black divider bar
        divider_y = top_section_height
        black_divider = ColorClip(
            size=(self.WIDTH, self.DIVIDER_HEIGHT), 
            color=(0, 0, 0)
        ).set_duration(duration).set_position(('center', divider_y))
        
        # Create captions (auto or manual)
        clips_to_composite = [original_resized, black_divider, reaction_resized]
        
        # Manual caption overrides auto-captions
        if self.caption_text:
            print(f"💬 Adding manual caption: '{self.caption_text}'")
            caption_clip = self._create_static_caption(self.caption_text, duration, divider_y)
            clips_to_composite.insert(2, caption_clip)
        elif self.auto_captions:
            print("💬 Generating automatic captions from speech...")
            caption_clips = self._create_auto_captions(divider_y)
            if caption_clips:
                # Add all auto-caption clips
                for cap_clip in caption_clips:
                    clips_to_composite.insert(2, cap_clip)
                print(f"   ✓ Added {len(caption_clips)} dynamic captions")
        
        # Composite all video elements
        print("🎨 Compositing video layers...")
        final_video = CompositeVideoClip(
            clips_to_composite,
            size=(self.WIDTH, self.HEIGHT)
        ).set_duration(duration)
        
        # Audio mixing (ONLY 2 sources: reaction + music)
        print("🎵 Mixing audio (reaction + background music)...")
        audio_clips = []
        
        # Add reaction audio
        if reaction_clip.audio is not None:
            audio_clips.append(reaction_clip.audio)
            print("  ✓ Added reaction audio")
        
        # Add background music
        music_clip = AudioFileClip(str(self.music_path))
        music_clip = music_clip.subclip(0, min(duration, music_clip.duration))
        
        # Lower music volume to 30% so reaction is clear
        music_clip = music_clip.volumex(0.3)
        audio_clips.append(music_clip)
        print("  ✓ Added background music (30% volume)")
        
        # Composite audio
        if audio_clips:
            final_audio = CompositeAudioClip(audio_clips)
            final_video = final_video.set_audio(final_audio)
        
        # Export video
        print(f"🚀 Exporting to {self.output_path}...")
        print("⏳ This may take a few minutes...")
        
        final_video.write_videofile(
            str(self.output_path),
            codec='libx264',
            audio_codec='aac',
            fps=30,
            preset='medium',
            bitrate='8000k'
        )
        
        # Cleanup
        original_clip.close()
        reaction_clip.close()
        music_clip.close()
        
        print(f"✅ Done! Your YouTube Short is ready: {self.output_path}")
        print(f"📊 Output: {self.WIDTH}x{self.HEIGHT} (9:16 vertical)")
        print(f"🔊 Audio sources: Reaction + Background Music (Original video muted)")
    
    def _resize_and_crop(self, clip, target_width, target_height):
        """
        Resize and crop clip to fit target dimensions while maintaining aspect ratio
        """
        clip_aspect = clip.w / clip.h
        target_aspect = target_width / target_height
        
        if clip_aspect > target_aspect:
            # Clip is wider - fit to height and crop width
            new_height = target_height
            new_width = int(new_height * clip_aspect)
            resized = clip.resize(height=new_height)
            x_center = (new_width - target_width) // 2
            cropped = resized.crop(x1=x_center, width=target_width)
        else:
            # Clip is taller - fit to width and crop height
            new_width = target_width
            new_height = int(new_width / clip_aspect)
            resized = clip.resize(width=new_width)
            y_center = (new_height - target_height) // 2
            cropped = resized.crop(y1=y_center, height=target_height)
        
        return cropped
    
    def _create_static_caption(self, caption_text, duration, divider_y):
        """
        Create static yellow caption banner with black text (for manual captions)
        """
        # Caption banner dimensions
        banner_width = int(self.WIDTH * 0.9)  # 90% of screen width
        banner_height = 80
        
        # Create yellow background banner
        banner = ColorClip(
            size=(banner_width, banner_height),
            color=self.CAPTION_BG_COLOR
        ).set_duration(duration)
        
        # Create black text
        try:
            text = TextClip(
                caption_text,
                fontsize=self.CAPTION_FONT_SIZE,
                color=self.CAPTION_TEXT_COLOR,
                font=self.CAPTION_FONT,
                method='caption',
                size=(banner_width - 20, None)  # Add padding
            ).set_duration(duration)
        except:
            # Fallback if Arial-Bold not available
            text = TextClip(
                caption_text,
                fontsize=self.CAPTION_FONT_SIZE,
                color=self.CAPTION_TEXT_COLOR,
                method='caption',
                size=(banner_width - 20, None)
            ).set_duration(duration)
        
        # Center text on banner
        text = text.set_position(('center', 'center'))
        
        # Composite text on banner
        caption_composite = CompositeVideoClip(
            [banner, text],
            size=(banner_width, banner_height)
        ).set_duration(duration)
        
        # Position caption in the middle of the divider
        caption_y = divider_y + (self.DIVIDER_HEIGHT - banner_height) // 2
        caption_composite = caption_composite.set_position(('center', caption_y))
        
        return caption_composite
    
    def _create_auto_captions(self, divider_y):
        """
        Create dynamic auto-captions from speech-to-text transcription
        Returns list of caption clips with timing
        """
        # Transcribe the reaction video
        word_segments = self._transcribe_audio(self.reaction_video_path)
        
        if not word_segments:
            print("   ⚠️ No speech detected in reaction video")
            return []
        
        # Chunk words into caption segments
        caption_chunks = self._chunk_words(word_segments, words_per_caption=4)
        
        # Create a caption clip for each chunk
        caption_clips = []
        banner_width = int(self.WIDTH * 0.9)
        banner_height = 80
        caption_y = divider_y + (self.DIVIDER_HEIGHT - banner_height) // 2
        
        for i, chunk in enumerate(caption_chunks):
            # Create yellow background banner
            banner = ColorClip(
                size=(banner_width, banner_height),
                color=self.CAPTION_BG_COLOR
            ).set_duration(chunk['end'] - chunk['start'])
            
            # Create black text
            try:
                text = TextClip(
                    chunk['text'],
                    fontsize=self.CAPTION_FONT_SIZE,
                    color=self.CAPTION_TEXT_COLOR,
                    font=self.CAPTION_FONT,
                    method='caption',
                    size=(banner_width - 20, None)
                ).set_duration(chunk['end'] - chunk['start'])
            except:
                # Fallback if Arial-Bold not available
                text = TextClip(
                    chunk['text'],
                    fontsize=self.CAPTION_FONT_SIZE,
                    color=self.CAPTION_TEXT_COLOR,
                    method='caption',
                    size=(banner_width - 20, None)
                ).set_duration(chunk['end'] - chunk['start'])
            
            # Center text on banner
            text = text.set_position(('center', 'center'))
            
            # Composite text on banner
            caption_composite = CompositeVideoClip(
                [banner, text],
                size=(banner_width, banner_height)
            ).set_duration(chunk['end'] - chunk['start'])
            
            # Position and time the caption
            caption_composite = caption_composite.set_position(('center', caption_y))
            caption_composite = caption_composite.set_start(chunk['start'])
            
            caption_clips.append(caption_composite)
        
        return caption_clips
