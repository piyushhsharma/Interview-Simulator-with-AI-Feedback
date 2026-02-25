from typing import Dict, Any, Optional
import logging
from datetime import datetime

from models.evaluation_result import EvaluationResult
from models.answer import Answer
from models.question import Question
from services.evaluation.enhanced_scoring import EnhancedScoringService
from services.evaluation.structure_analyzer import StructureAnalyzer
from services.evaluation.coverage_analyzer import CoverageAnalyzer
from services.evaluation.voice_analyzer import VoiceAnalyzer

logger = logging.getLogger(__name__)

class EnhancedEvaluationService:
    def __init__(self):
        self.scoring_service = EnhancedScoringService()
        self.structure_analyzer = StructureAnalyzer()
        self.coverage_analyzer = CoverageAnalyzer()
        self.voice_analyzer = VoiceAnalyzer()

    def evaluate_answer(
        self, 
        answer: Answer, 
        question: Question,
        audio_path: Optional[str] = None
    ) -> EvaluationResult:
        """Perform comprehensive evaluation of an answer."""
        try:
            # Get audio metadata if available
            audio_metadata = {}
            if audio_path:
                audio_metadata = self.voice_analyzer.analyze_audio_features(audio_path)
                # Add duration to answer object
                answer.audio_duration = audio_metadata.get('duration', 0)
                answer.audio_metadata = audio_metadata

            # Enhanced scoring with detailed feedback
            clarity_result = self.scoring_service.calculate_enhanced_clarity_score(answer.transcript)
            confidence_result = self.scoring_service.calculate_enhanced_confidence_score(
                answer.transcript, audio_metadata
            )
            technical_result = self.scoring_service.calculate_enhanced_technical_score(
                answer.transcript, {
                    'must_have_concepts': question.must_have_concepts,
                    'good_to_have_concepts': question.good_to_have_concepts,
                    'red_flags': question.red_flags
                }
            )

            # Structure analysis
            structure_result = self.structure_analyzer.analyze_answer_structure(answer.transcript)

            # Coverage analysis
            coverage_result = self.coverage_analyzer.analyze_concept_coverage(
                answer.transcript, 
                question.ideal_answer,
                {
                    'must_have_concepts': question.must_have_concepts,
                    'good_to_have_concepts': question.good_to_have_concepts,
                    'red_flags': question.red_flags
                }
            )

            # Calculate overall score
            overall_score = self._calculate_overall_score(
                clarity_result['score'],
                confidence_result['score'],
                technical_result['score']
            )

            # Generate comprehensive suggestions
            suggestions = self._generate_comprehensive_suggestions(
                clarity_result, confidence_result, technical_result,
                structure_result, coverage_result
            )

            # Create evaluation result
            evaluation = EvaluationResult(
                answer_id=answer.answer_id,
                clarity_score=clarity_result,
                confidence_score=confidence_result,
                technical_score=technical_result,
                structure_analysis=structure_result,
                coverage_analysis=coverage_result,
                overall_score=overall_score,
                suggestions=suggestions
            )

            logger.info(f"Evaluation completed for answer {answer.answer_id}")
            return evaluation

        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            # Return fallback evaluation
            return self._create_fallback_evaluation(answer)

    def _calculate_overall_score(self, clarity: float, confidence: float, technical: float) -> float:
        """Calculate weighted overall score."""
        # Technical correctness is most important (40%), clarity (30%), confidence (30%)
        weights = {'technical': 0.4, 'clarity': 0.3, 'confidence': 0.3}
        overall = (technical * weights['technical'] + 
                  clarity * weights['clarity'] + 
                  confidence * weights['confidence'])
        return round(overall, 1)

    def _generate_comprehensive_suggestions(
        self, clarity: Dict, confidence: Dict, technical: Dict,
        structure: Dict, coverage: Dict
    ) -> list:
        """Generate comprehensive improvement suggestions."""
        suggestions = []

        # Clarity suggestions
        if clarity['score'] < 6:
            suggestions.extend(clarity.get('strengths', []))
            if clarity['filler_count'] > 5:
                suggestions.append("Practice reducing filler words like 'um', 'uh', 'like'")
            if clarity['sentence_count'] < 3:
                suggestions.append("Structure your answer with more complete sentences")

        # Confidence suggestions
        if confidence['score'] < 6:
            if confidence['hesitation_count'] > 3:
                suggestions.append("Practice your answers to reduce hesitation")
            if confidence['passive_ratio'] > 0.15:
                suggestions.append("Use more active voice to sound more confident")
            if confidence['confident_words'] == 0:
                suggestions.append("Include confident language like 'definitely', 'certainly'")

        # Technical suggestions
        if technical['score'] < 6:
            if technical['missing_concepts']:
                suggestions.append(f"Study these key concepts: {', '.join(technical['missing_concepts'][:3])}")
            if technical['coverage_percentage'] < 50:
                suggestions.append("Focus on covering the fundamental concepts first")

        # Structure suggestions
        structure_issues = structure.get('issues', [])
        if structure_issues:
            suggestions.extend(structure.get('suggestions', []))

        # Coverage suggestions
        coverage_suggestions = coverage.get('suggestions', [])
        suggestions.extend(coverage_suggestions)

        # Remove duplicates and limit to top 5
        unique_suggestions = list(dict.fromkeys(suggestions))
        return unique_suggestions[:5]

    def _create_fallback_evaluation(self, answer: Answer) -> EvaluationResult:
        """Create a fallback evaluation in case of failures."""
        return EvaluationResult(
            answer_id=answer.answer_id,
            clarity_score={"score": 5, "issues": ["Evaluation failed"], "evidence": [], "strengths": []},
            confidence_score={"score": 5, "issues": ["Evaluation failed"], "evidence": [], "strengths": []},
            technical_score={"score": 5, "issues": ["Evaluation failed"], "evidence": [], "strengths": []},
            structure_analysis={"structure_score": 5, "issues": ["Structure analysis failed"]},
            coverage_analysis={"coverage_percentage": 50, "issues": ["Coverage analysis failed"]},
            overall_score=5.0,
            suggestions=["Please try again or contact support if the issue persists"]
        )
