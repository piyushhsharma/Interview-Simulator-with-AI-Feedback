import React from 'react';
import { CheckCircle2, XCircle, AlertCircle, TrendingUp, MessageSquare, Lightbulb, Target, BarChart3, FileText, Brain } from 'lucide-react';

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

  const EnhancedScoreCard = ({ title, scoreData, icon: Icon }) => {
    const score = scoreData.score || 0;
    const issues = scoreData.issues || [];
    const strengths = scoreData.strengths || [];
    const evidence = scoreData.evidence || [];

    return (
      <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
        <div className="flex items-center justify-between mb-3">
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

        {/* Strengths */}
        {strengths.length > 0 && (
          <div className="mb-2">
            <div className="text-xs font-medium text-green-700 mb-1">Strengths:</div>
            <div className="space-y-1">
              {strengths.map((strength, index) => (
                <div key={index} className="text-xs text-green-600 flex items-start">
                  <CheckCircle2 className="w-3 h-3 mr-1 mt-0.5 flex-shrink-0" />
                  {strength}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Issues */}
        {issues.length > 0 && (
          <div className="mb-2">
            <div className="text-xs font-medium text-red-700 mb-1">Issues:</div>
            <div className="space-y-1">
              {issues.map((issue, index) => (
                <div key={index} className="text-xs text-red-600 flex items-start">
                  <XCircle className="w-3 h-3 mr-1 mt-0.5 flex-shrink-0" />
                  {issue}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Evidence */}
        {evidence.length > 0 && (
          <div>
            <div className="text-xs font-medium text-gray-700 mb-1">Evidence:</div>
            <div className="flex flex-wrap gap-1">
              {evidence.map((item, index) => (
                <span key={index} className="text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded">
                  {item}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

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
          <h3 className="text-lg font-semibold text-gray-800">Performance Analysis</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <EnhancedScoreCard
            title="Clarity"
            scoreData={feedback.clarity_score || {}}
            icon={MessageSquare}
          />
          <EnhancedScoreCard
            title="Confidence"
            scoreData={feedback.confidence_score || {}}
            icon={TrendingUp}
          />
          <EnhancedScoreCard
            title="Technical"
            scoreData={feedback.technical_score || {}}
            icon={Brain}
          />
        </div>

        {/* Overall Score */}
        <div className="mt-6 p-4 bg-primary-50 rounded-lg border border-primary-200">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-semibold text-primary-900">Overall Score</h4>
              <p className="text-sm text-primary-700">Weighted average of all metrics</p>
            </div>
            <div className="text-center">
              <div className={`text-3xl font-bold ${getScoreClass(feedback.overall_score || 0)}`}>
                {feedback.overall_score || 0}/10
              </div>
              <span className={`text-sm font-medium ${getScoreClass(feedback.overall_score || 0)}`}>
                {getScoreLabel(feedback.overall_score || 0)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Structure Analysis */}
      {feedback.structure_analysis && (
        <div className="card">
          <div className="flex items-center space-x-2 mb-4">
            <Target className="w-5 h-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-800">Answer Structure Analysis</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Structure Components</h4>
              <div className="space-y-2">
                {Object.entries(feedback.structure_analysis.structure_detected || {}).map(([component, detected]) => (
                  <div key={component} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 capitalize">{component}</span>
                    <span className={`text-xs px-2 py-1 rounded ${
                      detected ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}>
                      {detected ? 'Present' : 'Missing'}
                    </span>
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Structure Quality</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Structure Score</span>
                  <span className={`font-medium ${getScoreClass(feedback.structure_analysis.structure_score || 0)}`}>
                    {feedback.structure_analysis.structure_score || 0}/10
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Logical Flow</span>
                  <span className="text-sm text-gray-700 capitalize">
                    {feedback.structure_analysis.logical_flow || 'unknown'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Total Sentences</span>
                  <span className="text-sm text-gray-700">
                    {feedback.structure_analysis.total_sentences || 0}
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          {feedback.structure_analysis.issues && feedback.structure_analysis.issues.length > 0 && (
            <div className="mt-4">
              <h4 className="font-medium text-gray-700 mb-2">Structure Issues</h4>
              <div className="space-y-1">
                {feedback.structure_analysis.issues.map((issue, index) => (
                  <div key={index} className="text-sm text-red-600 flex items-start">
                    <XCircle className="w-3 h-3 mr-1 mt-0.5 flex-shrink-0" />
                    {issue}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Coverage Analysis */}
      {feedback.coverage_analysis && (
        <div className="card">
          <div className="flex items-center space-x-2 mb-4">
            <BarChart3 className="w-5 h-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-800">Concept Coverage Analysis</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-700">
                {feedback.coverage_analysis.coverage_percentage || 0}%
              </div>
              <div className="text-sm text-green-600">Coverage</div>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-700">
                {feedback.coverage_analysis.total_covered || 0}
              </div>
              <div className="text-sm text-blue-600">Concepts Covered</div>
            </div>
            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-700">
                {feedback.coverage_analysis.total_expected || 0}
              </div>
              <div className="text-sm text-orange-600">Expected Concepts</div>
            </div>
          </div>
          
          {feedback.coverage_analysis.missing_concepts && feedback.coverage_analysis.missing_concepts.length > 0 && (
            <div className="mb-4">
              <h4 className="font-medium text-gray-700 mb-2">Missing Concepts</h4>
              <div className="flex flex-wrap gap-2">
                {feedback.coverage_analysis.missing_concepts.map((concept, index) => (
                  <span key={index} className="text-sm bg-red-100 text-red-700 px-3 py-1 rounded-full">
                    {concept}
                  </span>
                ))}
              </div>
            </div>
          )}
          
          {feedback.coverage_analysis.covered_concepts && feedback.coverage_analysis.covered_concepts.length > 0 && (
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Covered Concepts</h4>
              <div className="flex flex-wrap gap-2">
                {feedback.coverage_analysis.covered_concepts.map((concept, index) => (
                  <span key={index} className="text-sm bg-green-100 text-green-700 px-3 py-1 rounded-full">
                    {concept}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

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
