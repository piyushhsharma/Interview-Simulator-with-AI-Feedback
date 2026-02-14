from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class FeedbackService:
    def __init__(self):
        self.suggestions_map = {
            "clarity_issues": [
                "Reduce filler words (uh, um, like)",
                "Structure your answer with clear beginning, middle, and end",
                "Use transition words to improve flow",
                "Practice speaking in complete sentences"
            ],
            "confidence_issues": [
                "Practice the answer multiple times before interviews",
                "Use active voice instead of passive voice",
                "Start with a strong opening statement",
                "Avoid hesitation markers like 'I think' or 'maybe'"
            ],
            "technical_issues": [
                "Study core data structures and algorithms",
                "Include time and space complexity analysis",
                "Provide real-world examples",
                "Explain trade-offs between different approaches"
            ]
        }
    
    def generate_suggestions(self, scores: Dict[str, int], feedback: Dict[str, str]) -> List[str]:
        """
        Generate personalized suggestions based on scores and feedback.
        
        Args:
            scores: Dictionary of scores for each category
            feedback: Dictionary of feedback for each category
            
        Returns:
            List of actionable suggestions
        """
        suggestions = []
        
        # Analyze each score and add relevant suggestions
        if scores["clarity"] < 6:
            suggestions.extend(self.suggestions_map["clarity_issues"][:2])
        
        if scores["confidence"] < 6:
            suggestions.extend(self.suggestions_map["confidence_issues"][:2])
        
        if scores["technical_correctness"] < 6:
            suggestions.extend(self.suggestions_map["technical_issues"][:2])
        
        # Add specific suggestions based on feedback content
        for category, feedback_text in feedback.items():
            if "filler" in feedback_text.lower():
                suggestions.append("Practice recording yourself and count filler words")
            
            if "hesitation" in feedback_text.lower():
                suggestions.append("Prepare a mental outline before speaking")
            
            if "missing" in feedback_text.lower() and "concept" in feedback_text.lower():
                suggestions.append("Review fundamental HashMap implementation details")
        
        # Remove duplicates and limit to top 5 suggestions
        unique_suggestions = list(dict.fromkeys(suggestions))
        return unique_suggestions[:5]
    
    def generate_complete_feedback(self, transcript: str, scores_data: Dict[str, tuple]) -> Dict:
        """
        Generate complete feedback structure.
        
        Args:
            transcript: The transcribed text
            scores_data: Dictionary with (score, feedback) tuples for each category
            
        Returns:
            Complete feedback structure matching the required JSON format
        """
        # Extract scores and feedback
        scores = {}
        feedback = {}
        
        for category, (score, feedback_text) in scores_data.items():
            scores[category] = score
            feedback[category] = feedback_text
        
        # Generate suggestions
        suggestions = self.generate_suggestions(scores, feedback)
        
        # Build complete response
        complete_feedback = {
            "transcript": transcript,
            "scores": scores,
            "feedback": feedback,
            "suggestions": suggestions
        }
        
        logger.info(f"Generated feedback for transcript of length {len(transcript)}")
        return complete_feedback
