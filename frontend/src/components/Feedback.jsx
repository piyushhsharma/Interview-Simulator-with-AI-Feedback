import React from 'react';
import { CheckCircle2, XCircle, AlertCircle, TrendingUp, MessageSquare, Lightbulb } from 'lucide-react';

const Feedback = ({ feedback }) => {
  if (!feedback) return null;

  const getScoreClass = (score) => {
    if (score >= 8) return 'score-excellent';
    if (score >= 6) return 'score-good';
    if (score >= 4) return 'score-average';
    return 'score-poor';
  };

  const getScoreIcon = (score) => {
    if (score >= 8) return <CheckCircle2 className="w-4 h-4" />;
    if (score >= 6) return <AlertCircle className="w-4 h-4" />;
    return <XCircle className="w-4 h-4" />;
  };

  const getScoreLabel = (score) => {
    if (score >= 8) return 'Excellent';
    if (score >= 6) return 'Good';
    if (score >= 4) return 'Average';
    return 'Needs Improvement';
  };

  const ScoreCard = ({ title, score, feedback_text, icon: Icon }) => (
    <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-2">
          <Icon className="w-5 h-5 text-gray-600" />
          <h4 className="font-semibold text-gray-800">{title}</h4>
        </div>
        <div className="flex items-center space-x-2">
          <span className={`font-bold text-lg ${getScoreClass(score)}`}>
            {score}/10
          </span>
          {getScoreIcon(score)}
        </div>
      </div>
      <div className="mb-2">
        <span className={`text-xs font-medium ${getScoreClass(score)}`}>
          {getScoreLabel(score)}
        </span>
      </div>
      <p className="text-sm text-gray-600 leading-relaxed">
        {feedback_text}
      </p>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Transcript Section */}
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <MessageSquare className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-800">Your Answer Transcript</h3>
        </div>
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {feedback.transcript}
          </p>
        </div>
      </div>

      {/* Scores Section */}
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <TrendingUp className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-800">Performance Scores</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <ScoreCard
            title="Clarity"
            score={feedback.scores.clarity}
            feedback_text={feedback.feedback.clarity}
            icon={MessageSquare}
          />
          <ScoreCard
            title="Confidence"
            score={feedback.scores.confidence}
            feedback_text={feedback.feedback.confidence}
            icon={TrendingUp}
          />
          <ScoreCard
            title="Technical"
            score={feedback.scores.technical_correctness}
            feedback_text={feedback.feedback.technical_correctness}
            icon={CheckCircle2}
          />
        </div>

        {/* Overall Score */}
        <div className="mt-6 p-4 bg-primary-50 rounded-lg border border-primary-200">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-semibold text-primary-900">Overall Score</h4>
              <p className="text-sm text-primary-700">Average of all three metrics</p>
            </div>
            <div className="text-center">
              <div className={`text-3xl font-bold ${getScoreClass(
                Math.round((feedback.scores.clarity + feedback.scores.confidence + feedback.scores.technical_correctness) / 3)
              )}`}>
                {Math.round((feedback.scores.clarity + feedback.scores.confidence + feedback.scores.technical_correctness) / 3)}/10
              </div>
              <span className={`text-sm font-medium ${getScoreClass(
                Math.round((feedback.scores.clarity + feedback.scores.confidence + feedback.scores.technical_correctness) / 3)
              )}`}>
                {getScoreLabel(Math.round((feedback.scores.clarity + feedback.scores.confidence + feedback.scores.technical_correctness) / 3))}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Suggestions Section */}
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <Lightbulb className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-800">Improvement Suggestions</h3>
        </div>
        
        <div className="space-y-3">
          {feedback.suggestions.map((suggestion, index) => (
            <div key={index} className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-medium">
                {index + 1}
              </div>
              <p className="text-gray-700 leading-relaxed flex-1">
                {suggestion}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Feedback;
