import React, { useState, useEffect, useRef } from 'react';

// Types
interface Option {
  id: number;
  option_id: string;
  text: string;
  is_correct: boolean;
}

interface QuizQuestion {
  id: number;
  text: string;
  options: Option[];
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
  category: CategoryObject;
  level: 'Easy' | 'Medium' | 'Hard';
  estimated_time: number;
  tags?: Tag[];
  created_at: string;
  questions: QuizQuestion[];
}

interface PreviewQuizProps {
  quiz: Quiz;
  closeModal: () => void;
}

const PreviewQuiz: React.FC<PreviewQuizProps> = ({ quiz, closeModal }) => {
  // State
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOptions, setSelectedOptions] = useState<Record<number, string>>({});
  const [showResults, setShowResults] = useState(false);
  const [timeLeft, setTimeLeft] = useState(quiz.estimated_time * 60); // Convert minutes to seconds
  const [isPaused, setIsPaused] = useState(false);

  const modalRef = useRef<HTMLDivElement | null>(null);

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

  // Close modal when clicked outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(event.target as Node)) {
        closeModal();
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [closeModal]);

  // Format time as MM:SS
  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  // Current question
  const currentQuestion = quiz.questions[currentQuestionIndex];

  // Progress percentage
  const progressPercentage = (Object.keys(selectedOptions).length / quiz.questions.length) * 100;

  // Find correct option ID for a question
  const getCorrectOptionId = (question: QuizQuestion): string => {
    const correctOption = question.options.find(option => option.is_correct);
    return correctOption ? correctOption.option_id : '';
  };

  // Calculate score
  const calculateScore = () => {
    let correct = 0;
    quiz.questions.forEach(question => {
      const correctOptionId = getCorrectOptionId(question);
      if (selectedOptions[question.id] === correctOptionId) {
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
  const handleOptionSelect = (questionId: number, optionId: string) => {
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
    setTimeLeft(quiz.estimated_time * 60);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div ref={modalRef} className="bg-white rounded-lg max-w-4xl w-full max-h-90vh overflow-y-auto p-4">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 pb-4 border-b">
          <div>
            <h1 className="text-2xl font-bold">{quiz.title}</h1>
            <div className="text-sm text-gray-500 mt-1">{quiz.category.name} • {quiz.level}</div>
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
            <button
              onClick={closeModal}
              className="ml-4 px-3 py-1 text-sm border border-gray-300 rounded text-gray-700 hover:bg-gray-100"
            >
              Close
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
              <h2 className="text-xl font-bold">{currentQuestion.text}</h2>
            </div>
            
            {/* Options */}
            <div className="space-y-3">
              {currentQuestion.options.map(option => (
                <div 
                  key={option.id}
                  className={`p-4 border rounded-lg cursor-pointer transition ${
                    selectedOptions[currentQuestion.id] === option.option_id
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => handleOptionSelect(currentQuestion.id, option.option_id)}
                >
                  <div className="flex items-center">
                    <div className={`w-5 h-5 mr-3 rounded-full flex items-center justify-center border ${
                      selectedOptions[currentQuestion.id] === option.option_id
                        ? 'border-indigo-500 bg-indigo-500'
                        : 'border-gray-300'
                    }`}>
                      {selectedOptions[currentQuestion.id] === option.option_id && (
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
            
            {currentQuestionIndex < quiz.questions.length - 1 ? (
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
              {quiz.questions.map((question, index) => (
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
            
            {quiz.questions.map((question, index) => {
              const correctOptionId = getCorrectOptionId(question);
              return (
              <div key={question.id} className="border rounded-lg overflow-hidden">
                <div className="p-4 bg-gray-50 border-b">
                  <div className="flex justify-between items-start">
                    <span className="font-medium">Question {index + 1}</span>
                    <span className={`text-sm px-2 py-1 rounded-full ${
                      selectedOptions[question.id] === correctOptionId
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {selectedOptions[question.id] === correctOptionId ? 'Correct' : 'Incorrect'}
                    </span>
                  </div>
                  <p className="mt-2">{question.text}</p>
                </div>
                
                <div className="p-4">
                  {question.options.map(option => (
                    <div 
                      key={option.id}
                      className={`p-3 my-2 rounded-lg ${
                        selectedOptions[question.id] === option.option_id
                          ? selectedOptions[question.id] === correctOptionId
                            ? 'bg-green-50'
                            : 'bg-red-50'
                          : option.is_correct
                            ? 'bg-green-50'
                            : ''
                      }`}
                    >
                      <div className="flex items-center">
                        <span
                          className={`w-4 h-4 mr-3 rounded-full border ${
                            selectedOptions[question.id] === option.option_id
                              ? selectedOptions[question.id] === correctOptionId
                                ? 'border-green-500 bg-green-500'
                                : 'border-red-500 bg-red-500'
                              : option.is_correct
                                ? 'border-green-500 bg-green-500'
                                : 'border-gray-300'
                          }`}
                        />
                        <span>{option.text}</span>
                      </div>
                    </div>
                  ))}
                  <div className="mt-3 text-sm text-gray-500">
                    {question.explanation && <p><strong>Explanation:</strong> {question.explanation}</p>}
                  </div>
                </div>
              </div>
            )})}
          </div>
          
          <div className="mt-8 text-center">
            <button
              onClick={handleStartNewAttempt}
              className="px-6 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
            >
              Start New Attempt
            </button>
          </div>
        </div>
      )}
      </div>
    </div>
  );
};

export default PreviewQuiz;