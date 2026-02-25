from datetime import datetime
from typing import Optional, Dict, Any

class Answer:
    def __init__(
        self,
        answer_id: Optional[str] = None,
        session_id: Optional[str] = None,
        question_id: Optional[int] = None,
        transcript: Optional[str] = None,
        audio_duration: Optional[float] = None,
        audio_metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None
    ):
        self.answer_id = answer_id or f"{session_id}_{question_id}_{int(datetime.now().timestamp())}"
        self.session_id = session_id
        self.question_id = question_id
        self.transcript = transcript
        self.audio_duration = audio_duration
        self.audio_metadata = audio_metadata or {}
        self.created_at = created_at or datetime.now()

    def to_dict(self) -> dict:
        return {
            'answer_id': self.answer_id,
            'session_id': self.session_id,
            'question_id': self.question_id,
            'transcript': self.transcript,
            'audio_duration': self.audio_duration,
            'audio_metadata': self.audio_metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Answer':
        return cls(
            answer_id=data.get('answer_id'),
            session_id=data.get('session_id'),
            question_id=data.get('question_id'),
            transcript=data.get('transcript'),
            audio_duration=data.get('audio_duration'),
            audio_metadata=data.get('audio_metadata', {}),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
