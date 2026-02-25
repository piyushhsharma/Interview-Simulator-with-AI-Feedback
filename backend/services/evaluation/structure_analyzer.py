import re
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class StructureAnalyzer:
    def __init__(self):
        # Structure patterns and indicators
        self.structure_patterns = {
            "introduction": [
                r"\b(first|to start|in the beginning|initially|let me begin|i'll start)\b",
                r"\b(a .+ is|the .+ is|.+ refers to|.+ can be defined as)\b"
            ],
            "explanation": [
                r"\b(it works by|the way it works|how it works|the mechanism)\b",
                r"\b(because|since|due to|as a result|therefore)\b",
                r"\b(the process involves|steps include|the algorithm)\b"
            ],
            "example": [
                r"\b(for example|for instance|such as|like|consider)\b",
                r"\b(let's say|imagine|suppose|if we have)\b",
                r"\b(in practice|in real world|practically)\b"
            ],
            "conclusion": [
                r"\b(finally|in conclusion|to summarize|in summary|so overall)\b",
                r"\b(to wrap up|in conclusion|as you can see)\b",
                r"\b(the key point is|the main takeaway is)\b"
            ]
        }
        
        # Transition words for different parts
        self.transition_words = {
            "introduction": ["first", "to start", "initially", "let me begin"],
            "explanation": ["because", "since", "due to", "therefore", "the way"],
            "example": ["for example", "for instance", "such as", "like", "consider"],
            "conclusion": ["finally", "in conclusion", "to summarize", "so overall"]
        }

    def analyze_answer_structure(self, transcript: str) -> Dict[str, Any]:
        """Analyze the structure of the answer."""
        transcript_lower = transcript.lower()
        sentences = re.split(r'[.!?]+', transcript)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        structure_detected = {
            "introduction": False,
            "explanation": False,
            "example": False,
            "conclusion": False
        }
        
        structure_evidence = {
            "introduction": [],
            "explanation": [],
            "example": [],
            "conclusion": []
        }
        
        structure_positions = {
            "introduction": -1,
            "explanation": -1,
            "example": -1,
            "conclusion": -1
        }
        
        # Detect each structure component
        for component, patterns in self.structure_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, transcript_lower, re.IGNORECASE))
                if matches:
                    structure_detected[component] = True
                    structure_positions[component] = matches[0].start()
                    
                    # Capture evidence (the matched phrase)
                    for match in matches[:2]:  # Take first 2 matches
                        start = max(0, match.start() - 20)
                        end = min(len(transcript), match.end() + 20)
                        context = transcript[start:end].strip()
                        structure_evidence[component].append(context)
        
        # Analyze structure quality
        structure_score = self._calculate_structure_score(structure_detected, structure_positions)
        structure_issues = self._identify_structure_issues(structure_detected, structure_positions)
        structure_suggestions = self._generate_structure_suggestions(structure_detected, structure_issues)
        
        # Sentence-level analysis
        sentence_analysis = self._analyze_sentences(sentences)
        
        return {
            "structure_detected": structure_detected,
            "structure_positions": structure_positions,
            "structure_evidence": structure_evidence,
            "structure_score": structure_score,
            "issues": structure_issues,
            "suggestions": structure_suggestions,
            "sentence_analysis": sentence_analysis,
            "total_sentences": len(sentences),
            "logical_flow": self._assess_logical_flow(structure_detected, structure_positions)
        }

    def _calculate_structure_score(self, structure_detected: Dict, positions: Dict) -> float:
        """Calculate overall structure score."""
        base_score = 0
        
        # Points for having each component
        component_weights = {
            "introduction": 2.5,
            "explanation": 3.0,
            "example": 2.0,
            "conclusion": 2.5
        }
        
        for component, detected in structure_detected.items():
            if detected:
                base_score += component_weights[component]
        
        # Bonus for logical order
        if self._is_logical_order(positions):
            base_score += 1.0
        
        return min(10.0, base_score)

    def _is_logical_order(self, positions: Dict) -> bool:
        """Check if structure follows logical order."""
        # Expected order: intro -> explanation -> example -> conclusion
        order = ["introduction", "explanation", "example", "conclusion"]
        detected_positions = [(pos, comp) for comp, pos in positions.items() if pos >= 0]
        detected_positions.sort()
        
        detected_components = [comp for pos, comp in detected_positions]
        
        # Check if components appear in logical order
        for i in range(len(detected_components) - 1):
            current_idx = order.index(detected_components[i])
            next_idx = order.index(detected_components[i + 1])
            if current_idx > next_idx:
                return False
        
        return True

    def _identify_structure_issues(self, structure_detected: Dict, positions: Dict) -> List[str]:
        """Identify structural issues."""
        issues = []
        
        if not structure_detected["introduction"]:
            issues.append("Missing clear introduction")
        
        if not structure_detected["explanation"]:
            issues.append("Lacks detailed explanation")
        
        if not structure_detected["example"]:
            issues.append("No examples provided")
        
        if not structure_detected["conclusion"]:
            issues.append("Missing conclusion or summary")
        
        # Check for logical flow issues
        if structure_detected["example"] and structure_detected["introduction"]:
            intro_pos = positions["introduction"]
            example_pos = positions["example"]
            explanation_pos = positions["explanation"]
            
            if explanation_pos == -1 and example_pos > intro_pos:
                issues.append("Example appears before explanation")
        
        return issues

    def _generate_structure_suggestions(self, structure_detected: Dict, issues: List[str]) -> List[str]:
        """Generate structure improvement suggestions."""
        suggestions = []
        
        if not structure_detected["introduction"]:
            suggestions.append("Start with a clear definition or overview")
        
        if not structure_detected["explanation"]:
            suggestions.append("Provide detailed explanation of how things work")
        
        if not structure_detected["example"]:
            suggestions.append("Include real-world examples to illustrate concepts")
        
        if not structure_detected["conclusion"]:
            suggestions.append("End with a summary or key takeaway")
        
        if len(issues) > 2:
            suggestions.append("Structure your answer with clear beginning, middle, and end")
        
        return suggestions

    def _analyze_sentences(self, sentences: List[str]) -> Dict[str, Any]:
        """Analyze sentence-level characteristics."""
        if not sentences:
            return {
                "avg_length": 0,
                "length_variance": 0,
                "complex_sentences": 0,
                "simple_sentences": 0,
                "sentence_types": []
            }
        
        lengths = [len(s.split()) for s in sentences]
        avg_length = sum(lengths) / len(lengths)
        
        # Calculate variance
        variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
        
        # Classify sentences
        complex_sentences = sum(1 for length in lengths if length > 20)
        simple_sentences = sum(1 for length in lengths if length < 8)
        
        # Identify sentence types
        sentence_types = []
        for sentence in sentences:
            if any(word in sentence.lower() for word in ["because", "since", "therefore", "however"]):
                sentence_types.append("complex")
            elif any(word in sentence.lower() for word in ["and", "but", "or"]):
                sentence_types.append("compound")
            else:
                sentence_types.append("simple")
        
        return {
            "avg_length": round(avg_length, 1),
            "length_variance": round(variance, 1),
            "complex_sentences": complex_sentences,
            "simple_sentences": simple_sentences,
            "sentence_types": sentence_types[:5]  # First 5 sentence types
        }

    def _assess_logical_flow(self, structure_detected: Dict, positions: Dict) -> str:
        """Assess the logical flow of the answer."""
        detected_count = sum(structure_detected.values())
        
        if detected_count == 0:
            return "no_structure"
        elif detected_count == 1:
            return "minimal_structure"
        elif detected_count == 2:
            return "basic_structure"
        elif detected_count == 3:
            return "good_structure"
        else:
            if self._is_logical_order(positions):
                return "excellent_structure"
            else:
                return "disorganized_structure"
