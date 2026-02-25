import re
from typing import Dict, List, Any, Set
import logging

logger = logging.getLogger(__name__)

class CoverageAnalyzer:
    def __init__(self):
        # Concept extraction patterns
        self.concept_patterns = {
            "technical_terms": r'\b(hash|bucket|collision|array|linked list|key|value|hashcode|equals|load factor|capacity|resize|rehash|time complexity|space complexity|o\(1\)|constant time|chaining|open addressing|tree map|red-black tree|thread safety|synchronization|concurrent)\b',
            "process_terms": r'\b(initialize|insert|delete|search|lookup|iterate|resize|rehash|collision resolution|hash function)\b',
            "performance_terms": r'\b(average case|worst case|amortized|big o|complexity|scalability|performance|efficiency|optimization)\b',
            "implementation_terms": r'\b(java|python|c\+\+|implementation|code|algorithm|data structure|class|method|function)\b'
        }

    def analyze_concept_coverage(self, transcript: str, ideal_answer: str = None, question_rubric: Dict = None) -> Dict[str, Any]:
        """Analyze how well the answer covers expected concepts."""
        transcript_lower = transcript.lower()
        
        # Extract concepts from transcript
        transcript_concepts = self._extract_concepts(transcript_lower)
        
        # Get expected concepts from rubric or ideal answer
        expected_concepts = set()
        if question_rubric:
            expected_concepts.update(question_rubric.get('must_have_concepts', []))
            expected_concepts.update(question_rubric.get('good_to_have_concepts', []))
        
        if ideal_answer:
            ideal_concepts = self._extract_concepts(ideal_answer.lower())
            expected_concepts.update(ideal_concepts)
        
        # Calculate coverage metrics
        covered_concepts = transcript_concepts.intersection(expected_concepts)
        missing_concepts = expected_concepts - transcript_concepts
        additional_concepts = transcript_concepts - expected_concepts
        
        # Coverage percentage
        coverage_percentage = 0
        if expected_concepts:
            coverage_percentage = len(covered_concepts) / len(expected_concepts) * 100
        
        # Categorize coverage
        coverage_quality = self._assess_coverage_quality(coverage_percentage, len(missing_concepts))
        
        # Generate detailed analysis
        concept_analysis = self._analyze_concept_categories(transcript_lower)
        
        # Compare with ideal answer if available
        ideal_comparison = None
        if ideal_answer:
            ideal_comparison = self._compare_with_ideal(transcript_lower, ideal_answer.lower())
        
        return {
            "coverage_percentage": round(coverage_percentage, 1),
            "covered_concepts": list(covered_concepts),
            "missing_concepts": list(missing_concepts),
            "additional_concepts": list(additional_concepts),
            "total_expected": len(expected_concepts),
            "total_covered": len(covered_concepts),
            "coverage_quality": coverage_quality,
            "concept_analysis": concept_analysis,
            "ideal_comparison": ideal_comparison,
            "suggestions": self._generate_coverage_suggestions(missing_concepts, coverage_quality)
        }

    def _extract_concepts(self, text: str) -> Set[str]:
        """Extract technical concepts from text."""
        concepts = set()
        
        # Extract using patterns
        for category, pattern in self.concept_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            concepts.update(matches)
        
        # Also extract individual words that might be concepts
        words = re.findall(r'\b[a-z]+(?:\s+[a-z]+)?\b', text)
        concepts.update(words)
        
        return concepts

    def _assess_coverage_quality(self, percentage: float, missing_count: int) -> str:
        """Assess the quality of concept coverage."""
        if percentage >= 90:
            return "excellent"
        elif percentage >= 75:
            return "very_good"
        elif percentage >= 60:
            return "good"
        elif percentage >= 40:
            return "adequate"
        elif percentage >= 25:
            return "poor"
        else:
            return "very_poor"

    def _analyze_concept_categories(self, text: str) -> Dict[str, Any]:
        """Analyze coverage by concept categories."""
        category_analysis = {}
        
        for category, pattern in self.concept_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            unique_matches = set(matches)
            
            category_analysis[category] = {
                "count": len(matches),
                "unique_concepts": len(unique_matches),
                "concepts": list(unique_matches)[:5]  # Top 5 unique concepts
            }
        
        return category_analysis

    def _compare_with_ideal(self, transcript: str, ideal: str) -> Dict[str, Any]:
        """Compare transcript with ideal answer."""
        transcript_concepts = self._extract_concepts(transcript)
        ideal_concepts = self._extract_concepts(ideal)
        
        # Calculate similarity metrics
        common_concepts = transcript_concepts.intersection(ideal_concepts)
        transcript_only = transcript_concepts - ideal_concepts
        ideal_only = ideal_concepts - transcript_concepts
        
        # Jaccard similarity
        union = transcript_concepts.union(ideal_concepts)
        jaccard_similarity = len(common_concepts) / len(union) if union else 0
        
        # Length comparison
        transcript_words = len(transcript.split())
        ideal_words = len(ideal.split())
        length_ratio = transcript_words / ideal_words if ideal_words > 0 else 0
        
        return {
            "jaccard_similarity": round(jaccard_similarity, 3),
            "length_ratio": round(length_ratio, 2),
            "common_concepts": list(common_concepts)[:10],
            "transcript_only": list(transcript_only)[:5],
            "ideal_only": list(ideal_only)[:10],
            "similarity_rating": self._rate_similarity(jaccard_similarity)
        }

    def _rate_similarity(self, jaccard_score: float) -> str:
        """Rate the similarity based on Jaccard score."""
        if jaccard_score >= 0.8:
            return "very_high"
        elif jaccard_score >= 0.6:
            return "high"
        elif jaccard_score >= 0.4:
            return "moderate"
        elif jaccard_score >= 0.2:
            return "low"
        else:
            return "very_low"

    def _generate_coverage_suggestions(self, missing_concepts: Set[str], quality: str) -> List[str]:
        """Generate suggestions based on coverage analysis."""
        suggestions = []
        
        if quality in ["very_poor", "poor"]:
            suggestions.append("Focus on covering the fundamental concepts first")
            suggestions.append("Study the core terminology and definitions")
        
        if missing_concepts:
            top_missing = list(missing_concepts)[:3]
            suggestions.append(f"Consider including: {', '.join(top_missing)}")
        
        if quality in ["adequate", "good"]:
            suggestions.append("Add more depth to your explanations")
            suggestions.append("Include real-world examples to illustrate concepts")
        
        if quality in ["very_good", "excellent"]:
            suggestions.append("Great coverage! Consider edge cases and advanced topics")
        
        return suggestions
