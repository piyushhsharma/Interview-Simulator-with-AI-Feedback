# Interview Simulator with AI Feedback

A production-grade interview preparation platform that provides real-time AI feedback on technical interview answers. Built with React, FastAPI, and OpenAI Whisper for speech-to-text processing.

## 🎯 Overview

This application helps students practice technical interviews by:
- Recording spoken interview answers
- Transcribing speech to text using Whisper
- Evaluating answers on clarity, confidence, and technical correctness
- Providing structured, explainable feedback with actionable suggestions

## 🏗️ Architecture

```
┌─────────────────┐    HTTP     ┌─────────────────┐
│   React App     │ ◄─────────► │   FastAPI       │
│   (Frontend)    │             │   (Backend)     │
│                 │             │                 │
│ - Audio Recording│             │ - Transcription │
│ - UI Components │             │ - Scoring       │
│ - Feedback      │             │ - Feedback      │
└─────────────────┘             └─────────────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │   Whisper       │
                               │   (Speech-to-   │
                               │    Text)        │
                               └─────────────────┘
```

## 📁 Project Structure

```
interview-simulator/
│
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── services/
│   │   ├── transcription.py   # Whisper speech-to-text
│   │   ├── scoring.py         # AI evaluation logic
│   │   └── feedback.py        # Feedback generation
│   └── utils/
│       └── audio_utils.py     # Audio processing utilities
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── components/
│   │   │   ├── Recorder.jsx  # Audio recording component
│   │   │   └── Feedback.jsx   # Feedback display component
│   │   └── index.css         # Tailwind CSS styles
│   ├── package.json          # Node.js dependencies
│   └── tailwind.config.js    # Tailwind configuration
│
└── README.md
```

## 🧠 AI Evaluation System

### Scoring Categories

#### 1️⃣ Clarity Score (0–10)
Evaluates communication quality:
- **Sentence Structure**: Complete sentences vs fragments
- **Filler Words**: Count of "uh", "um", "like", etc.
- **Logical Flow**: Use of transition words and organization

#### 2️⃣ Confidence Score (0–10)
Measures delivery and assurance:
- **Hesitation**: Markers like "I think", "maybe", "well"
- **Passive Language**: Overuse of passive voice
- **Substance vs Length**: Meaningful content vs verbosity

#### 3️⃣ Technical Correctness (0–10)
Assesses technical accuracy:
- **Keyword Presence**: HashMap-specific terminology
- **Concept Accuracy**: Correct explanation of internals
- **Explanation Depth**: Coverage of edge cases and trade-offs

### Feedback Output Example

```json
{
  "transcript": "A HashMap in Java uses an array of buckets...",
  "scores": {
    "clarity": 7,
    "confidence": 6,
    "technical_correctness": 8
  },
  "feedback": {
    "clarity": "Your explanation was structured but contained filler words.",
    "confidence": "You hesitated while defining key concepts.",
    "technical_correctness": "Correctly explained time complexity but missed edge cases."
  },
  "suggestions": [
    "Reduce filler words",
    "Add real-world examples",
    "Explain trade-offs"
  ]
}
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- Microphone access

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server**
   ```bash
   uvicorn app:app --reload
   ```

   Backend will run on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the frontend**
   ```bash
   npm start
   ```

   Frontend will run on `http://localhost:3000`

## 🎮 How to Use

1. **Open the application** at `http://localhost:3000`
2. **Read the interview question** (currently: "Explain how a HashMap works internally in Java")
3. **Click "Start Recording"** and record your answer (1-3 minutes recommended)
4. **Click "Stop Recording"** when finished
5. **Wait for processing** (AI transcribes and evaluates your answer)
6. **Review your feedback** including:
   - Full transcript of your answer
   - Scores for clarity, confidence, and technical correctness
   - Detailed feedback for each category
   - Actionable improvement suggestions

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **OpenAI Whisper**: State-of-the-art speech-to-text
- **Librosa**: Audio processing
- **PyTorch**: Deep learning framework for Whisper

### Frontend
- **React 18**: Modern UI framework
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client for API calls

## 📊 Sample Interview Question

**Current Question**: "Explain how a HashMap works internally in Java."

**Expected Key Points**:
- Hash function and hashcode calculation
- Bucket array structure
- Collision handling (chaining with linked lists)
- Load factor and resizing
- Time complexity analysis (O(1) average case)
- Java 8+ optimizations (tree bins for large buckets)

## 🔧 Development Notes

### Adding New Questions
Questions are hardcoded in `backend/app.py`. To add more questions:

```python
QUESTIONS = [
    "Explain how a HashMap works internally in Java.",
    "What is the difference between ArrayList and LinkedList?",
    # Add more questions here
]
```

### Customizing Scoring
Modify the scoring logic in `backend/services/scoring.py`:
- Update `technical_keywords` for new topics
- Adjust scoring weights and thresholds
- Add new evaluation criteria

### Extending Feedback
Enhance feedback generation in `backend/services/feedback.py`:
- Add new suggestion categories
- Implement more sophisticated feedback logic
- Include additional metrics

## 🎯 Quality Bar

This project demonstrates:
- **Production-ready code** with proper error handling
- **Explainable AI** with transparent scoring logic
- **Modern UI/UX** with responsive design
- **Scalable architecture** with modular services
- **No vendor lock-in** using open-source technologies

## 📈 Resume Bullet Points

- **Built an AI-powered interview simulator** using React, FastAPI, and OpenAI Whisper
- **Implemented explainable AI scoring system** evaluating clarity, confidence, and technical accuracy
- **Designed real-time speech-to-text processing** with structured feedback generation
- **Created responsive UI with audio recording** and comprehensive analytics dashboard
- **Deployed full-stack application** with modular microservices architecture

## 🐛 Troubleshooting

### Common Issues

1. **Microphone not working**
   - Check browser permissions
   - Ensure HTTPS (localhost is exempt)
   - Try different browser

2. **Whisper model download fails**
   - Check internet connection
   - Ensure sufficient disk space (~2GB for base model)
   - Try running backend again after download completes

3. **Frontend can't connect to backend**
   - Ensure both services are running
   - Check ports: backend on 8000, frontend on 3000
   - Verify CORS configuration in `app.py`

4. **Audio processing is slow**
   - First-time Whisper download takes time
   - Consider using smaller model for faster processing
   - Check system resources

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ for interview preparation**