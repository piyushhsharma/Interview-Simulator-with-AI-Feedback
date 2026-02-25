from datetime import datetime
from typing import Optional, Dict, Any, List

class EvaluationResult:
    def __init__(
        self,
        evaluation_id: Optional[str] = None,
        answer_id: Optional[str] = None,
        clarity_score: Optional[Dict[str, Any]] = None,
        confidence_score: Optional[Dict[str, Any]] = None,
        technical_score: Optional[Dict[str, Any]] = None,
        structure_analysis: Optional[Dict[str, Any]] = None,
        coverage_analysis: Optional[Dict[str, Any]] = None,
        overall_score: Optional[float] = None,
        suggestions: Optional[List[str]] = None,
        created_at: Optional[datetime] = None
    ):
        self.evaluation_id = evaluation_id or f"eval_{answer_id}_{int(datetime.now().timestamp())}"
        self.answer_id = answer_id
        self.clarity_score = clarity_score or {}
        self.confidence_score = confidence_score or {}
        self.technical_score = technical_score or {}
        self.structure_analysis = structure_analysis or {}
        self.coverage_analysis = coverage_analysis or {}
        self.overall_score = overall_score
        self.suggestions = suggestions or []
        self.created_at = created_at or datetime.now()

    def to_dict(self) -> dict:
        return {
            'evaluation_id': self.evaluation_id,
            'answer_id': self.answer_id,
            'clarity_score': self.clarity_score,
            'confidence_score': self.confidence_score,
            'technical_score': self.technical_score,
            'structure_analysis': self.structure_analysis,
            'coverage_analysis': self.coverage_analysis,
            'overall_score': self.overall_score,
            'suggestions': self.suggestions,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'EvaluationResult':
        return cls(
            evaluation_id=data.get('evaluation_id'),
            answer_id=data.get('answer_id'),
            clarity_score=data.get('clarity_score', {}),
            confidence_score=data.get('confidence_score', {}),
            technical_score=data.get('technical_score', {}),
            structure_analysis=data.get('structure_analysis', {}),
            coverage_analysis=data.get('coverage_analysis', {}),
            overall_score=data.get('overall_score'),
            suggestions=data.get('suggestions', []),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
