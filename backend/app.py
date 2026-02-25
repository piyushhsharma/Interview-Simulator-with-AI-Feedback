from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import tempfile
import os
import uuid

from services.transcription import TranscriptionService
from services.scoring import ScoringService
from services.feedback import FeedbackService
from services.question_service import QuestionService
from services.enhanced_evaluation_service import EnhancedEvaluationService
from utils.audio_utils import process_audio_file, cleanup_temp_file
from database.database_manager import DatabaseManager
from models.question import Question

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Interview Simulator API",
    description="AI-powered interview feedback system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
transcription_service = TranscriptionService()
scoring_service = ScoringService()
feedback_service = FeedbackService()
question_service = QuestionService()
enhanced_evaluation_service = EnhancedEvaluationService()
db_manager = DatabaseManager()

# Pydantic models for API
class SessionRequest(BaseModel):
    total_questions: int = 3

class TextAnswerRequest(BaseModel):
    session_id: str
    question_id: int
    answer_text: str

# Sample interview question
INTERVIEW_QUESTION = "Explain how a HashMap works internally in Java."

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "message": "Interview Simulator API",
        "version": "1.0.0",
        "endpoints": {
            "question": "/question",
            "evaluate": "/evaluate",
            "health": "/health"
        }
    }

@app.get("/api/question")
async def get_random_question(
    category: str = Query(None, description="Filter by category"),
    difficulty: str = Query(None, description="Filter by difficulty")
):
    """Get a random interview question, optionally filtered by category and difficulty."""
    try:
        question = question_service.get_random_question(category, difficulty)
        
        if not question:
            raise HTTPException(
                status_code=404, 
                detail="No questions found matching the criteria"
            )
        
        return {
            "question": question["question"],
            "category": question["category"],
            "difficulty": question["difficulty"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching question: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch question")

@app.get("/question")
async def get_question():
    """Get the interview question (legacy endpoint for backward compatibility)."""
    try:
        question = question_service.get_random_question()
        
        if not question:
            # Fallback to hardcoded question if service fails
            return {
                "question": "Explain how a HashMap works internally in Java.",
                "category": "Data Structures",
                "difficulty": "Medium"
            }
        
        return {
            "question": question["question"],
            "category": question["category"],
            "difficulty": question["difficulty"]
        }
    except Exception as e:
        logger.error(f"Error fetching question: {str(e)}")
        # Fallback to hardcoded question
        return {
            "question": "Explain how a HashMap works internally in Java.",
            "category": "Data Structures",
            "difficulty": "Medium"
        }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "services": "running"}

@app.post("/evaluate")
async def evaluate_answer(audio: UploadFile = File(...), session_id: str = None, question_id: int = None):
    """
    Evaluate interview answer from audio file.
    
    Args:
        audio: Audio file containing the interview answer
        session_id: Optional session ID for tracking
        question_id: Optional question ID for rubric-based evaluation
        
    Returns:
        Complete feedback with transcript, scores, and suggestions
    """
    temp_audio_path = None
    
    try:
        # Validate audio file
        if not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Read audio bytes
        audio_bytes = await audio.read()
        
        if len(audio_bytes) == 0:
            raise HTTPException(status_code=400, detail="Audio file is empty")
        
        # Process audio file
        temp_audio_path = process_audio_file(audio_bytes)
        
        # Transcribe audio
        transcript = transcription_service.transcribe_audio(temp_audio_path)
        
        if not transcript:
            raise HTTPException(status_code=500, detail="Transcription failed")
        
        if len(transcript.strip()) < 10:
            raise HTTPException(status_code=400, detail="Transcript too short - please speak more clearly")
        
        # Get question data if question_id provided
        question = None
        if question_id:
            question_data = question_service.get_question_by_id(question_id)
            if question_data:
                question = Question.from_dict(question_data)
        
        # Create answer record
        answer = Answer(
            session_id=session_id,
            question_id=question_id,
            transcript=transcript
        )
        
        # Store answer in database
        if not db_manager.create_answer(answer):
            logger.warning("Failed to store answer in database")
        
        # Enhanced evaluation
        evaluation = enhanced_evaluation_service.evaluate_answer(answer, question, temp_audio_path)
        
        # Store evaluation result
        if not db_manager.create_evaluation_result(evaluation):
            logger.warning("Failed to store evaluation result in database")
        
        # Update session if provided
        if session_id:
            session = db_manager.get_session(session_id)
            if session:
                session.completed_questions += 1
                db_manager.update_session(session)
        
        # Return enhanced feedback
        return JSONResponse(content=evaluation.to_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Evaluation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
    
    finally:
        # Clean up temporary files
        if temp_audio_path:
            cleanup_temp_file(temp_audio_path)

# Session management endpoints
@app.post("/api/session/create")
async def create_session(request: SessionRequest):
    """Create a new interview session."""
    try:
        from models.interview_session import InterviewSession
        session = InterviewSession(total_questions=request.total_questions)
        
        if db_manager.create_session(session):
            return {"session_id": session.session_id, "total_questions": session.total_questions}
        else:
            raise HTTPException(status_code=500, detail="Failed to create session")
    except Exception as e:
        logger.error(f"Session creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create session")

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get session details."""
    try:
        session = db_manager.get_session(session_id)
        if session:
            return session.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get session")

@app.post("/api/evaluate/text")
async def evaluate_text_answer(request: TextAnswerRequest):
    """Evaluate text-based answer (fallback for audio issues)."""
    try:
        # Get question data
        question = None
        question_data = question_service.get_question_by_id(request.question_id)
        if question_data:
            question = Question.from_dict(question_data)
        
        # Create answer record
        from models.answer import Answer
        answer = Answer(
            session_id=request.session_id,
            question_id=request.question_id,
            transcript=request.answer_text
        )
        
        # Store answer in database
        if not db_manager.create_answer(answer):
            logger.warning("Failed to store answer in database")
        
        # Enhanced evaluation (without audio)
        evaluation = enhanced_evaluation_service.evaluate_answer(answer, question)
        
        # Store evaluation result
        if not db_manager.create_evaluation_result(evaluation):
            logger.warning("Failed to store evaluation result in database")
        
        # Update session
        session = db_manager.get_session(request.session_id)
        if session:
            session.completed_questions += 1
            db_manager.update_session(session)
        
        return JSONResponse(content=evaluation.to_dict())
        
    except Exception as e:
        logger.error(f"Text evaluation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Evaluation failed")

@app.get("/api/history")
async def get_history(limit: int = 10):
    """Get interview session history."""
    try:
        history = db_manager.get_session_history(limit)
        return {"history": history}
    except Exception as e:
        logger.error(f"Failed to get history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get history")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
