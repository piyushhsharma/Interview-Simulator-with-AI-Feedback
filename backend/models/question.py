from typing import List, Optional
from datetime import datetime

class Question:
    def __init__(
        self,
        id: int,
        question: str,
        category: str,
        difficulty: str,
        must_have_concepts: Optional[List[str]] = None,
        good_to_have_concepts: Optional[List[str]] = None,
        red_flags: Optional[List[str]] = None,
        ideal_answer: Optional[str] = None
    ):
        self.id = id
        self.question = question
        self.category = category
        self.difficulty = difficulty
        self.must_have_concepts = must_have_concepts or []
        self.good_to_have_concepts = good_to_have_concepts or []
        self.red_flags = red_flags or []
        self.ideal_answer = ideal_answer

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'question': self.question,
            'category': self.category,
            'difficulty': self.difficulty,
            'must_have_concepts': self.must_have_concepts,
            'good_to_have_concepts': self.good_to_have_concepts,
            'red_flags': self.red_flags,
            'ideal_answer': self.ideal_answer
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Question':
        return cls(
            id=data['id'],
            question=data['question'],
            category=data['category'],
            difficulty=data['difficulty'],
            must_have_concepts=data.get('must_have_concepts', []),
            good_to_have_concepts=data.get('good_to_have_concepts', []),
            red_flags=data.get('red_flags', []),
            ideal_answer=data.get('ideal_answer')
        )
