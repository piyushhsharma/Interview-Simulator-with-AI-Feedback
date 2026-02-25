import json
import random
import os
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class QuestionService:
    def __init__(self):
        self.questions = []
        self._load_questions()
    
    def _load_questions(self):
        """Load questions from JSON file."""
        try:
            questions_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
            with open(questions_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.questions = data.get('questions', [])
            logger.info(f"Loaded {len(self.questions)} questions")
        except Exception as e:
            logger.error(f"Failed to load questions: {str(e)}")
            self.questions = []
    
    def get_question_by_id(self, question_id: int) -> Optional[Dict]:
        """
        Get a specific question by ID.
        
        Args:
            question_id: The ID of the question to retrieve
            
        Returns:
            Question dictionary or None if not found
        """
        for question in self.questions:
            if question.get('id') == question_id:
                return question
        return None
    
    def get_random_question(self, category: Optional[str] = None, difficulty: Optional[str] = None) -> Optional[Dict]:
        """
        Get a random question, optionally filtered by category and/or difficulty.
        
        Args:
            category: Filter by category (Data Structures, OS, DBMS, Backend, System Design, Cloud)
            difficulty: Filter by difficulty (Easy, Medium, Hard)
            
        Returns:
            Random question dictionary or None if no questions match
        """
        if not self.questions:
            return None
        
        # Filter questions based on criteria
        filtered_questions = self.questions
        
        if category:
            filtered_questions = [q for q in filtered_questions if q.get('category') == category]
        
        if difficulty:
            filtered_questions = [q for q in filtered_questions if q.get('difficulty') == difficulty]
        
        if not filtered_questions:
            return None
        
        return random.choice(filtered_questions)
    
    def get_all_categories(self) -> List[str]:
        """Get all available categories."""
        categories = set()
        for question in self.questions:
            if 'category' in question:
                categories.add(question['category'])
        return sorted(list(categories))
    
    def get_all_difficulties(self) -> List[str]:
        """Get all available difficulty levels."""
        difficulties = set()
        for question in self.questions:
            if 'difficulty' in question:
                difficulties.add(question['difficulty'])
        return sorted(list(difficulties))
    
    def get_question_count(self, category: Optional[str] = None, difficulty: Optional[str] = None) -> int:
        """Get count of questions matching criteria."""
        count = 0
        for question in self.questions:
            category_match = not category or question.get('category') == category
            difficulty_match = not difficulty or question.get('difficulty') == difficulty
            if category_match and difficulty_match:
                count += 1
        return count
