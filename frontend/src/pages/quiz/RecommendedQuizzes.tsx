import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/authContext';

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
  tags?: string[] | Tag[]; // Update to handle both string[] and Tag[] types
  created_at: string;
  questions: QuizQuestion[];
  // Additional properties used in rendering
  questionsCount?: number;
  estimatedTime?: number;
  popularity?: number;
  author?: {
    name: string;
    avatar: string;
  };
  imageUrl?: string;
  difficulty?: 'Easy' | 'Medium' | 'Hard'; // Added for consistency with filteredQuizzes usage
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

const RecommendedQuizzes: React.FC = () => {
  const { fetchWithAuth, displayNotification } = useAuth();
  // Filter state
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [filteredQuizzes, setFilteredQuizzes] = useState<Quiz[]>([]);
  const [availableCategories, setAvailableCategories] = useState<CategoryObject[]>([]);
  const [availableTags, setAvailableTags] = useState<Tag[]>([]);
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('All');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  // Pagination state
  const [nextPageUrl, setNextPageUrl] = useState<string | null>(null);
  const [loadingMore, setLoadingMore] = useState<boolean>(false);

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [hasNextPage, setHasNextPage] = useState<boolean>(false);
  const [isLoadingMore, setIsLoadingMore] = useState<boolean>(false);


  const navigate = useNavigate();

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

  async function fetchQuizzes(page = 1, append = false) {
    try {
      setIsLoadingMore(append);
      if (!append) setIsLoading(true);

 
     
      const data: ApiResponse = await fetchWithAuth({
        method: 'GET',
        path: `/admin/quizzes/?page_size=10&page=${page}`,
      });
      
      // Process the quiz data to ensure tags are in a consistent format
      const processedQuizzes = data.results.map(quiz => {
        // Ensure tags are always in a consistent format (array of string IDs)
        const processedTags = Array.isArray(quiz.tags) 
          ? quiz.tags.map(tag => typeof tag === 'string' ? tag : tag.id)
          : [];
        
        // Add default values for properties used in rendering
        return {
          ...quiz,
          tags: processedTags,
          questionsCount: quiz.questions?.length || 0,
          estimatedTime: quiz.estimated_time || 0,
          popularity: 0, // Default value, replace with actual data if available
          difficulty: quiz.level, // Copy level to difficulty for consistency
          author: {
            name: "Unknown Author", // Default value, replace with actual data if available
            avatar: "https://via.placeholder.com/32" // Default avatar
          }
        };
      });
      
      // Store the next page URL for pagination
      setNextPageUrl(data.metadata.next);
      setHasNextPage(!!data.metadata.next);
      setCurrentPage(page);
      
      if (!append) {
        setQuizzes(processedQuizzes);
      } else {
        setQuizzes(prevQuizzes => [...prevQuizzes, ...processedQuizzes]);
      }
    } catch (error) {
      console.error('Error fetching quizzes:', error);
      displayNotification("error", "Failed to fetch quizzes.");
    } finally {
      setIsLoading(false);
      setLoadingMore(false);
    }
  }
  
  useEffect(() => {
    fetchQuizzes();
    fetchTags();
    fetchCategories();
  }, []);
  

  const handleLoadMore = () => {
    if (hasNextPage && !isLoadingMore) {
      fetchQuizzes(currentPage + 1, true);
    }
  };

  // Update filtered quizzes when filters change
  useEffect(() => {
    const filtered = quizzes.filter(quiz => {
      return (selectedCategory === 'All' || quiz.category?.id === selectedCategory) &&
             (selectedDifficulty === 'All' || quiz.level === selectedDifficulty);
    });
    setFilteredQuizzes(filtered);
  }, [selectedCategory, selectedDifficulty, quizzes]);

  // Function to render difficulty badge with appropriate color
  const renderDifficultyBadge = (difficulty: 'Easy' | 'Medium' | 'Hard') => {
    let bgColor = '';
    switch(difficulty) {
      case 'Easy':
        bgColor = 'bg-green-100 text-green-800';
        break;
      case 'Medium':
        bgColor = 'bg-yellow-100 text-yellow-800';
        break;
      case 'Hard':
        bgColor = 'bg-red-100 text-red-800';
        break;
    }
    
    return (
      <span className={`text-xs font-medium px-2.5 py-0.5 rounded ${bgColor}`}>
        {difficulty}
      </span>
    );
  };

  // Get unique categories from availableCategories
  const categories = [
    { id: 'All', name: 'All' },
    ...availableCategories
  ];

  const difficulties = ['All', 'Easy', 'Medium', 'Hard'];

  return (
    <div className="p-6 bg-gray-50">
      <h1 className="text-3xl font-bold mb-8">Recommended Quizzes</h1>
      
      {/* Filters */}
      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <div className="flex-1">
          <label htmlFor="category-filter" className="block text-sm font-medium text-gray-700 mb-1">
            Category
          </label>
          <select
            id="category-filter"
            className="w-full p-2 border border-gray-300 rounded-md bg-white"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            {categories.map(category => (
              <option key={category.id} value={category.id}>{category.name}</option>
            ))}
          </select>
        </div>
        <div className="flex-1">
          <label htmlFor="difficulty-filter" className="block text-sm font-medium text-gray-700 mb-1">
            Difficulty
          </label>
          <select
            id="difficulty-filter"
            className="w-full p-2 border border-gray-300 rounded-md bg-white"
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
          >
            {difficulties.map(difficulty => (
              <option key={difficulty} value={difficulty}>{difficulty}</option>
            ))}
          </select>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      ) : (
        <>
          {/* Featured Quiz */}
          {filteredQuizzes.length > 0 && (
            <div className="mb-12">
              <div className="text-sm text-gray-500 mb-4">FEATURED QUIZ</div>
              <div className="bg-white border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition">
                <div className="md:flex">
                  {filteredQuizzes[0].imageUrl && (
                    <div className="md:flex-shrink-0">
                      <img 
                        src={filteredQuizzes[0].imageUrl || "https://via.placeholder.com/400x300"}
                        alt={filteredQuizzes[0].title} 
                        className="h-48 w-full object-cover md:w-64"
                      />
                    </div>
                  )}
                  <div className="p-6">
                    <div className="flex justify-between items-start">
                      <div>
                        <div className="uppercase tracking-wide text-sm text-indigo-600 font-semibold mb-1">
                          {filteredQuizzes[0].category?.name || "Uncategorized"}
                        </div>
                        <h2 className="text-xl font-bold text-gray-900 hover:text-indigo-600 transition mb-2">
                          {filteredQuizzes[0].title}
                        </h2>
                      </div>
                      <div>
                        {renderDifficultyBadge(filteredQuizzes[0].level)}
                      </div>
                    </div>
                    <p className="mt-2 text-gray-600">{filteredQuizzes[0].description}</p>
                    <div className="mt-4 flex items-center text-sm text-gray-500">
                      <span className="mr-4">{filteredQuizzes[0].questionsCount} questions</span>
                      <span className="mr-4">~{filteredQuizzes[0].estimatedTime} mins</span>
                      <span>{filteredQuizzes[0].popularity?.toLocaleString()} attempts</span>
                    </div>
                    <div className="mt-6 flex items-center justify-between">
                      <div className="flex items-center">
                        {/* <img 
                          src={filteredQuizzes[0].author?.avatar || "https://via.placeholder.com/32"}
                          alt={filteredQuizzes[0].author?.name || "Author"} 
                          className="w-8 h-8 rounded-full mr-2"
                        />
                        <span className="text-sm text-gray-700">{filteredQuizzes[0].author?.name || "Unknown Author"}</span> */}
                      </div>
                      <button onClick={() => navigate(`${filteredQuizzes[0].id}`)} className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition">
                        Start Quiz
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {/* Quiz List */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {filteredQuizzes.slice(1).map(quiz => (
              <div key={quiz.id} className="bg-white border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition">
                <div className="p-6">
                  <div className="flex justify-between items-start mb-3">
                    <div className="uppercase tracking-wide text-sm text-indigo-600 font-semibold">
                      {quiz.category?.name || "Uncategorized"}
                    </div>
                    {renderDifficultyBadge(quiz.level)}
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 hover:text-indigo-600 transition mb-2">
                    {quiz.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4">{quiz.description}</p>
                  <div className="flex items-center text-xs text-gray-500 mb-4">
                    <span className="mr-3">{quiz.questionsCount} questions</span>
                    <span className="mr-3">~{quiz.estimatedTime} mins</span>
                    <span>{quiz.popularity?.toLocaleString()} attempts</span>
                  </div>
                  
                  {/* Tags */}
                  <div className="flex flex-wrap gap-2 mb-4">
                    {Array.isArray(quiz.tags) && quiz.tags.slice(0, 3).map(tag => {
                      const tagName = typeof tag === 'string' 
                        ? availableTags.find(t => t.id === tag)?.name || tag 
                        : tag.name;
                      
                      return (
                        <span 
                          key={typeof tag === 'string' ? tag : tag.id} 
                          className="px-2 py-1 bg-gray-100 text-gray-800 text-xs rounded-full"
                        >
                          {tagName}
                        </span>
                      );
                    })}
                    {Array.isArray(quiz.tags) && quiz.tags.length > 3 && (
                      <span className="px-2 py-1 text-gray-500 text-xs">
                        +{quiz.tags.length - 3} more
                      </span>
                    )}
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      {/* <img 
                        src={quiz.author?.avatar || "https://via.placeholder.com/32"}
                        alt={quiz.author?.name || "Author"} 
                        className="w-6 h-6 rounded-full mr-2"
                      />
                      <span className="text-xs text-gray-700">{quiz.author?.name || "Unknown Author"}</span> */}
                    </div>
                    <button onClick={() => navigate(`${quiz.id}`)} className="px-3 py-1 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 transition">
                      Start Quiz
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          {/* Empty state */}
          {filteredQuizzes.length === 0 && (
            <div className="text-center py-12">
              <h3 className="text-lg font-medium text-gray-900 mb-2">No quizzes found</h3>
              <p className="text-gray-500">Try adjusting your filters to see more results.</p>
            </div>
          )}
          
          {/* Load More Button */}
          {filteredQuizzes.length > 0 && nextPageUrl && (
            <button
              onClick={handleLoadMore}
              disabled={loadingMore}
              className={`w-full mt-4 text-indigo-600 font-medium py-2 hover:bg-indigo-50 rounded-lg transition-colors ${loadingMore ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {loadingMore ? 'Loading more...' : 'Load more quizzes'}
            </button>
          )}
        </>
      )}
    </div>
  );
};

export default RecommendedQuizzes;