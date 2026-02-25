import librosa
import numpy as np
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class VoiceAnalyzer:
    def analyze_audio_features(self, audio_path: str) -> Dict[str, Any]:
        """Extract voice features from audio file."""
        try:
            # Load audio
            y, sr = librosa.load(audio_path)
            
            # Extract features
            features = {
                "duration": librosa.get_duration(y=y, sr=sr),
                "speaking_rate": self._calculate_speaking_rate(y, sr),
                "pause_analysis": self._analyze_pauses(y, sr),
                "energy_analysis": self._analyze_energy(y, sr),
                "pitch_analysis": self._analyze_pitch(y, sr)
            }
            
            return features
        except Exception as e:
            logger.error(f"Voice analysis failed: {str(e)}")
            return {}

    def _calculate_speaking_rate(self, y: np.ndarray, sr: int) -> float:
        """Calculate speaking rate in words per minute."""
        duration = librosa.get_duration(y=y, sr=sr)
        # Estimate word count using energy peaks
        energy = librosa.feature.rms(y=y)[0]
        peaks = librosa.util.peak_pick(energy, pre_max=3, post_max=3, pre_avg=3, post_avg=3, delta=0.5, wait=10)
        estimated_words = len(peaks)
        wpm = (estimated_words / duration) * 60 if duration > 0 else 0
        return round(wpm, 1)

    def _analyze_pauses(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Analyze pauses in speech."""
        energy = librosa.feature.rms(y=y)[0]
        threshold = np.mean(energy) * 0.3
        silence_frames = energy < threshold
        
        # Find continuous silence segments
        pause_durations = []
        current_pause = 0
        
        for is_silent in silence_frames:
            if is_silent:
                current_pause += 1
            else:
                if current_pause > 10:  # Minimum pause duration
                    pause_duration = current_pause / sr
                    pause_durations.append(pause_duration)
                current_pause = 0
        
        long_pauses = sum(1 for p in pause_durations if p > 1.0)
        
        return {
            "total_pauses": len(pause_durations),
            "long_pauses": long_pauses,
            "avg_pause_duration": np.mean(pause_durations) if pause_durations else 0
        }

    def _analyze_energy(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Analyze energy levels."""
        energy = librosa.feature.rms(y=y)[0]
        return {
            "avg_energy": float(np.mean(energy)),
            "energy_variance": float(np.var(energy)),
            "energy_range": float(np.max(energy) - np.min(energy))
        }

    def _analyze_pitch(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Analyze pitch characteristics."""
        try:
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_values = []
            
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if pitch_values:
                return {
                    "avg_pitch": float(np.mean(pitch_values)),
                    "pitch_variance": float(np.var(pitch_values)),
                    "pitch_range": float(np.max(pitch_values) - np.min(pitch_values))
                }
        except:
            pass
        
        return {"avg_pitch": 0, "pitch_variance": 0, "pitch_range": 0}
