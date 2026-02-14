import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Brain, RefreshCw, FileText, Settings } from 'lucide-react';
import Recorder from './components/Recorder';
import Feedback from './components/Feedback';

function App() {
  const [question, setQuestion] = useState('');
  const [category, setCategory] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuestion();
  }, []);

  const fetchQuestion = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/question');
      setQuestion(response.data.question);
      setCategory(response.data.category);
      setDifficulty(response.data.difficulty);
      setError('');
    } catch (err) {
      setError('Failed to load question. Please refresh the page.');
      console.error('Error fetching question:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRecordingComplete = async (audioBlob) => {
    setIsProcessing(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.wav');

      const response = await axios.post('/evaluate', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000, // 60 second timeout
      });

      setFeedback(response.data);
      setError('');
    } catch (err) {
      if (err.response) {
        setError(err.response.data.detail || 'Failed to process your answer. Please try again.');
      } else if (err.code === 'ECONNABORTED') {
        setError('Processing took too long. Please try a shorter answer.');
      } else {
        setError('Network error. Please check your connection and try again.');
      }
      console.error('Error processing audio:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  const resetInterview = () => {
    setFeedback(null);
    setError('');
  };

  const getOverallScore = () => {
    if (!feedback) return null;
    return Math.round(
      (feedback.scores.clarity + feedback.scores.confidence + feedback.scores.technical_correctness) / 3
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-primary-600 p-2 rounded-lg">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Interview Simulator</h1>
                <p className="text-sm text-gray-600">AI-Powered Technical Interview Practice</p>
              </div>
            </div>
            <button
              onClick={fetchQuestion}
              disabled={loading || isProcessing}
              className="btn-secondary flex items-center space-x-2"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              <span>New Question</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-danger-50 border border-danger-200 rounded-lg text-danger-700">
            <div className="flex items-center space-x-2">
              <Settings className="w-5 h-5" />
              <span className="font-medium">Error:</span>
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Question Section */}
        <div className="mb-8">
          <div className="card">
            <div className="flex items-center space-x-2 mb-4">
              <FileText className="w-5 h-5 text-primary-600" />
              <h2 className="text-xl font-semibold text-gray-800">Interview Question</h2>
            </div>
            
            {loading ? (
              <div className="text-center py-8">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                <p className="mt-2 text-gray-600">Loading question...</p>
              </div>
            ) : (
              <div className="bg-primary-50 rounded-lg p-6 border border-primary-200">
                <p className="text-lg text-gray-800 leading-relaxed font-medium">
                  {question}
                </p>
                <div className="mt-4 flex items-center space-x-4 text-sm text-gray-600">
                  <span className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full font-medium">
                    {category}
                  </span>
                  <span className={`px-3 py-1 rounded-full font-medium ${
                    difficulty === 'Easy' ? 'bg-success-100 text-success-700' :
                    difficulty === 'Medium' ? 'bg-warning-100 text-warning-700' :
                    'bg-danger-100 text-danger-700'
                  }`}>
                    {difficulty} Difficulty
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Recording or Feedback Section */}
        {!feedback ? (
          <Recorder 
            onRecordingComplete={handleRecordingComplete} 
            isProcessing={isProcessing}
          />
        ) : (
          <div>
            {/* Results Header */}
            <div className="mb-6 text-center">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Your Interview Results</h2>
              <div className="flex items-center justify-center space-x-4">
                <div className="text-center">
                  <div className="text-4xl font-bold text-primary-600">{getOverallScore()}/10</div>
                  <div className="text-sm text-gray-600">Overall Score</div>
                </div>
              </div>
            </div>

            {/* Feedback Display */}
            <Feedback feedback={feedback} />

            {/* Action Buttons */}
            <div className="mt-8 text-center">
              <button
                onClick={resetInterview}
                className="btn-primary mr-4"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Try Again
              </button>
              <button
                onClick={fetchQuestion}
                className="btn-secondary"
              >
                <FileText className="w-4 h-4 mr-2" />
                Next Question
              </button>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="text-center text-sm text-gray-600">
            <p>Interview Simulator with AI Feedback • Practice technical interviews with real-time analysis</p>
            <p className="mt-1">Built with React, FastAPI, and OpenAI Whisper</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
