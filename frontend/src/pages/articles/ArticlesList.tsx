import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/authContext';
import { BookmarkIcon } from 'lucide-react';

// Types
interface Author {
  name: string;
  avatar: string;
}

interface Article {
  id: string;
  title: string;
  excerpt: string;
  author: Author;
  publishedDate: string;
  readingTime: number;
  category: string;
  imageUrl?: string;
  likes_count: number;
  has_liked: boolean;
}

interface ApiResponse {
  metadata: {
    count: number;
    page: number;
    page_size: number;
    next: string | null;
    previous: string | null;
  };
  results: ApiArticle[];
}

interface ApiArticle {
  id: string;
  title: string;
  authors: string;
  publish_date: string;
  text: string;
  top_image: string;
  meta_description: string;
  likes_count: number;
  has_liked: boolean;
}

const ArticlesList: React.FC = () => {
  const { fetchWithAuth, displayNotification } = useAuth();
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [pageLoading, setPageLoading] = useState<boolean>(true);
  const [nextPageUrl, setNextPageUrl] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [viewMode, setViewMode] = useState<'all' | 'bookmarked'>('all')

  // Function to transform API articles to our Article format
  const transformArticles = (apiArticles: ApiArticle[]): Article[] => {
    return apiArticles.map(article => {
      // Extract excerpt from text or meta_description
      const excerpt = article.meta_description || article.text.substring(0, 150) + '...';
      
      // Format date
      const publishDate = new Date(article.publish_date);
      const formattedDate = publishDate.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });

      // Create author object (using authors string from API)
      const author: Author = {
        name: article.authors || 'Unknown Author',
        avatar: '/api/placeholder/40/40' // Placeholder avatar
      };

      // Calculate reading time (rough estimate: 200 words per minute)
      const wordCount = article.text.split(' ').length;
      const readingTime = Math.max(1, Math.round(wordCount / 200));

      return {
        id: article.id,
        title: article.title,
        excerpt,
        author,
        publishedDate: formattedDate,
        readingTime,
        category: 'Article', // Default category, could be improved
        imageUrl: article.top_image || undefined,
        likes_count: article.likes_count,
        has_liked: article.has_liked
      };
    });
  };

  // Fetch articles from API
  const fetchArticles = async (page: number = 1, newOne:boolean=false) => {
    try {
      if(newOne){
        setPageLoading(true)
      }else{
        setLoading(true);
      }
      
      const response = await fetchWithAuth({
        method: 'GET',
        path: `/admin/articles/?page=${page}&page_size=5`,
      });
      
      const data: ApiResponse = response;
      const transformedArticles = transformArticles(data.results);
      
      if (page === 1) {
        setArticles(transformedArticles);
      } else {
        setArticles(prevArticles => [...prevArticles, ...transformedArticles]);
      }
      
      setNextPageUrl(data.metadata.next);
      setCurrentPage(data.metadata.page);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching articles:', err);
      setLoading(false);
    }finally{
      if(newOne){
        setPageLoading(false)
      }else{
        setLoading(false);
      }
    }
  };

  // Handle load more button click
  const handleLoadMore = () => {
    if (nextPageUrl) {
      fetchArticles(currentPage + 1);
    }
  };

  // Handle article like
  const handleLike = async (articleId: string) => {
    try {
      await fetchWithAuth({
        method: 'POST',
        path: `/admin/articles/${articleId}/like/`,
      });

      // Update like count and status in state
      setArticles(prevArticles => 
        prevArticles.map(article => {
          if (article.id === articleId) {
            return {
              ...article,
              likes_count: article.has_liked ? article.likes_count - 1 : article.likes_count + 1,
              has_liked: !article.has_liked
            };
          }
          return article;
        })
      );

      displayNotification(
        "success",
        "Article liked successfully!"
      )

    } catch (err) {
      console.error('Error liking article:', err);
    }
  };

  // New method to fetch bookmarked articles
  const fetchBookmarkedArticles = async (page: number = 1) => {
    try {
      setPageLoading(true);
      const response = await fetchWithAuth({
        method: 'GET',
        path: `/admin/articles/bookmarked/?page=${page}&page_size=5`,
      });
      
      const data: ApiResponse = response;
      const transformedArticles = transformArticles(data.results);
      
      if (page === 1) {
        setArticles(transformedArticles);
      } else {
        setArticles(prevArticles => [...prevArticles, ...transformedArticles]);
      }
      
      setNextPageUrl(data.metadata.next);
      setCurrentPage(data.metadata.page);
      setPageLoading(false);
    } catch (err) {
      console.error('Error fetching bookmarked articles:', err);
      setPageLoading(false);
      displayNotification('error', 'Failed to fetch bookmarked articles');
    }
  };


  // Initial fetch on component mount
  useEffect(() => {
    const fetching = () => {
      setPageLoading(true)
      fetchArticles();
      setPageLoading(false)
    }
    fetching();
  }, []);


  // Toggle between all articles and bookmarked articles
  const toggleBookmarkedView = () => {
    if (viewMode === 'all') {
      setViewMode('bookmarked');
      fetchBookmarkedArticles();
    } else {
      setViewMode('all');
      fetchArticles();
    }
  };

  return (
    <div className="container mx-auto p-6 bg-gray-50">
      <div className="flex justify-end mb-6">
        <button 
          onClick={toggleBookmarkedView}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
            viewMode === 'bookmarked' 
              ? 'bg-indigo-600 text-white hover:bg-indigo-700' 
              : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
          }`}
        >
          <BookmarkIcon size={20} />
          <span>
            {viewMode === 'all' ? 'View Bookmarked' : 'View All Articles'}
          </span>
        </button>
      </div>
      {pageLoading ? (
        <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
      ): (
        <div className="space-y-8">
          {/* Featured Section - Show only if we have articles */}
          {articles.length > 0 && (
            <div className="border-b pb-8">
              <div className="text-sm text-gray-500 mb-4">FEATURED STORY</div>
              <Link to={`/articles/${articles[0].id}`} className="flex flex-col md:flex-row gap-6">
                {articles[0].imageUrl && (
                  <img 
                    src={articles[0].imageUrl} 
                    alt={articles[0].title} 
                    className="w-full md:w-1/2 h-56 object-cover rounded-lg"
                  />
                )}
                <div className="flex-1">
                  <h2 className="text-2xl font-bold mb-2 hover:text-gray-700 cursor-pointer">
                    {articles[0].title}
                  </h2>
                  <p className="text-gray-600 mb-4">{articles[0].excerpt}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      {/* <img 
                        src={articles[0].author.avatar} 
                        alt={articles[0].author.name} 
                        className="w-8 h-8 rounded-full mr-2"
                      /> */}
                      <div className="text-sm">
                        <div className="font-medium">{articles[0].author.name}</div>
                        <div className="text-gray-500">
                          {articles[0].publishedDate} · {articles[0].readingTime} min read · {articles[0].category}
                        </div>
                      </div>
                    </div>
                    <button 
                      onClick={(e) => {
                        e.preventDefault();
                        handleLike(articles[0].id);
                      }}
                      className="flex items-center text-gray-500 hover:text-red-500"
                    >
                      <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        className="h-5 w-5" 
                        fill={articles[0].has_liked ? "currentColor" : "none"} 
                        viewBox="0 0 24 24" 
                        stroke="currentColor"
                        strokeWidth={articles[0].has_liked ? "0" : "1.5"}
                        style={{ color: articles[0].has_liked ? '#ef4444' : 'inherit' }}
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                      </svg>
                      <span className="ml-1">{articles[0].likes_count}</span>
                    </button>
                  </div>
                </div>
              </Link>
            </div>
          )}
          
          {/* Article List */}
          {articles.length > (articles.length > 0 ? 1 : 0) ? (
            <div className="space-y-8">
              <h3 className="text-xl font-semibold mb-4">Latest Articles</h3>
              
              {articles.slice(articles.length > 0 ? 1 : 0).map(article => (
                <Link to={`/articles/${article.id}`} key={article.id} className="flex flex-col md:flex-row gap-6 border-b pb-8">
                  <div className="flex-1">
                    <h2 className="text-xl font-bold mb-2 hover:text-gray-700 cursor-pointer">
                      {article.title}
                    </h2>
                    <p className="text-gray-600 mb-4">{article.excerpt}</p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        {/* <img 
                          src={article.author.avatar} 
                          alt={article.author.name} 
                          className="w-8 h-8 rounded-full mr-2"
                        /> */}
                        <div className="text-sm">
                          <div className="font-medium">{article.author.name}</div>
                          <div className="text-gray-500">
                            {article.publishedDate} · {article.readingTime} min read · {article.category}
                          </div>
                        </div>
                      </div>
                      <button 
                        onClick={(e) => {
                          e.preventDefault();
                          handleLike(article.id);
                        }}
                        className="flex items-center text-gray-500 hover:text-red-500"
                      >
                        <svg 
                          xmlns="http://www.w3.org/2000/svg" 
                          className="h-5 w-5" 
                          fill={article.has_liked ? "currentColor" : "none"} 
                          viewBox="0 0 24 24" 
                          stroke="currentColor"
                          strokeWidth={article.has_liked ? "0" : "1.5"}
                          style={{ color: article.has_liked ? '#ef4444' : 'inherit' }}
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                        </svg>
                        <span className="ml-1">{article.likes_count}</span>
                      </button>
                    </div>
                  </div>
                  {article.imageUrl && (
                    <img 
                      src={article.imageUrl} 
                      alt={article.title} 
                      className="w-full md:w-1/3 h-40 object-cover rounded-lg"
                    />
                  )}
                </Link>
              ))}
            </div>
          ) : (
            <>
            {viewMode === 'bookmarked' && articles.length === 0 && (
            <div className="text-center py-12">
              <BookmarkIcon size={48} className="mx-auto text-gray-400 mb-4" />
              <h2 className="text-xl font-semibold text-gray-600">
                No Bookmarked Articles
              </h2>
              <p className="text-gray-500 mt-2">
                You haven't bookmarked any articles yet.
              </p>
              <button 
                onClick={() => {
                  setViewMode('all')
                  fetchArticles();
                }}
                className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
              >
                Browse Articles
              </button>
            </div>
          )}
          </>
          )}


          {articles?.length > 0 && nextPageUrl && (
              <button 
                onClick={handleLoadMore}
                disabled={loading}
                className="w-full mt-4 text-indigo-600 font-medium py-2 hover:bg-indigo-50 rounded-lg transition-colors disabled:opacity-50">
                {loading ? (
                  <span className="flex items-center justify-center">
                    <span className="animate-spin h-4 w-4 mr-2 border-t-2 border-b-2 border-indigo-600 rounded-full"></span>
                    Loading...
                  </span>
                ) : (
                  "Load More Articles"
                )}
              </button>
          )}
        </div>
      )}
    </div>
  );
};

export default ArticlesList;