import { useState, useEffect } from 'react';

interface Question {
  id: number;
  question: string;
  options: string[];
  correctAnswer: string;
}

interface Answers {
  [key: number]: string;
}

const Quiz = () => {
  // Typing the state properly
  const [quiz, setQuiz] = useState<Question[]>([]); // Specify the type of quiz state
  const [answers, setAnswers] = useState<Answers>({}); // Typing answers as an object with numeric keys
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  useEffect(() => {
    // Simulated quiz data
    const data: Question[] = [
      {
        id: 1,
        question: 'What is the capital of France?',
        options: ['Paris', 'London', 'Berlin', 'Madrid'],
        correctAnswer: 'Paris',
      },
      {
        id: 2,
        question: 'What is 2 + 2?',
        options: ['3', '4', '5', '6'],
        correctAnswer: '4',
      },
      {
        id: 3,
        question: 'Which planet is known as the Red Planet?',
        options: ['Earth', 'Mars', 'Jupiter', 'Saturn'],
        correctAnswer: 'Mars',
      },
    ];

    setQuiz(data); // Set quiz data
  }, []);

  // Handle option change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>, questionId: number) => {
    setAnswers({
      ...answers,
      [questionId]: e.target.value,
    });
  };

  // Handle form submission and calculate score
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    let calculatedScore = 0;

    quiz.forEach((question) => {
      if (answers[question.id] === question.correctAnswer) {
        calculatedScore += 1;
      }
    });

    setScore(calculatedScore);
    setIsSubmitted(true);
  };

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-lg mt-10">
      <h2 className="text-3xl font-semibold text-center text-gray-800 mb-6">Quiz: Test Your Knowledge</h2>
      
      {quiz.length === 0 ? (
        <div className="text-center text-gray-600">Loading quiz...</div>
      ) : (
        <form onSubmit={handleSubmit}>
          {quiz.map((question) => (
            <div key={question.id} className="mb-6">
              <h3 className="text-xl font-medium text-gray-700 mb-2">{question.question}</h3>
              
              <div className="space-y-4">
                {question.options.map((option, index) => (
                  <label key={index} className="block text-gray-600">
                    <input
                      type="radio"
                      name={`question-${question.id}`}
                      value={option}
                      onChange={(e) => handleChange(e, question.id)}
                      checked={answers[question.id] === option}
                      className="mr-2 leading-tight"
                    />
                    {option}
                  </label>
                ))}
              </div>
            </div>
          ))}

          {!isSubmitted ? (
            <div className="text-center">
              <button
                type="submit"
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50"
              >
                Submit Quiz
              </button>
            </div>
          ) : (
            <div className="text-center mt-6">
              <h3 className="text-2xl font-semibold text-gray-800">You scored {score} out of {quiz.length}</h3>
              <button
                onClick={() => setIsSubmitted(false)}
                className="mt-4 px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 focus:outline-none"
              >
                Try Again
              </button>
            </div>
          )}
        </form>
      )}
    </div>
  );
};

export default Quiz;
