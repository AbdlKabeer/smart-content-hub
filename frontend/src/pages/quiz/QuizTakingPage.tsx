import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../../context/authContext';

// Types
interface Option {
  id: string;
  text: string;
}

interface QuizQuestion {
  id: string;
  text: string;
  options: Option[];
  correctOptionId: string;
  explanation?: string;
}

interface CategoryObject {
  id: string;
  name: string;
  slug: string;
}

interface Tag {
  id: string;
  name: string;
}

interface Quiz {
  id: string;
  title: string;
  description: string;
  category: CategoryObject | string;
  level?: 'Easy' | 'Medium' | 'Hard';
  estimated_time?: number;
  tags?: string[] | Tag[];
  created_at?: string;
  questions: QuizQuestion[];
  difficulty?: 'Easy' | 'Medium' | 'Hard';
}

const QuizTakingPage: React.FC = () => {
  const { fetchWithAuth } = useAuth();
  const { id } = useParams<{ id: string }>();
  
  // State
  const [loading, setLoading] = useState(true);
  const [quiz, setQuiz] = useState<Quiz>({
    id: '',
    title: '',
    description: '',
    category: '',
    difficulty: 'Medium',
    questions: [ ]
  });
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOptions, setSelectedOptions] = useState<Record<string, string>>({});
  const [showResults, setShowResults] = useState(false);
  const [timeLeft, setTimeLeft] = useState(30 * 60); // 30 minutes in seconds
  const [isPaused, setIsPaused] = useState(false);

  async function fetchQuizData() {
    setLoading(true);
    try {
      const data = await fetchWithAuth({
        method: 'GET',
        path: `/admin/quizzes/${id}/`,
      });
      
      // Transform the API response to our form format
      setQuiz(data);
    } catch (error) {
      console.error('Error fetching quiz data:', error);
    } finally {
      setLoading(false);
    }
  }

  // Timer effect
  useEffect(() => {
    if (isPaused || showResults) return;
    
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          setShowResults(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    
    return () => clearInterval(timer);
  }, [isPaused, showResults]);

  // Fetch quiz data on component mount
  useEffect(() => {
    if (id) {
      fetchQuizData();
    }
  }, [id]);

  // Format time as MM:SS
  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  // Get category name
  const getCategoryName = () => {
    if (typeof quiz.category === 'string') {
      return quiz.category;
    }
    return quiz.category.name;
  };

  // Get formatted tags
  const getFormattedTags = () => {
    if (!quiz.tags || quiz.tags.length === 0) return null;
    
    if (typeof quiz.tags[0] === 'string') {
      return (quiz.tags as string[]);
    } else {
      return (quiz.tags as Tag[]).map(tag => tag.name);
    }
  };

  // Current question
  const currentQuestion = quiz.questions[currentQuestionIndex];

  // Progress percentage
  const progressPercentage = (Object.keys(selectedOptions).length / quiz.questions.length) * 100;

  // Calculate score
  const calculateScore = () => {
    let correct = 0;
    quiz.questions.forEach(question => {
      if (selectedOptions[question.id] === question.correctOptionId) {
        correct++;
      }
    });
    return {
      correct,
      total: quiz.questions.length,
      percentage: Math.round((correct / quiz.questions.length) * 100)
    };
  };

  // Handle option selection
  const handleOptionSelect = (questionId: string, optionId: string) => {
    if (showResults) return;
    
    setSelectedOptions(prev => ({
      ...prev,
      [questionId]: optionId
    }));
  };

  // Handle navigation
  const goToNextQuestion = () => {
    if (currentQuestionIndex < quiz.questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const goToPrevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  // Finish quiz
  const handleFinishQuiz = () => {
    setShowResults(true);
  };

  // Start new attempt
  const handleStartNewAttempt = () => {
    setSelectedOptions({});
    setCurrentQuestionIndex(0);
    setShowResults(false);
    setTimeLeft(30 * 60);
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6 bg-gray-50 min-h-screen flex flex-col items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600 mb-4"></div>
        <p className="text-gray-600">Loading quiz...</p>
      </div>
    );
  }

  const tags = getFormattedTags();

  return (
    <div className="max-w-4xl mx-auto p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 pb-4 border-b">
        <div>
          <h1 className="text-2xl font-bold">{quiz.title}</h1>
          <div className="text-sm text-gray-500 mt-1">
            {getCategoryName()} • {quiz.difficulty}
          </div>
          
          {/* Tags */}
          {tags && tags.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-2">
              {tags.map((tag, index) => (
                <span 
                  key={index} 
                  className="px-2 py-1 bg-indigo-100 text-indigo-800 text-xs rounded-full"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
          
          {/* Description */}
          {quiz.description && (
            <div className="mt-3 text-sm text-gray-700">
              {quiz.description}
            </div>
          )}
        </div>
        <div className="mt-4 md:mt-0 flex items-center">
          <div className="flex items-center mr-4">
            <svg className="w-5 h-5 text-gray-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="font-mono text-lg">{formatTime(timeLeft)}</span>
          </div>
          <button 
            className="px-3 py-1 text-sm border border-gray-300 rounded text-gray-700 hover:bg-gray-100"
            onClick={() => setIsPaused(!isPaused)}
          >
            {isPaused ? 'Resume' : 'Pause'}
          </button>
        </div>
      </div>
      
      {/* Progress bar */}
      <div className="w-full h-2 bg-gray-200 rounded-full mb-8">
        <div 
          className="h-2 bg-indigo-600 rounded-full"
          style={{ width: `${progressPercentage}%` }}
        ></div>
      </div>
      
      {!showResults ? (
        <>
          {/* Question */}
          <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
            <div className="mb-6">
              <div className="text-sm text-gray-500 mb-2">
                Question {currentQuestionIndex + 1} of {quiz.questions.length}
              </div>
              <h2 className="text-xl font-bold">{currentQuestion?.text}</h2>
            </div>
            
            {/* Options */}
            <div className="space-y-3">
              {currentQuestion?.options.map(option => (
                <div 
                  key={option.id}
                  className={`p-4 border rounded-lg cursor-pointer transition ${
                    selectedOptions[currentQuestion.id] === option.id
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => handleOptionSelect(currentQuestion.id, option.id)}
                >
                  <div className="flex items-center">
                    <div className={`w-5 h-5 mr-3 rounded-full flex items-center justify-center border ${
                      selectedOptions[currentQuestion.id] === option.id
                        ? 'border-indigo-500 bg-indigo-500'
                        : 'border-gray-300'
                    }`}>
                      {selectedOptions[currentQuestion.id] === option.id && (
                        <div className="w-2 h-2 rounded-full bg-white"></div>
                      )}
                    </div>
                    <span>{option.text}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Navigation */}
          <div className="flex justify-between">
            <button
              onClick={goToPrevQuestion}
              className={`px-4 py-2 border border-gray-300 rounded ${
                currentQuestionIndex === 0 ? 'text-gray-400 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-50'
              }`}
              disabled={currentQuestionIndex === 0}
            >
              Previous
            </button>
            
            {currentQuestionIndex < quiz?.questions.length - 1 ? (
              <button
                onClick={goToNextQuestion}
                className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
              >
                Next
              </button>
            ) : (
              <button
                onClick={handleFinishQuiz}
                className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                disabled={Object.keys(selectedOptions).length < quiz.questions.length}
              >
                Finish Quiz
              </button>
            )}
          </div>
          
          {/* Question navigator */}
          <div className="mt-10">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Question Navigation</h3>
            <div className="flex flex-wrap gap-2">
              {quiz?.questions.map((question, index) => (
                <button
                  key={question.id}
                  onClick={() => setCurrentQuestionIndex(index)}
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm ${
                    index === currentQuestionIndex
                      ? 'bg-indigo-600 text-white'
                      : selectedOptions[question.id]
                        ? 'bg-indigo-100 text-indigo-800'
                        : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {index + 1}
                </button>
              ))}
            </div>
          </div>
        </>
      ) : (
        /* Results page */
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold mb-2">Quiz Complete!</h2>
            <p className="text-gray-600">Here's how you did</p>
          </div>
          
          {/* Score */}
          <div className="flex justify-center mb-10">
            <div className="w-48 h-48 relative">
              <svg className="w-full h-full" viewBox="0 0 100 100">
                {/* Background circle */}
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  fill="none"
                  stroke="#e5e7eb"
                  strokeWidth="10"
                />
                {/* Score circle */}
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  fill="none"
                  stroke={calculateScore().percentage >= 70 ? "#4ade80" : calculateScore().percentage >= 40 ? "#fbbf24" : "#ef4444"}
                  strokeWidth="10"
                  strokeDasharray={`${2 * Math.PI * 45 * calculateScore().percentage / 100} ${2 * Math.PI * 45 * (1 - calculateScore().percentage / 100)}`}
                  strokeDashoffset={2 * Math.PI * 45 * 0.25}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-4xl font-bold">{calculateScore().percentage}%</span>
                <span className="text-sm text-gray-500">{calculateScore().correct}/{calculateScore().total} correct</span>
              </div>
            </div>
          </div>
          
          {/* Question review */}
          <div className="space-y-8">
            <h3 className="text-xl font-bold">Question Review</h3>
            
            {quiz?.questions.map((question, index) => (
              <div key={question.id} className="border rounded-lg overflow-hidden">
                <div className="p-4 bg-gray-50 border-b">
                  <div className="flex justify-between items-start">
                    <span className="font-medium">Question {index + 1}</span>
                    <span className={`text-sm px-2 py-1 rounded-full ${
                      selectedOptions[question.id] === question.correctOptionId
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {selectedOptions[question.id] === question.correctOptionId ? 'Correct' : 'Incorrect'}
                    </span>
                  </div>
                  <p className="mt-2">{question.text}</p>
                </div>
                
                <div className="p-4">
                  {question?.options.map(option => (
                    <div 
                      key={option.id}
                      className={`p-3 my-2 rounded-lg ${
                        option.id === question.correctOptionId
                          ? 'bg-green-100 border border-green-200'
                          : selectedOptions[question.id] === option.id && option.id !== question.correctOptionId
                            ? 'bg-red-100 border border-red-200'
                            : 'bg-gray-50 border border-gray-200'
                      }`}
                    >
                      <div className="flex items-center">
                        <div className={`w-5 h-5 mr-3 rounded-full flex items-center justify-center ${
                          option.id === question.correctOptionId
                            ? 'bg-green-500'
                            : selectedOptions[question.id] === option.id && option.id !== question.correctOptionId
                              ? 'bg-red-500'
                              : 'border border-gray-300'
                        }`}>
                          {(option.id === question.correctOptionId || 
                            (selectedOptions[question.id] === option.id && option.id !== question.correctOptionId)) && (
                            <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                              {option.id === question.correctOptionId ? (
                                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                              ) : (
                                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                              )}
                            </svg>
                          )}
                        </div>
                        <span>{option.text}</span>
                      </div>
                    </div>
                  ))}
                </div>
                
                {/* Explanation */}
                {question?.explanation && (
                  <div className="p-4 bg-blue-50 border-t border-blue-100">
                    <h4 className="text-sm font-medium text-blue-800 mb-1">Explanation</h4>
                    <p className="text-blue-900">{question.explanation}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
          
          {/* Actions */}
          <div className="mt-8 flex justify-center">
            <button
              onClick={handleStartNewAttempt}
              className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium"
            >
              Start New Attempt
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default QuizTakingPage;