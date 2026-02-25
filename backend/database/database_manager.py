import sqlite3
import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from models.interview_session import InterviewSession
from models.question import Question
from models.answer import Answer
from models.evaluation_result import EvaluationResult

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "interview_simulator.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create sessions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS interview_sessions (
                        session_id TEXT PRIMARY KEY,
                        created_at TEXT,
                        completed_at TEXT,
                        total_questions INTEGER,
                        completed_questions INTEGER
                    )
                ''')
                
                # Create questions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS questions (
                        id INTEGER PRIMARY KEY,
                        question TEXT NOT NULL,
                        category TEXT NOT NULL,
                        difficulty TEXT NOT NULL,
                        must_have_concepts TEXT,
                        good_to_have_concepts TEXT,
                        red_flags TEXT,
                        ideal_answer TEXT
                    )
                ''')
                
                # Create answers table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS answers (
                        answer_id TEXT PRIMARY KEY,
                        session_id TEXT,
                        question_id INTEGER,
                        transcript TEXT,
                        audio_duration REAL,
                        audio_metadata TEXT,
                        created_at TEXT,
                        FOREIGN KEY (session_id) REFERENCES interview_sessions (session_id),
                        FOREIGN KEY (question_id) REFERENCES questions (id)
                    )
                ''')
                
                # Create evaluation_results table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS evaluation_results (
                        evaluation_id TEXT PRIMARY KEY,
                        answer_id TEXT,
                        clarity_score TEXT,
                        confidence_score TEXT,
                        technical_score TEXT,
                        structure_analysis TEXT,
                        coverage_analysis TEXT,
                        overall_score REAL,
                        suggestions TEXT,
                        created_at TEXT,
                        FOREIGN KEY (answer_id) REFERENCES answers (answer_id)
                    )
                ''')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            raise
    
    def create_session(self, session: InterviewSession) -> bool:
        """Create a new interview session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO interview_sessions 
                    (session_id, created_at, completed_at, total_questions, completed_questions)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    session.session_id,
                    session.created_at.isoformat(),
                    session.completed_at.isoformat() if session.completed_at else None,
                    session.total_questions,
                    session.completed_questions
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to create session: {str(e)}")
            return False
    
    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        """Get interview session by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT session_id, created_at, completed_at, total_questions, completed_questions
                    FROM interview_sessions WHERE session_id = ?
                ''', (session_id,))
                
                row = cursor.fetchone()
                if row:
                    session = InterviewSession(
                        session_id=row[0],
                        created_at=datetime.fromisoformat(row[1]) if row[1] else None,
                        completed_at=datetime.fromisoformat(row[2]) if row[2] else None,
                        total_questions=row[3],
                        completed_questions=row[4]
                    )
                    
                    # Load answers for this session
                    session.answers = self.get_session_answers(session_id)
                    return session
                return None
        except Exception as e:
            logger.error(f"Failed to get session: {str(e)}")
            return None
    
    def update_session(self, session: InterviewSession) -> bool:
        """Update interview session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE interview_sessions 
                    SET completed_at = ?, total_questions = ?, completed_questions = ?
                    WHERE session_id = ?
                ''', (
                    session.completed_at.isoformat() if session.completed_at else None,
                    session.total_questions,
                    session.completed_questions,
                    session.session_id
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to update session: {str(e)}")
            return False
    
    def create_answer(self, answer: Answer) -> bool:
        """Create a new answer."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO answers 
                    (answer_id, session_id, question_id, transcript, audio_duration, audio_metadata, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    answer.answer_id,
                    answer.session_id,
                    answer.question_id,
                    answer.transcript,
                    answer.audio_duration,
                    json.dumps(answer.audio_metadata),
                    answer.created_at.isoformat()
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to create answer: {str(e)}")
            return False
    
    def get_session_answers(self, session_id: str) -> List[Answer]:
        """Get all answers for a session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT answer_id, session_id, question_id, transcript, audio_duration, audio_metadata, created_at
                    FROM answers WHERE session_id = ? ORDER BY created_at
                ''', (session_id,))
                
                answers = []
                for row in cursor.fetchall():
                    answer = Answer(
                        answer_id=row[0],
                        session_id=row[1],
                        question_id=row[2],
                        transcript=row[3],
                        audio_duration=row[4],
                        audio_metadata=json.loads(row[5]) if row[5] else {},
                        created_at=datetime.fromisoformat(row[6]) if row[6] else None
                    )
                    answers.append(answer)
                return answers
        except Exception as e:
            logger.error(f"Failed to get session answers: {str(e)}")
            return []
    
    def create_evaluation_result(self, evaluation: EvaluationResult) -> bool:
        """Create a new evaluation result."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO evaluation_results 
                    (evaluation_id, answer_id, clarity_score, confidence_score, technical_score, 
                     structure_analysis, coverage_analysis, overall_score, suggestions, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    evaluation.evaluation_id,
                    evaluation.answer_id,
                    json.dumps(evaluation.clarity_score),
                    json.dumps(evaluation.confidence_score),
                    json.dumps(evaluation.technical_score),
                    json.dumps(evaluation.structure_analysis),
                    json.dumps(evaluation.coverage_analysis),
                    evaluation.overall_score,
                    json.dumps(evaluation.suggestions),
                    evaluation.created_at.isoformat()
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to create evaluation result: {str(e)}")
            return False
    
    def get_evaluation_result(self, answer_id: str) -> Optional[EvaluationResult]:
        """Get evaluation result by answer ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT evaluation_id, answer_id, clarity_score, confidence_score, technical_score,
                           structure_analysis, coverage_analysis, overall_score, suggestions, created_at
                    FROM evaluation_results WHERE answer_id = ?
                ''', (answer_id,))
                
                row = cursor.fetchone()
                if row:
                    return EvaluationResult(
                        evaluation_id=row[0],
                        answer_id=row[1],
                        clarity_score=json.loads(row[2]) if row[2] else {},
                        confidence_score=json.loads(row[3]) if row[3] else {},
                        technical_score=json.loads(row[4]) if row[4] else {},
                        structure_analysis=json.loads(row[5]) if row[5] else {},
                        coverage_analysis=json.loads(row[6]) if row[6] else {},
                        overall_score=row[7],
                        suggestions=json.loads(row[8]) if row[8] else [],
                        created_at=datetime.fromisoformat(row[9]) if row[9] else None
                    )
                return None
        except Exception as e:
            logger.error(f"Failed to get evaluation result: {str(e)}")
            return None
    
    def get_session_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent session history."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT s.session_id, s.created_at, s.completed_at, s.total_questions, s.completed_questions,
                           COUNT(a.answer_id) as answer_count, AVG(er.overall_score) as avg_score
                    FROM interview_sessions s
                    LEFT JOIN answers a ON s.session_id = a.session_id
                    LEFT JOIN evaluation_results er ON a.answer_id = er.answer_id
                    GROUP BY s.session_id
                    ORDER BY s.created_at DESC
                    LIMIT ?
                ''', (limit,))
                
                history = []
                for row in cursor.fetchall():
                    history.append({
                        'session_id': row[0],
                        'created_at': row[1],
                        'completed_at': row[2],
                        'total_questions': row[3],
                        'completed_questions': row[4],
                        'answer_count': row[5],
                        'avg_score': round(row[6], 1) if row[6] else None
                    })
                return history
        except Exception as e:
            logger.error(f"Failed to get session history: {str(e)}")
            return []
