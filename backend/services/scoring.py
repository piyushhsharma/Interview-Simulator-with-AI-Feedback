import re
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class ScoringService:
    def __init__(self):
        # HashMap technical keywords for evaluation
        self.technical_keywords = [
            "hash", "bucket", "collision", "array", "linked list", "key", "value",
            "hashcode", "equals", "load factor", "capacity", "resize", "rehash",
            "time complexity", "space complexity", "O(1)", "constant time",
            "chaining", "open addressing", "tree map", "red-black tree"
        ]
        
        # Filler words to detect
        self.filler_words = ["uh", "um", "like", "you know", "actually", "basically"]
        
        # Passive voice indicators
        self.passive_indicators = ["is", "are", "was", "were", "been", "being", "by"]
    
    def calculate_clarity_score(self, transcript: str) -> Tuple[int, str]:
        """
        Calculate clarity score based on sentence structure, fillers, and logical flow.
        
        Returns:
            Tuple of (score_0_to_10, feedback)
        """
        score = 10
        feedback_points = []
        
        # Count filler words
        filler_count = 0
        for filler in self.filler_words:
            filler_count += len(re.findall(rf'\b{re.escape(filler)}\b', transcript, re.IGNORECASE))
        
        if filler_count > 5:
            score -= 3
            feedback_points.append(f"Too many filler words ({filler_count} found)")
        elif filler_count > 2:
            score -= 1
            feedback_points.append("Some filler words detected")
        
        # Check sentence structure
        sentences = re.split(r'[.!?]+', transcript)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 3:
            score -= 2
            feedback_points.append("Response too short, needs more structure")
        elif len(sentences) > 10:
            score -= 1
            feedback_points.append("Very long response, could be more concise")
        
        # Check for logical flow indicators
        flow_indicators = ["first", "then", "next", "finally", "because", "therefore", "so"]
        flow_count = sum(1 for indicator in flow_indicators if indicator in transcript.lower())
        
        if flow_count == 0:
            score -= 1
            feedback_points.append("Lacks logical flow indicators")
        
        score = max(0, min(10, score))
        feedback = "Your explanation was " + ("well-structured" if score >= 7 else "somewhat structured" if score >= 5 else "poorly structured")
        if feedback_points:
            feedback += ". " + ". ".join(feedback_points) + "."
        
        return score, feedback
    
    def calculate_confidence_score(self, transcript: str) -> Tuple[int, str]:
        """
        Calculate confidence score based on hesitation, passive language, and substance.
        
        Returns:
            Tuple of (score_0_to_10, feedback)
        """
        score = 10
        feedback_points = []
        
        # Count hesitation markers
        hesitation_markers = ["well", "let me think", "i guess", "maybe", "perhaps", "i think"]
        hesitation_count = sum(1 for marker in hesitation_markers if marker in transcript.lower())
        
        if hesitation_count > 3:
            score -= 2
            feedback_points.append("Shows hesitation in response")
        
        # Check passive voice usage
        words = transcript.lower().split()
        passive_count = sum(1 for word in words if word in self.passive_indicators)
        
        if passive_count > len(words) * 0.15:  # More than 15% passive
            score -= 2
            feedback_points.append("Uses passive language frequently")
        
        # Check length vs substance ratio
        if len(transcript.split()) < 30:
            score -= 3
            feedback_points.append("Response too brief for the question")
        elif len(transcript.split()) > 200:
            score -= 1
            feedback_points.append("Response overly verbose")
        
        # Check for confident language
        confident_words = ["definitely", "certainly", "absolutely", "clearly", "obviously"]
        confident_count = sum(1 for word in confident_words if word in transcript.lower())
        
        if confident_count == 0:
            score -= 1
            feedback_points.append("Lacks confident language")
        
        score = max(0, min(10, score))
        confidence_level = "confident" if score >= 7 else "somewhat confident" if score >= 5 else "lacks confidence"
        feedback = f"You sound {confidence_level}"
        if feedback_points:
            feedback += ". " + ". ".join(feedback_points) + "."
        
        return score, feedback
    
    def calculate_technical_score(self, transcript: str) -> Tuple[int, str]:
        """
        Calculate technical correctness score based on keywords, concepts, and explanation depth.
        
        Returns:
            Tuple of (score_0_to_10, feedback)
        """
        score = 0
        feedback_points = []
        transcript_lower = transcript.lower()
        
        # Check for core HashMap concepts
        core_concepts = {
            "hash function": 2,
            "bucket": 1,
            "collision": 2,
            "array": 1,
            "linked list": 1,
            "key-value": 1,
            "hashcode": 2,
            "equals": 1,
            "load factor": 2,
            "resize": 1,
            "time complexity": 2,
            "o(1)": 2,
            "constant time": 1
        }
        
        for concept, points in core_concepts.items():
            if concept in transcript_lower:
                score += points
        
        # Bonus for advanced concepts
        advanced_concepts = ["chaining", "open addressing", "rehash", "tree map"]
        for concept in advanced_concepts:
            if concept in transcript_lower:
                score += 1
        
        # Normalize to 0-10 scale
        score = min(10, score)
        
        # Generate feedback
        if score >= 8:
            feedback_points.append("Excellent technical explanation")
        elif score >= 6:
            feedback_points.append("Good technical understanding")
        elif score >= 4:
            feedback_points.append("Basic technical knowledge")
        else:
            feedback_points.append("Technical understanding needs improvement")
        
        # Check for missing key concepts
        missing_concepts = []
        if "hash function" not in transcript_lower:
            missing_concepts.append("hash function")
        if "collision" not in transcript_lower:
            missing_concepts.append("collision handling")
        if "time complexity" not in transcript_lower:
            missing_concepts.append("time complexity")
        
        if missing_concepts:
            feedback_points.append(f"Missing key concepts: {', '.join(missing_concepts)}")
        
        feedback = ". ".join(feedback_points) + "."
        
        return score, feedback
    
    def calculate_all_scores(self, transcript: str) -> Dict[str, Tuple[int, str]]:
        """
        Calculate all three scores for the transcript.
        
        Returns:
            Dict with scores and feedback for each category
        """
        return {
            "clarity": self.calculate_clarity_score(transcript),
            "confidence": self.calculate_confidence_score(transcript),
            "technical_correctness": self.calculate_technical_score(transcript)
        }
