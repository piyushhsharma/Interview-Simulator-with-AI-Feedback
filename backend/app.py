from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import tempfile
import os

from services.transcription import TranscriptionService
from services.scoring import ScoringService
from services.feedback import FeedbackService
from utils.audio_utils import process_audio_file, cleanup_temp_file

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

@app.get("/question")
async def get_question():
    """Get the interview question."""
    return {
        "question": INTERVIEW_QUESTION,
        "category": "Data Structures",
        "difficulty": "Medium"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "services": "running"}

@app.post("/evaluate")
async def evaluate_answer(audio: UploadFile = File(...)):
    """
    Evaluate interview answer from audio file.
    
    Args:
        audio: Audio file containing the interview answer
        
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
        
        # Calculate scores
        scores_data = scoring_service.calculate_all_scores(transcript)
        
        # Generate complete feedback
        feedback = feedback_service.generate_complete_feedback(transcript, scores_data)
        
        logger.info(f"Successfully evaluated answer: {len(transcript)} characters transcribed")
        
        return JSONResponse(content=feedback)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Evaluation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
    
    finally:
        # Clean up temporary files
        if temp_audio_path:
            cleanup_temp_file(temp_audio_path)

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
