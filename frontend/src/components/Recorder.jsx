import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Loader2, Clock } from 'lucide-react';

const Recorder = ({ onRecordingComplete, isProcessing }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [error, setError] = useState('');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      setError('');
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        onRecordingComplete(audioBlob);
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

    } catch (err) {
      setError('Microphone access denied. Please allow microphone access to record your answer.');
      console.error('Error accessing microphone:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="card max-w-md mx-auto">
      <div className="text-center">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">
          Record Your Answer
        </h3>
        
        {error && (
          <div className="mb-4 p-3 bg-danger-50 border border-danger-200 rounded-lg text-danger-700 text-sm">
            {error}
          </div>
        )}

        <div className="mb-6">
          {!isRecording && !isProcessing && (
            <button
              onClick={startRecording}
              className="btn-primary relative group"
            >
              <Mic className="w-5 h-5 mr-2" />
              Start Recording
              <div className="absolute inset-0 rounded-lg bg-primary-700 opacity-0 group-hover:opacity-20 transition-opacity" />
            </button>
          )}

          {isRecording && (
            <button
              onClick={stopRecording}
              className="bg-danger-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-danger-600 transition-colors duration-200 shadow-lg recording-pulse"
            >
              <MicOff className="w-5 h-5 mr-2" />
              Stop Recording
            </button>
          )}

          {isProcessing && (
            <button disabled className="bg-gray-400 text-white px-6 py-3 rounded-lg font-medium cursor-not-allowed">
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              Processing...
            </button>
          )}
        </div>

        {isRecording && (
          <div className="space-y-2">
            <div className="flex items-center justify-center space-x-2 text-gray-600">
              <Clock className="w-4 h-4" />
              <span className="font-mono text-lg">{formatTime(recordingTime)}</span>
            </div>
            <div className="text-sm text-gray-500">
              Recording in progress... Speak clearly and concisely.
            </div>
          </div>
        )}

        {!isRecording && !isProcessing && (
          <div className="text-sm text-gray-500 space-y-1">
            <p>Click "Start Recording" to begin your answer.</p>
            <p>Try to speak for 1-3 minutes for best results.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Recorder;
