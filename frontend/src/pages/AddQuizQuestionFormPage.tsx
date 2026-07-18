// @ts-nocheck
import { useState, useEffect } from 'react';
import { useAuth } from '../context/authContext';

interface Course {
    id: string;
    title: string;
}

interface Question {
    question_text: string;
    answers: string[];
    correctAnswer: string;
}

export default function AddQuizQuestionFormPage() {
    const { fetchWithAuth, displayNotification } = useAuth();

    // State for the quiz title, description, and course
    const [quizTitle, setQuizTitle] = useState('');
    const [quizDescription, setQuizDescription] = useState('');
    const [selectedCourse, setSelectedCourse] = useState<string>('');  // Fixed type to string
    const [courses] = useState<Course[]>([]); // To hold list of courses for selection

    // State for all questions
    const [questions, setQuestions] = useState<Question[]>([{
        question_text: '',
        answers: ['', '', '', ''],
        correctAnswer: ''
    }]);

    // State for modal visibility
    const [isModalOpen, setIsModalOpen] = useState(false);

    async function fetchCourses() {
        try {
            // const data = await fetchWithAuth({
            //     method: 'GET',
            //     path: `/account/courses-without-quiz`,
            // });

            // Filter courses to only include those with has_quiz: false
            // const filteredCourses = data?.data.filter(course => course.has_quiz === false);
            // setCourses(filteredCourses);
        } catch (error) {
            console.error('Error fetching courses:', error);
            displayNotification("error", "Failed to fetch courses.");
        }
    }

    // Fetch courses on component mount (assuming an API or context for available courses)
    useEffect(() => {
        fetchCourses();
    }, [displayNotification]);

    // Handle changes to individual question fields
    const handleQuestionChange = (index: number, field: keyof Question, value: string) => {
        const updatedQuestions = [...questions];
        updatedQuestions[index][field] = value;
        setQuestions(updatedQuestions);
    };

    // Handle changes to answers
    const handleAnswerChange = (index: number, answerIndex: number, value: string) => {
        const updatedQuestions = [...questions];
        updatedQuestions[index].answers[answerIndex] = value;
        setQuestions(updatedQuestions);
    };

    // Add a new question (only if current question is valid)
    const handleAddQuestion = () => {
        const currentQuestion = questions[questions.length - 1];
        if (currentQuestion.question_text && currentQuestion.answers.every(ans => ans) && currentQuestion.correctAnswer) {
            setQuestions([...questions, { question_text: '', answers: ['', '', '', ''], correctAnswer: '' }]);
        } else {
            displayNotification("error", 'Please fill in all fields of the current question before adding another.');
        }
    };

    // Submit all questions
    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();

        // Validate that at least one question is filled and all are valid
        if (!quizTitle || !quizDescription || !selectedCourse) {
            displayNotification("error", 'Please fill in the quiz title, description, and course before submitting.');
            return;
        }

        if (questions.length === 0 || questions.some(({ question_text, answers, correctAnswer }) => !question_text || answers.some((answer) => !answer) || !correctAnswer)) {
            displayNotification("error", 'Please fill in at least one complete question.');
            return;
        }

        // Prepare quiz data
        const quizData = {
            title: quizTitle,
            description: quizDescription,
            course: selectedCourse,
            questions: questions.map(({ question_text, answers, correctAnswer }) => ({
                question_text,
                answers,
                correct_answer: correctAnswer
            }))
        };

        try {
            const data = await fetchWithAuth({
                method: 'POST',
                path: `/quizzes`,
                body: quizData
            });

            displayNotification('success', data?.detail);

        } catch (error) {
            console.error('Error fetching user profile:', error);
        }
    };

    // Handle preview modal toggle
    const handlePreview = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    return (
        <>
            <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-lg dark:bg-boxdark">
                <h1 className="text-2xl font-semibold text-gray-800 dark:text-white mb-6">Add New Quiz Questions</h1>
                <form onSubmit={handleSubmit}>
                    {/* Quiz Title and Description */}
                    <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-700 dark:text-white mb-2">Quiz Title</label>
                        <input
                            type="text"
                            value={quizTitle}
                            onChange={(e) => setQuizTitle(e.target.value)}
                            placeholder="Enter quiz title"
                            className="w-full p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary"
                            required
                        />
                    </div>

                    <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-700 dark:text-white mb-2">Quiz Description</label>
                        <textarea
                            value={quizDescription}
                            onChange={(e) => setQuizDescription(e.target.value)}
                            placeholder="Enter quiz description"
                            className="w-full p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary"
                            required
                        />
                    </div>

                    {/* Quiz Course Selection */}
                    <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-700 dark:text-white mb-2">Select Course</label>
                        <select
                            value={selectedCourse}
                            onChange={(e) => setSelectedCourse(e.target.value)}
                            className="w-full p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary"
                            required
                        >
                            <option value="" disabled>Select a course</option>
                            {courses.map((course) => (
                                <option key={course.id} value={course.id}>
                                    {course.title}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Questions Section */}
                    {questions.map((questionData, index) => (
                        <div key={index} className="mb-6 border-b pb-4">
                            <div className="mb-4">
                                <label className="block text-sm font-medium text-gray-700 dark:text-white mb-2">Question {index + 1}</label>
                                <input
                                    type="text"
                                    value={questionData.question_text}
                                    onChange={(e) => handleQuestionChange(index, 'question_text', e.target.value)}
                                    placeholder="Enter the question"
                                    className="w-full p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary"
                                    required
                                />
                            </div>

                            <div className="mb-4">
                                <label className="block text-sm font-medium text-gray-700 dark:text-white mb-2">Answers</label>
                                {questionData.answers.map((answer, answerIndex) => (
                                    <div key={answerIndex} className="mb-2">
                                        <input
                                            type="text"
                                            value={answer}
                                            onChange={(e) => handleAnswerChange(index, answerIndex, e.target.value)}
                                            placeholder={`Answer ${answerIndex + 1}`}
                                            className="w-full p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary"
                                            required
                                        />
                                    </div>
                                ))}
                            </div>

                            <div className="mb-4">
                                <label className="block text-sm font-medium text-gray-700 dark:text-white mb-2">Correct Answer</label>
                                <select
                                    value={questionData.correctAnswer}
                                    onChange={(e) => handleQuestionChange(index, 'correctAnswer', e.target.value)}
                                    className="w-full p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary"
                                    required
                                >
                                    <option value="" disabled>Select correct answer</option>
                                    {questionData.answers.map((answer, answerIndex) => (
                                        <option key={answerIndex} value={answer}>
                                            Answer {answerIndex + 1}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>
                    ))}

                    <div className="flex justify-between mb-6">
                        <button
                            type="button"
                            onClick={handleAddQuestion}
                            className="text-primary hover:underline"
                            disabled={!(questions[questions.length - 1].question_text && questions[questions.length - 1].answers.every(ans => ans) && questions[questions.length - 1].correctAnswer)}
                        >
                            Add Another Question
                        </button>
                        <button
                            type="button"
                            onClick={handlePreview}
                            className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary-dark"
                        >
                            Preview
                        </button>
                    </div>

                    <button
                        type="submit"
                        className="w-full bg-primary text-white p-3 rounded-lg hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-primary dark:bg-primary dark:hover:bg-primary-dark dark:focus:ring-primary"
                    >
                        Submit Quiz
                    </button>
                </form>
            </div>

            {/* Preview Modal */}
            {isModalOpen && (
                <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 z-50">
                    <div className="bg-white p-6 rounded-lg shadow-lg max-w-xl w-full">
                        <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-4">Preview Quiz</h2>
                        <div className="space-y-4">
                            <p className="font-medium text-lg text-gray-700 dark:text-white">Quiz Title: {quizTitle}</p>
                            <p className="text-gray-600 dark:text-gray-400">Description: {quizDescription}</p>
                            <p className="text-gray-600 dark:text-gray-400">Course: {courses.find(course => course.id === selectedCourse)?.title}</p>
                            {questions.map((questionData, index) => (
                                <div key={index} className="border-b pb-4">
                                    <p className="font-medium text-lg text-gray-700 dark:text-white">{questionData.question_text}</p>
                                    {questionData.answers.map((answer, answerIndex) => (
                                        <p key={answerIndex} className="text-gray-600 dark:text-gray-400">
                                            {answerIndex + 1}. {answer}
                                        </p>
                                    ))}
                                    <p className="text-primary mt-2">Correct Answer: {questionData.correctAnswer}</p>
                                </div>
                            ))}
                        </div>
                        <div className="mt-4 flex justify-end space-x-4">
                            <button onClick={handleCloseModal} className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400">Close</button>
                            <button onClick={handleSubmit} className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary-dark">Submit</button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
