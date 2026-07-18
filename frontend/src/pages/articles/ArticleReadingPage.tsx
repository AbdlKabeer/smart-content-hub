import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../../context/authContext';
import { BookmarkPlus,  ThumbsUp, BookmarkMinus } from 'lucide-react';
import { Link } from 'react-router-dom';

interface Article {
  id: string;
  title: string;
  authors: string;
  publish_date: string;
  text: string;
  top_image: string;
  meta_description: string;
  likes_count: number;
  has_liked: boolean;
  keywords: string;
  source_url: string;
  has_bookmarked:boolean;
  bookmarks_count:number;
}

const ArticleReadingPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { fetchWithAuth } = useAuth();
  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        setLoading(true);
        const response = await fetchWithAuth({
          method: 'GET',
          path: `/admin/articles/${id}/`,
        });
        
        setArticle(response);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching article:', err);
        setError('Failed to load article. Please try again later.');
        setLoading(false);
      }
    };

    if (id) {
      fetchArticle();
    }
  }, [id, fetchWithAuth]);

  // Format the publish date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric'
    });
  };

  // Calculate reading time based on word count (200 words per minute)
  const calculateReadingTime = (text: string) => {
    const wordCount = text.split(/\s+/).length;
    const minutes = Math.max(1, Math.round(wordCount / 200));
    return `${minutes} min read`;
  };

  // Handle like functionality
  const handleLike = async () => {
    if (!article) return;
    
    try {
      await fetchWithAuth({
        method: 'POST',
        path: `/admin/articles/${id}/like/`,
      });
      
      setArticle(prev => {
        if (!prev) return null;
        return {
          ...prev,
          likes_count: prev.has_liked ? prev.likes_count - 1 : prev.likes_count + 1,
          has_liked: !prev.has_liked
        };
      });
    } catch (err) {
      console.error('Error liking article:', err);
    }
  };


  const handleBookmark = async () => {
    if (!article) return;
    
    try {
      if (article.has_bookmarked) {
        // Unbookmark
        await fetchWithAuth({
          method: 'DELETE',
          path: `/admin/articles/${id}/unbookmark/`,
        });
      } else {
        // Bookmark
        await fetchWithAuth({
          method: 'POST',
          path: `/admin/articles/${id}/bookmark/`,
        });
      }
      
      // Update local state
      setArticle(prev => {
        if (!prev) return null;
        return {
          ...prev,
          has_bookmarked: !prev.has_bookmarked,
          bookmarks_count: prev.has_bookmarked 
            ? prev.bookmarks_count - 1 
            : prev.bookmarks_count + 1
        };
      });
    } catch (err) {
      console.error('Error bookmarking article:', err);
      // Optionally show an error toast or message
    }
  };

  // Extract paragraphs from the text
  const getParagraphs = (text: string) => {
    return text.split('\n\n').filter(p => p.trim() !== '');
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin h-8 w-8 border-t-2 border-b-2 border-indigo-600 rounded-full"></div>
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="max-w-4xl mx-auto p-6 text-center">
        <h2 className="text-2xl font-bold text-red-600">Error</h2>
        <p className="mt-2">{error || 'Article not found'}</p>
        <Link to="/articles" className="mt-4 inline-block text-indigo-600 hover:underline">
          Return to articles
        </Link>
      </div>
    );
  }

  const paragraphs = getParagraphs(article.text);
  const readTime = calculateReadingTime(article.text);
  const formattedDate = formatDate(article.publish_date);
  const keywords = article.keywords ? article.keywords.split(',').map(k => k.trim()).filter(k => k) : [];

  return (
    <div className="max-w-4xl mx-auto bg-white min-h-screen p-6">
      {/* Article Header */}
      <div className="mb-8">
        {article.top_image && (
          <img 
            src={article.top_image} 
            alt={article.title} 
            className="w-full h-64 object-cover rounded-lg"
          />
        )}
        
        <div className="mt-6">
          <div className="flex flex-wrap gap-2 mb-4">
            {keywords.map((tag, index) => (
              <span key={index} className="bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded-full">
                {tag}
              </span>
            ))}
          </div>
          
          <h1 className="text-3xl font-bold text-gray-800 mb-4">{article.title}</h1>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              {/* <img 
                src="/api/placeholder/40/40" 
                alt={article.authors} 
                className="w-10 h-10 rounded-full mr-3"
              /> */}
              <div>
                <p className="font-medium">{article.authors}</p>
                <p className="text-gray-500 text-sm">{formattedDate} · {readTime}</p>
              </div>
            </div>
            
            <div className="flex space-x-4">
                <button 
                  onClick={handleBookmark}
                  className={`text-gray-500 hover:text-indigo-600 ${article.has_bookmarked ? 'text-indigo-600' : ''}`}
                >
                  {article.has_bookmarked ? <BookmarkMinus size={20} /> : <BookmarkPlus size={20} />}
                </button>
            </div>
          </div>
          {/* Article Footer - add bookmarks count */}
          <div className="mt-12 pt-6 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <button 
                  onClick={handleLike}
                  className="flex items-center space-x-1 text-gray-600 hover:text-indigo-600"
                >
                  <ThumbsUp size={18} 
                    className={article.has_liked ? "text-indigo-600" : ""} 
                  />
                  <span>{article.likes_count}</span>
                </button>
                <button 
                  onClick={handleBookmark}
                  className={`flex items-center space-x-1 text-gray-500 hover:text-indigo-600 ${article.has_bookmarked ? 'text-indigo-600' : ''}`}
                >
                  {article.has_bookmarked ? <BookmarkMinus size={18} /> : <BookmarkPlus size={18} />}
                  <span>{article.bookmarks_count}</span>
                </button>
              </div>
            </div>
        </div>
        </div>
      </div>
      
      {/* Article Content */}
      <div className="prose max-w-none">
        {paragraphs.map((paragraph, index) => (
          <p key={index} className="mb-6 text-gray-700 leading-relaxed">
            {paragraph}
          </p>
        ))}
      </div>
      
      {/* Article Footer */}
      <div className="mt-12 pt-6 border-t border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button 
              onClick={handleLike}
              className="flex items-center space-x-1 text-gray-600 hover:text-indigo-600"
            >
              <ThumbsUp size={18} 
                className={article.has_liked ? "text-indigo-600" : ""} 
              />
              <span>{article.likes_count}</span>
            </button>
            <button 
                  onClick={handleBookmark}
                className={`flex items-center space-x-1 text-gray-500 hover:text-indigo-600 ${article.has_bookmarked ? 'text-indigo-600' : ''}`}
              >
                {article.has_bookmarked ? <BookmarkMinus size={18} /> : <BookmarkPlus size={18} />}
                <span>{article.bookmarks_count}</span>
              </button>
          </div>
          
          {/* {article.source_url && (
            <a 
              href={article.source_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              View Original
            </a>
          )} */}
        </div>
        
        <div className="mt-8">
          <h3 className="font-bold text-lg mb-4">Related Articles</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Link to={`/articles`} className="border border-gray-200 rounded-lg p-4 hover:border-indigo-300 cursor-pointer transition-colors">
              <h4 className="font-medium mb-1">Browse more articles</h4>
              <p className="text-gray-500 text-sm">Discover more content</p>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArticleReadingPage;