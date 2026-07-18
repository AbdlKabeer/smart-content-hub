// @ts-nocheck
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import PreviewQuiz from '../../../components/admin/quiz/PreviewQuiz';
import { useAuth } from '../../../context/authContext';

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

// Updated Quiz interface to match API response
interface Quiz {
  id: string;
  title: string;
  description: string;
  category: CategoryObject;
  level: 'Easy' | 'Medium' | 'Hard';
  estimated_time: number;
  tags?: string[] | Tag[]; // Update to handle both string[] and Tag[] types
  created_at: string;
  questions: QuizQuestion[];
}

interface ApiResponse {
  metadata: {
    count: number;
    is_filter: boolean;
    has_records: boolean;
    page_size: number;
    page: number;
    next: string | null;
    previous: string | null;
  };
  results: Quiz[];
}

const QuizListingPage: React.FC = () => {
  const { fetchWithAuth, displayNotification } = useAuth();
  // State
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [filteredQuizzes, setFilteredQuizzes] = useState<Quiz[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [difficultyFilter, setDifficultyFilter] = useState<string>('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [availableTags, setAvailableTags] = useState<Tag[]>([]);
  const [showPreviewModal, setShowPreviewModal] = useState(false);
  const [selectedQuiz, setSelectedQuiz] = useState<Quiz | null>(null);
  const [availableCategories, setAvailableCategories] = useState<CategoryObject[]>([]);

  async function fetchTags() {
    try {
      const data = await fetchWithAuth({
        method: 'GET',
        path: `/admin/tags/`,
      });
      setAvailableTags(data);
    } catch (error) {
      console.error('Error fetching tags:', error);
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
    }
  }

  async function fetchQuizzes() {
    try {
      const data: ApiResponse = await fetchWithAuth({
        method: 'GET',
        path: `/admin/quizzes/`,
      });
      
      // Process the quiz data to ensure tags are in a consistent format
      const processedQuizzes = data.results.map(quiz => {
        // Ensure tags are always in a consistent format (array of string IDs)
        const processedTags = Array.isArray(quiz.tags) 
          ? quiz.tags.map(tag => typeof tag === 'string' ? tag : tag.id)
          : [];
        
        return {
          ...quiz,
          tags: processedTags
        };
      });
      
      setQuizzes(processedQuizzes);
      setFilteredQuizzes(processedQuizzes);
    } catch (error) {
      console.error('Error fetching quizzes:', error);
      displayNotification("error", "Failed to fetch quizzes.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    fetchQuizzes();
    fetchTags();
    fetchCategories();
  }, []);

  // Apply filters
  useEffect(() => {
    let result = quizzes;

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      result = result.filter(quiz => 
        quiz.title.toLowerCase().includes(term) || 
        quiz.description.toLowerCase().includes(term) ||
        quiz.category.name.toLowerCase().includes(term)
      );
    }

    // Apply difficulty filter
    if (difficultyFilter) {
      result = result.filter(quiz => quiz.level === difficultyFilter);
    }

    // Apply tag filters - Fixed to work with array of tag IDs
    if (selectedTags.length > 0) {
      result = result.filter(quiz => 
        quiz.tags && quiz.tags.some(tagId => selectedTags.includes(tagId))
      );
    }

    setFilteredQuizzes(result);
  }, [quizzes, searchTerm, difficultyFilter, selectedTags]);

  // Handle tag selection
  const toggleTag = (tagId: string) => {
    setSelectedTags(prev => 
      prev.includes(tagId)
        ? prev.filter(t => t !== tagId)
        : [...prev, tagId]
    );
  };

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    }).format(date);
  };

  // Handle quiz preview
  const openPreviewModal = (quiz: Quiz) => {
    setSelectedQuiz(quiz);
    setShowPreviewModal(true);
  };

  const closeModal = () => {
    setShowPreviewModal(false);
    setSelectedQuiz(null);
  };

  // Clear all filters
  const clearFilters = () => {
    setSearchTerm('');
    setDifficultyFilter('');
    setSelectedTags([]);
  };

  // Function to get tag name from id (for display purposes)
  const getTagName = (tagId: string) => {
    const tag = availableTags.find(t => t.id === tagId);
    return tag ? tag.name : tagId;
  };

  return (
    <div className="max-w-7xl mx-auto p-6 bg-gray-50 min-h-screen">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">Quiz Library</h1>
          <p className="text-gray-600 mt-1">Browse and filter available quizzes</p>
        </div>
        <div className="mt-4 md:mt-0">
          <Link 
            to="/admin/quiz-create" 
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Create New Quiz
          </Link>
        </div>
      </div>

      {/* Filters section */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
              Search
            </label>
            <input
              type="text"
              id="search"
              placeholder="Search by title, description, or category"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label htmlFor="difficulty" className="block text-sm font-medium text-gray-700 mb-1">
              Difficulty
            </label>
            <select
              id="difficulty"
              value={difficultyFilter}
              onChange={(e) => setDifficultyFilter(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">All Levels</option>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          <div className="md:col-span-1 flex items-end">
            <button
              onClick={clearFilters}
              className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
            >
              Clear Filters
            </button>
          </div>
        </div>

        {/* Tags filter */}
        <div className="mt-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Filter by Tags
          </label>
          <div className="flex flex-wrap gap-2">
            {availableTags.map(tag => (
              <button
                key={tag.id}
                onClick={() => toggleTag(tag.id)}
                className={`px-3 py-1 rounded-full text-sm ${
                  selectedTags.includes(tag.id)
                    ? 'bg-indigo-100 text-indigo-800 border border-indigo-300'
                    : 'bg-gray-100 text-gray-800 border border-gray-200 hover:bg-gray-200'
                }`}
              >
                {tag.name}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Quizzes listing */}
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      ) : filteredQuizzes.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm p-12 text-center">
          <h3 className="text-lg font-medium text-gray-700 mb-2">No quizzes found</h3>
          <p className="text-gray-500">Try adjusting your filter criteria or create a new quiz.</p>
        </div>
      ) : (
        <div className="overflow-hidden bg-white shadow-sm rounded-lg">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Quiz
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell">
                    Category
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden sm:table-cell">
                    Difficulty
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden lg:table-cell">
                    Time
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell">
                    Created
                  </th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredQuizzes.map((quiz) => (
                  <tr key={quiz.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div>
                          <div className="text-sm font-medium text-gray-900">{quiz.title}</div>
                          <div className="text-sm text-gray-500 truncate max-w-xs">{quiz.description}</div>
                          <div className="mt-1 flex flex-wrap gap-1 sm:hidden">
                            {quiz.tags && quiz.tags.slice(0, 2).map(tagId => (
                              <span key={`${tagId}-${quiz.id}`} className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-100 text-indigo-800">
                                {getTagName(tagId)}
                              </span>
                            ))}
                            {quiz.tags && quiz.tags.length > 2 && (
                              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                                +{quiz.tags.length - 2}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap hidden md:table-cell">
                      <div className="text-sm text-gray-900">{quiz.category.name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap hidden sm:table-cell">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                        ${quiz.level === 'Easy' ? 'bg-green-100 text-green-800' : 
                          quiz.level === 'Medium' ? 'bg-yellow-100 text-yellow-800' : 
                          'bg-red-100 text-red-800'}`}>
                        {quiz.level}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 hidden lg:table-cell">
                      {quiz.estimated_time} mins
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 hidden md:table-cell">
                      {formatDate(quiz.created_at)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => openPreviewModal(quiz)}
                        className="text-indigo-600 hover:text-indigo-900 mr-4"
                      >
                        Preview
                      </button>
                      <Link
                        to={`/admin/quiz-edit/${quiz.id}`}
                        className="text-gray-600 hover:text-gray-900"
                      >
                        Edit
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      {/* Preview Modal */}
      {showPreviewModal && selectedQuiz && (
          
        <PreviewQuiz quiz={selectedQuiz} closeModal={closeModal} />
      )}
    </div>
  );
};

export default QuizListingPage;