// @ts-nocheck
import React, { useState, useEffect, useRef } from 'react';
import { Link, useParams } from 'react-router-dom';
import { useAuth } from '../../context/authContext';

interface Video {
  id: string;
  title: string;
  description: string;
  video_file: string;
  thumbnail: string;
  views: number;
  created_at: string;
  average_rating: number | null;
  likes_count: number;
  has_rated: boolean;
  has_liked: boolean;
  category: {
    id: string;
    name: string;
    slug: string;
  };
  tags: {
    id: string;
    name: string;
  }[];
}

interface RelatedVideo {
  id: string;
  title: string;
  thumbnail: string;
  views: number;
  created_at: string;
  duration?: string;
  channel?: string;
}

const VideoPlayerPage: React.FC = () => {
  const { videoId } = useParams<{ videoId: string }>();
  const [video, setVideo] = useState<Video | null>(null);
  const [relatedVideos, setRelatedVideos] = useState<RelatedVideo[]>([]);
  const [relatedArticles, setRelatedArticles] = useState<RelatedVideo[]>([]);
  const [relatedQuizzes, setRelatedQuizzes] = useState<RelatedVideo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showRatingPopup, setShowRatingPopup] = useState(false);
  const [rating, setRating] = useState<number>(0);
  const videoRef = useRef<HTMLVideoElement>(null);
  const { fetchWithAuth, displayNotification } = useAuth();
  const [hasPassedHalfway, setHasPassedHalfway] = useState(false);

  // Fetch video data when component mounts or videoId changes
  useEffect(() => {
    const fetchVideoData = async () => {
      if (!videoId) return;

      setLoading(true);
      try {
        const data = await fetchWithAuth({
          method: 'GET',
          path: `/admin/videos/${videoId}/`,
        });
        setVideo(data);
        
      } catch (err) {
        console.error('Error fetching video:', err);
        setError('Failed to load video. Please try again later.');
        displayNotification("error", "Failed to load video.");
      } finally {
        setLoading(false);
      }

      fetchRelatedVideos(videoId);
    };

    fetchVideoData();
  }, [videoId]);

  // Fetch related videos based on category
  const fetchRelatedVideos = async (videoId: string) => {
    try {
      const data = await fetchWithAuth({
        method: 'GET',
        path: `/admin/videos/${videoId}/related/?limit=5`,
      });
      console.log(data?.data)
      setRelatedVideos(data?.data?.related_videos || []);
      // setRelatedVideos(data?.data?.videos || []);
      setRelatedArticles(data?.data?.related_articles || [])
      setRelatedQuizzes(data?.data?.related_quizzes || [])
    } catch (err) {
      console.error('Error fetching related videos:', err);
      displayNotification("error", "Failed to load related videos.");
    }
  };

  // Handle video time update to show rating popup
  const handleTimeUpdate = () => {
    if (videoRef.current && !hasPassedHalfway && !video?.has_rated) {
      const currentTime = videoRef.current.currentTime;
      const duration = videoRef.current.duration;
      
      if (currentTime > duration * 0.8) {
        setShowRatingPopup(true);
        setHasPassedHalfway(true);
      }
    }
  };

  // Handle rating submission
  const handleRateVideo = async () => {
    if (!videoId || rating === 0) return;

    try {
      await fetchWithAuth({
        method: 'POST',
        path: `/admin/videos/${videoId}/rate/`,
        body: { rating },
      });
      
      displayNotification("success", "Thank you for rating this video!");
      setShowRatingPopup(false);
      
      // Update video data to reflect the new rating
      const updatedVideo = await fetchWithAuth({
        method: 'GET',
        path: `/admin/videos/${videoId}/`,
      });
      setVideo(updatedVideo);
    } catch (err) {
      console.error('Error rating video:', err);
    }
  };

  // Handle like/dislike
  const handleLikeVideo = async (liked: boolean) => {
    if (!videoId) return;

    try {
      await fetchWithAuth({
        method: 'POST',
        path: `/admin/videos/${videoId}/like/`,
        body: { },
      });
      
      // Update video data to reflect the new like status
      const updatedVideo = await fetchWithAuth({
        method: 'GET',
        path: `/admin/videos/${videoId}/`,
      });
      setVideo(updatedVideo);
      
      displayNotification("success", liked ? "Video liked!" : "Video disliked!");
    } catch (err) {
      console.error('Error liking/disliking video:', err);
    }
  };

  // Format date for display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else if (diffDays < 30) {
      const weeks = Math.floor(diffDays / 7);
      return `${weeks} ${weeks === 1 ? 'week' : 'weeks'} ago`;
    } else if (diffDays < 365) {
      const months = Math.floor(diffDays / 30);
      return `${months} ${months === 1 ? 'month' : 'months'} ago`;
    } else {
      const years = Math.floor(diffDays / 365);
      return `${years} ${years === 1 ? 'year' : 'years'} ago`;
    }
  };

  // Format view count
  const formatViewCount = (views: number) => {
    if (views >= 1000000) {
      return `${(views / 1000000).toFixed(1)}M views`;
    } else if (views >= 1000) {
      return `${(views / 1000).toFixed(1)}K views`;
    } else {
      return `${views} views`;
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          </div>;
  }

  if (error || !video) {
    return <div className="flex items-center justify-center h-screen">{error || 'Video not found'}</div>;
  }

  return (
    <div className="flex flex-col lg:flex-row bg-gray-100 min-h-screen">
      {/* Main Content */}
      <div className="lg:w-2/3 p-4">
        {/* Video Player */}
        <div className="bg-black relative pt-0 pb-0 h-0" style={{ paddingBottom: '56.25%' }}>
          <video 
            ref={videoRef}
            className="absolute inset-0 w-full h-full object-cover"
            src={video.video_file}
            poster={video.thumbnail}
            controls
            autoPlay
            onTimeUpdate={handleTimeUpdate}
          />
        </div>

        {/* Video Info */}
        <div className="mt-4">
          <h1 className="text-xl font-bold">{video.title}</h1>
          <div className="flex items-center justify-between mt-2">
            <div className="text-gray-600">
              {formatViewCount(video.views)} • {formatDate(video.created_at)}
            </div>
            <div className="flex space-x-4">
              <div className="flex items-center">
                <button 
                  className={`flex items-center ${video.has_liked ? 'text-blue-600' : 'text-gray-700'}`}
                  onClick={() => handleLikeVideo(true)}
                >
                  <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
                  </svg>
                  {video.likes_count} Like{video.likes_count !== 1 ? 's' : ''}
                </button>
              </div>
              <div className="flex items-center">
                <button 
                  className={`flex items-center ${video.has_liked === false ? 'text-red-600' : 'text-gray-700'}`}
                  onClick={() => handleLikeVideo(false)}
                >
                  <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M18 9.5a1.5 1.5 0 11-3 0v-6a1.5 1.5 0 013 0v6zM14 9.667v-5.43a2 2 0 00-1.105-1.79l-.05-.025A4 4 0 0011.055 2h-5.416a2 2 0 00-1.962 1.608l-1.2 6A2 2 0 004.44 12H8v4a2 2 0 002 2 1 1 0 001-1v-.667a4 4 0 01.8-2.4l1.4-1.866a4 4 0 00.8-2.4z" />
                  </svg>
                  Dislike
                </button>
              </div>
              {video.average_rating && (
                <div className="flex items-center text-yellow-500">
                  <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  {video.average_rating.toFixed(1)}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Tags */}
        {video.tags.length > 0 && (
          <div className="mt-4 flex flex-wrap gap-2">
            {video.tags.map(tag => (
              <Link 
                key={tag.id} 
                to={`/tags/${tag.name.toLowerCase()}`}
                className="bg-gray-300 hover:bg-gray-400 px-2 py-1 rounded-full text-xs"
              >
                {tag.name}
              </Link>
            ))}
          </div>
        )}

        {/* Description */}
        <div className="mt-4 bg-gray-200 p-4 rounded">
          <p className="text-sm">{video.description}</p>
        </div>
      </div>

      {/* Related Videos */}
      <div className="lg:w-1/3 p-4">
        <h2 className="text-lg font-bold mb-4">Related Videos</h2>
        <div className="space-y-4">
          {relatedVideos.map(relatedVideo => (
            <Link 
              key={relatedVideo.id} 
              className="flex cursor-pointer hover:bg-gray-200 p-2 rounded"
              to={`/videos/${relatedVideo.id}`}
            >
              <div className="relative w-40 h-24 flex-shrink-0">
                <img 
                  src={relatedVideo.thumbnail} 
                  alt={relatedVideo.title} 
                  className="w-full h-full object-cover"
                />
                {relatedVideo.duration && (
                  <div className="absolute bottom-1 right-1 bg-black text-white text-xs px-1 rounded">
                    {relatedVideo.duration}
                  </div>
                )}
              </div>
              <div className="ml-2 flex-grow">
                <h3 className="font-medium text-sm line-clamp-2">{relatedVideo.title}</h3>
                <p className="text-gray-600 text-xs mt-1">{relatedVideo.channel || video.category.name}</p>
                <p className="text-gray-600 text-xs">
                  {formatViewCount(relatedVideo.views)} • {formatDate(relatedVideo.created_at)}
                </p>
              </div>
            </Link>
          ))}
        </div>

        {/* // For related articles section */}
        {relatedArticles?.length > 0 && (
          <div className="mt-4">
            <h2 className="text-lg font-bold mb-4">Related Articles</h2>
            <div className="space-y-4">
              {relatedArticles.map(article => (
                <Link 
                  key={article.id} 
                  className="flex cursor-pointer hover:bg-gray-200 p-2 rounded"
                  to={`/articles/${article.id}`}
                >
                  <div className="relative w-40 h-24 flex-shrink-0">
                    <img 
                      src={article.top_image || '/placeholder-image.jpg'} 
                      alt={article.title} 
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute bottom-1 right-1 bg-black text-white text-xs px-1 rounded">
                      {new Date(article.publish_date).toLocaleDateString()} {/* Display publish date */}
                    </div>
                  </div>
                  <div className="ml-2 flex-grow">
                    <h3 className="font-medium text-sm line-clamp-2">{article.title}</h3>
                    <p className="text-gray-600 text-xs mt-1">{article.authors}</p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}

        {relatedQuizzes?.length > 0 && (
          <div className="mt-4">
            <h2 className="text-lg font-bold mb-4">Related Quizzes</h2>
            <div className="space-y-4">
              {relatedQuizzes.map(quiz => (
                <Link 
                  key={quiz.id} 
                  className="flex cursor-pointer hover:bg-gray-200 p-2 rounded"
                  to={`/quizzes/${quiz.id}`}
                >
                  <div className="relative w-40 h-24 flex-shrink-0 bg-gray-300 flex items-center justify-center">
                    <span className="text-lg font-bold">{quiz.level}</span>
                    <div className="absolute bottom-1 right-1 bg-black text-white text-xs px-1 rounded">
                      {quiz.estimated_time} mins {/* Display quiz time */}
                    </div>
                  </div>
                  <div className="ml-2 flex-grow">
                    <h3 className="font-medium text-sm line-clamp-2">{quiz.title}</h3>
                    <p className="text-gray-600 text-xs mt-1">{quiz.category.name}</p>
                    <p className="text-gray-600 text-xs">{quiz.questions.length} questions</p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}


      


      
      </div>
      

      

      {/* Rating Popup */}
      {showRatingPopup && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg max-w-md w-full">
            <h2 className="text-xl font-bold mb-4">Rate this video</h2>
            <p className="mb-4">We'd love to know what you think of this video!</p>
            
            <div className="flex justify-center mb-6">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  className="text-3xl px-2 focus:outline-none"
                  onClick={() => setRating(star)}
                >
                  <span className={star <= rating ? "text-yellow-500" : "text-gray-300"}>★</span>
                </button>
              ))}
            </div>
            
            <div className="flex justify-end space-x-4">
              <button
                className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100"
                onClick={() => setShowRatingPopup(false)}
              >
                Skip
              </button>
              <button
                className={`px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 ${rating === 0 ? 'opacity-50 cursor-not-allowed' : ''}`}
                onClick={handleRateVideo}
                disabled={rating === 0}
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VideoPlayerPage;