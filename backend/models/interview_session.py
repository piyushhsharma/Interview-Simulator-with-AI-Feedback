from datetime import datetime
from typing import Optional, List
import uuid

class InterviewSession:
    def __init__(
        self,
        session_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        total_questions: int = 0,
        completed_questions: int = 0
    ):
        self.session_id = session_id or str(uuid.uuid4())
        self.created_at = created_at or datetime.now()
        self.completed_at = completed_at
        self.total_questions = total_questions
        self.completed_questions = completed_questions
        self.answers = []  # List of Answer objects

    def to_dict(self) -> dict:
        return {
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'total_questions': self.total_questions,
            'completed_questions': self.completed_questions,
            'answers': [answer.to_dict() for answer in self.answers]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'InterviewSession':
        session = cls(
            session_id=data.get('session_id'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None,
            total_questions=data.get('total_questions', 0),
            completed_questions=data.get('completed_questions', 0)
        )
        # Answers will be loaded separately from database
        return session
