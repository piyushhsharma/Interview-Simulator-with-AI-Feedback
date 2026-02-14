import whisper
import torch
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class TranscriptionService:
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model for transcription."""
        try:
            # Use base model for balance of speed and accuracy
            self.model = whisper.load_model("base")
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            raise
    
    def transcribe_audio(self, audio_path: str) -> Optional[str]:
        """
        Transcribe audio file to text using Whisper.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            result = self.model.transcribe(audio_path)
            transcript = result["text"].strip()
            logger.info(f"Transcription completed: {len(transcript)} characters")
            return transcript
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            return None
