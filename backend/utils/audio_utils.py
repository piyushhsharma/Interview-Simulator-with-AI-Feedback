import librosa
import numpy as np
from io import BytesIO
import tempfile
import os

def process_audio_file(audio_bytes: bytes, sample_rate: int = 16000) -> str:
    """
    Process uploaded audio file and save as temporary WAV file for Whisper.
    
    Args:
        audio_bytes: Raw audio bytes from upload
        sample_rate: Target sample rate for Whisper (16kHz)
    
    Returns:
        Path to temporary audio file
    """
    try:
        # Load audio from bytes
        audio_data, sr = librosa.load(BytesIO(audio_bytes), sr=sample_rate)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_path = temp_file.name
        temp_file.close()
        
        # Save processed audio
        librosa.output.write_wav(temp_path, audio_data, sample_rate)
        
        return temp_path
    except Exception as e:
        raise Exception(f"Audio processing failed: {str(e)}")
    finally:
        if 'temp_file' in locals() and not temp_file.closed:
            temp_file.close()

def cleanup_temp_file(file_path: str):
    """Clean up temporary audio file."""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except Exception:
        pass
