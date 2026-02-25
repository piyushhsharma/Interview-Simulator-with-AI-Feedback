import re
from typing import Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class EnhancedScoringService:
    def __init__(self):
        # Enhanced filler words detection
        self.filler_words = {
            "uh": 1, "um": 1, "like": 0.5, "you know": 0.5, "actually": 0.3, 
            "basically": 0.3, "sort of": 0.5, "kind of": 0.5, "I mean": 0.3,
            "you see": 0.3, "right": 0.2, "so": 0.2, "well": 0.3
        }
        
        # Hesitation markers
        self.hesitation_markers = {
            "let me think": 2, "let's see": 1.5, "I guess": 1, "maybe": 1,
            "perhaps": 1, "I think": 0.5, "I believe": 0.3, "probably": 0.5
        }
        
        # Passive voice indicators
        self.passive_indicators = [
            "is", "are", "was", "were", "been", "being", "by"
        ]
        
        # Structure indicators
        self.structure_indicators = {
            "introduction": ["first", "to start", "in the beginning", "initially"],
            "example": ["for example", "for instance", "such as", "like"],
            "conclusion": ["finally", "in conclusion", "to summarize", "in summary"]
        }
        
        # Confident language
        self.confident_words = [
            "definitely", "certainly", "absolutely", "clearly", "obviously",
            "without doubt", "undoubtedly", "specifically", "precisely"
        ]

    def calculate_enhanced_clarity_score(self, transcript: str) -> Dict[str, Any]:
        """Calculate clarity score with detailed analysis."""
        score = 10
        issues = []
        evidence = []
        strengths = []
        
        # Count filler words
        filler_count = 0
        filler_words_found = []
        transcript_lower = transcript.lower()
        
        for filler, weight in self.filler_words.items():
            count = len(re.findall(rf'\b{re.escape(filler)}\b', transcript_lower))
            if count > 0:
                filler_count += count * weight
                filler_words_found.extend([filler] * count)
        
        if filler_count > 8:
            score -= 4
            issues.append("Excessive filler words detected")
            evidence.extend(filler_words_found[:5])  # Show first 5
        elif filler_count > 4:
            score -= 2
            issues.append("Some filler words present")
            evidence.extend(filler_words_found[:3])
        else:
            strengths.append("Minimal use of filler words")
        
        # Check sentence structure
        sentences = re.split(r'[.!?]+', transcript)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        if len(sentences) < 3:
            score -= 2
            issues.append("Too few complete sentences")
        elif avg_sentence_length > 25:
            score -= 1
            issues.append("Sentences too long and complex")
        elif avg_sentence_length < 8:
            score -= 1
            issues.append("Sentences too short and choppy")
        else:
            strengths.append("Good sentence structure and length")
        
        # Check logical flow
        flow_count = 0
        flow_words = ["first", "then", "next", "finally", "because", "therefore", "so", "however"]
        for word in flow_words:
            flow_count += transcript_lower.count(word)
        
        if flow_count == 0:
            score -= 2
            issues.append("Lacks logical flow indicators")
        elif flow_count >= 3:
            strengths.append("Good logical flow with transitions")
        
        score = max(0, min(10, score))
        
        return {
            "score": score,
            "issues": issues,
            "evidence": evidence,
            "strengths": strengths,
            "filler_count": filler_count,
            "sentence_count": len(sentences),
            "avg_sentence_length": round(avg_sentence_length, 1)
        }

    def calculate_enhanced_confidence_score(self, transcript: str, audio_metadata: Dict = None) -> Dict[str, Any]:
        """Calculate confidence score with voice analysis."""
        score = 10
        issues = []
        evidence = []
        strengths = []
        
        transcript_lower = transcript.lower()
        
        # Count hesitation markers
        hesitation_count = 0
        hesitation_words_found = []
        
        for marker, weight in self.hesitation_markers.items():
            count = transcript_lower.count(marker)
            if count > 0:
                hesitation_count += count * weight
                hesitation_words_found.extend([marker] * count)
        
        if hesitation_count > 5:
            score -= 3
            issues.append("Frequent hesitation markers")
            evidence.extend(hesitation_words_found[:3])
        elif hesitation_count > 2:
            score -= 1
            issues.append("Some hesitation detected")
        else:
            strengths.append("Speaks with minimal hesitation")
        
        # Check passive voice
        words = transcript_lower.split()
        passive_count = sum(1 for word in words if word in self.passive_indicators)
        passive_ratio = passive_count / len(words) if words else 0
        
        if passive_ratio > 0.2:
            score -= 2
            issues.append("Heavy use of passive voice")
        elif passive_ratio > 0.15:
            score -= 1
            issues.append("Some passive language")
        else:
            strengths.append("Uses active voice effectively")
        
        # Check confident language
        confident_count = sum(1 for word in self.confident_words if word in transcript_lower)
        if confident_count >= 3:
            strengths.append("Strong confident language")
        elif confident_count == 0:
            score -= 1
            issues.append("Lacks confident language")
        
        # Voice-based metrics (if available)
        voice_score = 0
        if audio_metadata:
            # Speaking rate analysis
            speaking_rate = audio_metadata.get('speaking_rate', 150)  # words per minute
            if speaking_rate < 100:
                voice_score -= 1
                issues.append("Speaking too slowly")
            elif speaking_rate > 180:
                voice_score -= 1
                issues.append("Speaking too quickly")
            else:
                strengths.append("Good speaking pace")
            
            # Pause analysis
            long_pauses = audio_metadata.get('long_pauses', 0)
            if long_pauses > 3:
                voice_score -= 2
                issues.append("Frequent long pauses")
            elif long_pauses <= 1:
                strengths.append("Smooth delivery with minimal pauses")
        
        score += voice_score
        score = max(0, min(10, score))
        
        return {
            "score": score,
            "issues": issues,
            "evidence": evidence,
            "strengths": strengths,
            "hesitation_count": hesitation_count,
            "passive_ratio": round(passive_ratio, 2),
            "confident_words": confident_count,
            "voice_metrics": audio_metadata or {}
        }

    def calculate_enhanced_technical_score(self, transcript: str, question_rubric: Dict = None) -> Dict[str, Any]:
        """Calculate technical score with rubric-based evaluation."""
        score = 0
        issues = []
        evidence = []
        strengths = []
        missing_concepts = []
        covered_concepts = []
        
        transcript_lower = transcript.lower()
        
        if question_rubric:
            # Must-have concepts (high weight)
            must_have = question_rubric.get('must_have_concepts', [])
            must_have_score = 0
            for concept in must_have:
                if concept.lower() in transcript_lower:
                    must_have_score += 2
                    covered_concepts.append(concept)
                else:
                    missing_concepts.append(concept)
            
            # Good-to-have concepts (medium weight)
            good_to_have = question_rubric.get('good_to_have_concepts', [])
            good_to_have_score = 0
            for concept in good_to_have:
                if concept.lower() in transcript_lower:
                    good_to_have_score += 1
                    covered_concepts.append(concept)
            
            # Red flags (negative scoring)
            red_flags = question_rubric.get('red_flags', [])
            red_flag_penalty = 0
            red_flag_found = []
            for flag in red_flags:
                if flag.lower() in transcript_lower:
                    red_flag_penalty += 2
                    red_flag_found.append(flag)
            
            # Calculate base score
            base_score = must_have_score + good_to_have_score - red_flag_penalty
            
            # Bonus for comprehensive coverage
            total_concepts = len(must_have) + len(good_to_have)
            coverage_ratio = len(covered_concepts) / total_concepts if total_concepts > 0 else 0
            
            if coverage_ratio >= 0.8:
                strengths.append("Comprehensive coverage of key concepts")
            elif coverage_ratio >= 0.6:
                strengths.append("Good coverage of main concepts")
            elif coverage_ratio < 0.4:
                issues.append("Insufficient coverage of key concepts")
            
            if missing_concepts:
                issues.append(f"Missing key concepts: {', '.join(missing_concepts[:3])}")
            
            if red_flag_found:
                issues.append(f"Potential misconceptions: {', '.join(red_flag_found)}")
            
            score = min(10, max(0, base_score))
            
        else:
            # Fallback to keyword-based scoring
            technical_keywords = [
                "hash", "bucket", "collision", "array", "linked list", "key", "value",
                "hashcode", "equals", "load factor", "capacity", "resize", "rehash",
                "time complexity", "space complexity", "o(1)", "constant time",
                "chaining", "open addressing", "tree map", "red-black tree"
            ]
            
            keyword_score = 0
            found_keywords = []
            for keyword in technical_keywords:
                if keyword in transcript_lower:
                    keyword_score += 1
                    found_keywords.append(keyword)
            
            score = min(10, keyword_score)
            evidence = found_keywords[:5]  # Show first 5 found keywords
            
            if score >= 7:
                strengths.append("Strong technical vocabulary")
            elif score >= 4:
                strengths.append("Adequate technical knowledge")
            else:
                issues.append("Limited technical terminology")
        
        return {
            "score": score,
            "issues": issues,
            "evidence": evidence,
            "strengths": strengths,
            "missing_concepts": missing_concepts,
            "covered_concepts": covered_concepts,
            "coverage_percentage": round(len(covered_concepts) / (len(missing_concepts) + len(covered_concepts)) * 100, 1) if (missing_concepts or covered_concepts) else 0
        }
