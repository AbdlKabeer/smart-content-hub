import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../context/authContext';

// Types
interface CategoryObject {
  id: string;
  name: string;
  slug: string;
}

interface Tag {
  id: string;
  name: string;
}

interface QuizQuestion {
  id: string;
  text: string;
  options: {
    id: string;
    text: string;
  }[];
  correctOptionId: string;
  explanation?: string;
}

interface QuizFormData {
  title: string;
  description: string;
  category_id: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  estimatedTime: number;
  tags: string[];
  questions: QuizQuestion[];
}

const AdminQuizUploadPage: React.FC = () => {
  const navigate = useNavigate();
  const { fetchWithAuth, displayNotification } = useAuth();

  const [availableTags, setAvailableTags] = useState<Tag[]>([]);
  const [availableCategories, setAvailableCategories] = useState<CategoryObject[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  
  // State for form data
  const [formData, setFormData] = useState<QuizFormData>({
    title: '',
    description: '',
    category_id: '',
    difficulty: 'Medium',
    estimatedTime: 20,
    tags: [],
    questions: []
  });
  
  // State for the current question being edited
  const [currentQuestion, setCurrentQuestion] = useState<QuizQuestion>({
    id: '',
    text: '',
    options: [
      { id: 'a', text: '' },
      { id: 'b', text: '' },
      { id: 'c', text: '' },
      { id: 'd', text: '' }
    ],
    correctOptionId: '',
    explanation: ''
  });
  
  // Add state to control question form visibility
  const [showQuestionForm, setShowQuestionForm] = useState<boolean>(false);
  
  // Fetch tags and categories on component mount
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        await Promise.all([fetchTags(), fetchCategories()]);
      } catch (error) {
        displayNotification?.( 'error','Error loading data. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);
  
  // Handle form field changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  // Handle question field changes
  const handleQuestionChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setCurrentQuestion(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  // Handle option field changes
  const handleOptionChange = (optionId: string, value: string) => {
    setCurrentQuestion(prev => ({
      ...prev,
      options: prev.options.map(option => 
        option.id === optionId ? { ...option, text: value } : option
      )
    }));
  };
  
  // Handle correct option selection
  const handleCorrectOptionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCurrentQuestion(prev => ({
      ...prev,
      correctOptionId: e.target.value
    }));
  };

  async function fetchTags() {
    try {
      const data = await fetchWithAuth({
        method: 'GET',
        path: `/admin/tags/`,
      });
      setAvailableTags(data);
    } catch (error) {
      console.error('Error fetching tags:', error);
      throw error;
    }
  }

  async function fetchCategories() {
    try {
      const data = await fetchWithAuth({
        method: 'GET',
        path: `/admin/categories/`,
      });
      setAvailableCategories(data);
    } catch (error) {
      console.error('Error fetching categories:', error);
      throw error;
    }
  }
  
  // Show the question form
  const handleShowQuestionForm = () => {
    setShowQuestionForm(true);
  };
  
  // Cancel adding a question
  const handleCancelQuestion = () => {
    setShowQuestionForm(false);
    setCurrentQuestion({
      id: '',
      text: '',
      options: [
        { id: 'a', text: '' },
        { id: 'b', text: '' },
        { id: 'c', text: '' },
        { id: 'd', text: '' }
      ],
      correctOptionId: '',
      explanation: ''
    });
  };
  
  // Add question to quiz
  const handleAddQuestion = () => {
    // Validate question
    if (!currentQuestion.text || 
        currentQuestion.options.some(opt => !opt.text) || 
        !currentQuestion.correctOptionId) {
      displayNotification?.( 'error','Please fill in all question fields and select a correct answer.');
      return;
    }
    
    // Create unique ID for the question
    const questionId = currentQuestion.id || `q${formData.questions.length + 1}`;
    
    // Add question to form data
    setFormData(prev => ({
      ...prev,
      questions: [...prev.questions, { ...currentQuestion, id: questionId }]
    }));
    
    // Reset current question form
    setCurrentQuestion({
      id: '',
      text: '',
      options: [
        { id: 'a', text: '' },
        { id: 'b', text: '' },
        { id: 'c', text: '' },
        { id: 'd', text: '' }
      ],
      correctOptionId: '',
      explanation: ''
    });
    
    // Hide the question form after adding
    setShowQuestionForm(false);
  };
  
  // Remove question from quiz
  const handleRemoveQuestion = (questionId: string) => {
    setFormData(prev => ({
      ...prev,
      questions: prev.questions.filter(q => q.id !== questionId)
    }));
  };
  
  // Edit existing question
  const handleEditQuestion = (questionId: string) => {
    const questionToEdit = formData.questions.find(q => q.id === questionId);
    if (questionToEdit) {
      setCurrentQuestion(questionToEdit);
      setFormData(prev => ({
        ...prev,
        questions: prev.questions.filter(q => q.id !== questionId)
      }));
      setShowQuestionForm(true);
    }
  };
  
  // Select tag from available tags
  const handleSelectTag = (tagId: string) => {
    if (!formData.tags.includes(tagId)) {
      setFormData(prev => ({
        ...prev,
        tags: [...prev.tags, tagId]
      }));
    }
  };
  
  // Remove tag
  const handleRemoveTag = (tagId: string) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.filter(t => t !== tagId)
    }));
  };
  
  // Add a new state variable for form submission loading
  const [submitting, setSubmitting] = useState<boolean>(false);

  // Modify the handleSubmit function
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate form
    if (!formData.title || !formData.description || !formData.category_id || formData.questions.length === 0) {
      displayNotification?.( 'error','Please fill in all required fields and add at least one question.');
      return;
    }

    // Validate that estimatedTime is set
    if (!formData.estimatedTime) {
      displayNotification?.( 'error','Please set an estimated time for the quiz.');
      return;
    }
    
    // Set submitting state to true
    setSubmitting(true);
    
    try {
      // Create a copy of the data for submission
      const submissionData = {
        ...formData,
        // Make sure these fields are explicitly included
        estimatedTime: formData.estimatedTime,
        tags: formData.tags, // The serializer will handle this
      };
      
      console.log('Submitting quiz data:', submissionData);
      
      await fetchWithAuth({
        method: 'POST',
        path: '/admin/quizzes/',
        body: submissionData
      });
      
      displayNotification?.( 'success','Quiz successfully created!');
      navigate('/admin/quiz-list');
    } catch (error: any) {
      console.error('Error creating quiz:', error);
      let errorMessage = 'Error creating quiz. Please try again.';
      if (error.response?.data) {
        errorMessage += ' ' + JSON.stringify(error.response.data);
      }
      displayNotification?.( 'error',errorMessage);
    } finally {
      // Reset submitting state
      setSubmitting(false);
    }
  };
  
  // Get tag name by id
  const getTagName = (tagId: string) => {
    const tag = availableTags.find(t => t.id === tagId);
    return tag ? tag.name : tagId;
  };
  
  return (
    <div className="max-w-5xl mx-auto p-6 bg-gray-50 min-h-screen">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Create New Quiz</h1>
        <p className="text-gray-600">Fill in the details below to create a new quiz.</p>
      </div>
      
      {loading ? (
        <div className="text-center py-8">
          <p>Loading...</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Quiz Basic Information */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-bold mb-4">Quiz Information</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                  Title *
                </label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  className="w-full p-2 border border-gray-300 rounded-md"
                  required
                />
              </div>
              
              <div>
                <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
                  Category *
                </label>
                <select
                  id="category"
                  name="category_id"
                  value={formData.category_id}
                  onChange={handleInputChange}
                  className="w-full p-2 border border-gray-300 rounded-md"
                  required
                >
                  <option value="">Select a category</option>
                  {availableCategories.map(category => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label htmlFor="difficulty" className="block text-sm font-medium text-gray-700 mb-1">
                  Difficulty *
                </label>
                <select
                  id="difficulty"
                  name="difficulty"
                  value={formData.difficulty}
                  onChange={handleInputChange}
                  className="w-full p-2 border border-gray-300 rounded-md"
                  required
                >
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>
              
              <div>
                <label htmlFor="estimatedTime" className="block text-sm font-medium text-gray-700 mb-1">
                  Estimated Time (minutes) *
                </label>
                <input
                  type="number"
                  id="estimatedTime"
                  name="estimatedTime"
                  value={formData.estimatedTime}
                  onChange={handleInputChange}
                  min="5"
                  max="120"
                  className="w-full p-2 border border-gray-300 rounded-md"
                  required
                />
              </div>
            </div>
            
            <div className="mt-4">
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                Description *
              </label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows={3}
                className="w-full p-2 border border-gray-300 rounded-md"
                required
              />
            </div>
            
            {/* Tags */}
            <div className="mt-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tags
              </label>
              <div className="flex flex-wrap gap-2 mb-2">
                {availableTags.map(tag => (
                  <button
                    key={tag.id}
                    type="button"
                    onClick={() => handleSelectTag(tag.id)}
                    className={`px-2 py-1 text-xs rounded-full ${
                      formData.tags.includes(tag.id)
                        ? 'bg-indigo-500 text-white'
                        : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
                    }`}
                  >
                    {tag.name}
                  </button>
                ))}
              </div>
              
              {formData.tags.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-1">Selected Tags:</p>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {formData.tags.map(tagId => (
                      <span 
                        key={tagId} 
                        className="px-2 py-1 bg-indigo-100 text-indigo-800 text-xs rounded-full flex items-center"
                      >
                        {getTagName(tagId)}
                        <button
                          type="button"
                          onClick={() => handleRemoveTag(tagId)}
                          className="ml-1 text-indigo-600 hover:text-indigo-800"
                        >
                          &times;
                        </button>
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
          
          {/* Questions Section */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Questions</h2>
              {!showQuestionForm && (
                <button
                  type="button"
                  onClick={handleShowQuestionForm}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                >
                  Add Question
                </button>
              )}
            </div>
            
            {/* Question Editor - Only show when button is clicked */}
            {showQuestionForm && (
              <div className="border border-gray-200 rounded-lg p-4 mb-6">
                <h3 className="text-lg font-medium mb-3">
                  {currentQuestion.id ? 'Edit Question' : 'Add New Question'}
                </h3>
                
                <div className="mb-4">
                  <label htmlFor="question-text" className="block text-sm font-medium text-gray-700 mb-1">
                    Question Text *
                  </label>
                  <textarea
                    id="question-text"
                    name="text"
                    value={currentQuestion.text}
                    onChange={handleQuestionChange}
                    rows={2}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    placeholder="Enter your question here..."
                    required
                  />
                </div>
                
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Options *
                  </label>
                  <div className="space-y-3">
                    {currentQuestion.options.map(option => (
                      <div key={option.id} className="flex items-center">
                        <input
                          type="radio"
                          id={`option-${option.id}`}
                          name="correctOption"
                          value={option.id}
                          checked={currentQuestion.correctOptionId === option.id}
                          onChange={handleCorrectOptionChange}
                          className="mr-2"
                        />
                        <label htmlFor={`option-${option.id}`} className="mr-2 w-8">
                          {option.id.toUpperCase()}.
                        </label>
                        <input
                          type="text"
                          value={option.text}
                          onChange={(e) => handleOptionChange(option.id, e.target.value)}
                          className="flex-grow p-2 border border-gray-300 rounded-md"
                          placeholder={`Option ${option.id.toUpperCase()}`}
                          required
                        />
                      </div>
                    ))}
                  </div>
                  <p className="text-sm text-gray-500 mt-1">
                    Select the radio button next to the correct answer.
                  </p>
                </div>
                
                <div className="mb-4">
                  <label htmlFor="explanation" className="block text-sm font-medium text-gray-700 mb-1">
                    Explanation (Optional)
                  </label>
                  <textarea
                    id="explanation"
                    name="explanation"
                    value={currentQuestion.explanation || ''}
                    onChange={handleQuestionChange}
                    rows={2}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    placeholder="Explain why the correct answer is right (shown after answering)"
                  />
                </div>
                
                <div className="flex justify-end space-x-2">
                  <button
                    type="button"
                    onClick={handleCancelQuestion}
                    className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    onClick={handleAddQuestion}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                  >
                    {currentQuestion.id ? 'Update Question' : 'Add Question'}
                  </button>
                </div>
              </div>
            )}
            
            {/* Question List */}
            {formData.questions.length > 0 ? (
              <div className="border border-gray-200 rounded-lg divide-y">
                {formData.questions.map((question, index) => (
                  <div key={question.id} className="p-4 hover:bg-gray-50">
                    <div className="flex justify-between items-start">
                      <div className="flex-grow">
                        <div className="font-medium mb-1">
                          Question {index + 1}: {question.text}
                        </div>
                        <div className="text-sm text-gray-600 ml-4">
                          {question.options.map(option => (
                            <div key={option.id} className="flex items-center">
                              <span className={`w-6 ${option.id === question.correctOptionId ? 'font-bold text-green-600' : ''}`}>
                                {option.id.toUpperCase()}.
                              </span>
                              <span>{option.text}</span>
                              {option.id === question.correctOptionId && (
                                <span className="ml-2 text-xs text-green-600">✓ Correct</span>
                              )}
                            </div>
                          ))}
                        </div>
                        {question.explanation && (
                          <div className="text-sm text-gray-600 mt-2">
                            <span className="font-medium">Explanation:</span> {question.explanation}
                          </div>
                        )}
                      </div>
                      <div className="flex space-x-2">
                        <button
                          type="button"
                          onClick={() => handleEditQuestion(question.id)}
                          className="text-indigo-600 hover:text-indigo-800"
                        >
                          Edit
                        </button>
                        <button
                          type="button"
                          onClick={() => handleRemoveQuestion(question.id)}
                          className="text-red-600 hover:text-red-800"
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 border border-dashed border-gray-300 rounded-lg">
                <p className="text-gray-500">No questions added yet. Click "Add Question" to begin.</p>
              </div>
            )}
          </div>
          
          {/* Submit Button */}
          <div className="flex justify-end">
            <button
              type="button"
              onClick={() => navigate('/admin/quiz-list')}
              className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md mr-2 hover:bg-gray-50"
              disabled={submitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className={`px-6 py-2 ${formData.questions.length === 0 ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'} text-white rounded-md flex items-center`}
              disabled={formData.questions.length === 0 || submitting}
            >
              {submitting ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Submitting...
                </>
              ) : (
                'Create Quiz'
              )}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default AdminQuizUploadPage;