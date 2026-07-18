import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import thumbnail from '../../assets/images/thumbnail-im.jpg';
import { useAuth } from '../../context/authContext';

interface Tag {
  id: string;
  name: string;
}

interface Category {
  id: string;
  name: string;
  slug: string;
}

interface Video {
  id: string;
  title: string;
  description: string;
  slug: string;
  category: Category;
  tags: Tag[];
  video_file: string;
  thumbnail: string;
  created_at: string;
  views: number;
  status?: 'Public' | 'Unlisted' | 'Private';
  channel?: string;
  channelAvatar?: string;
  duration?: string;
  date?: string;
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
  results: Video[];
}

const AllVideosPage: React.FC = () => {
  const { fetchWithAuth, displayNotification } = useAuth();
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [videos, setVideos] = useState<Video[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [availableCategories, setAvailableCategories] = useState<Tag[]>([]);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [hasNextPage, setHasNextPage] = useState<boolean>(false);
  const [isLoadingMore, setIsLoadingMore] = useState<boolean>(false);

  async function fetchTags() {
    try {
      const data = await fetchWithAuth({
        method: 'GET',
        path: `/admin/tags/`,
      });
      setAvailableCategories(data);
    } catch (error) {
      console.error('Error fetching tags:', error);
      displayNotification("error", "Failed to fetch tags.");
    }
  }

  async function fetchVideos(page = 1, append = false) {
    try {
      setIsLoadingMore(append);
      if (!append) setIsLoading(true);
      
      const data: ApiResponse = await fetchWithAuth({
        method: 'GET',
        path: `/admin/videos/?page_size=10&page=${page}`,
      });
      
      // Set default status if not provided in API
      const videosWithStatus = data.results.map(video => ({
        ...video,
        status: video.status || 'Public', // Default to 'Public' if status is not provided
        date: new Date(video.created_at).toLocaleDateString(), // Format date from created_at
        channel: video.category?.name || 'Unknown Channel', // Use category name as channel if available
        duration: '00:00' // Add a placeholder duration since it's not in the API
      }));
      
      if (append) {
        setVideos(prev => [...prev, ...videosWithStatus]);
      } else {
        setVideos(videosWithStatus);
      }
      
      // Check if there's a next page
      setHasNextPage(!!data.metadata.next);
      setCurrentPage(page);
    } catch (error) {
      console.error('Error fetching videos:', error);
      displayNotification("error", "Failed to fetch videos.");
    } finally {
      setIsLoading(false);
      setIsLoadingMore(false);
    }
  }

  const loadMoreVideos = () => {
    if (hasNextPage && !isLoadingMore) {
      fetchVideos(currentPage + 1, true);
    }
  };

  useEffect(() => {
    fetchVideos();
    fetchTags();
  }, []);

  // Filter videos based on search term and selected category
  const filteredVideos = videos.filter(video => {
    const matchesSearch = video.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          video.tags.some(tag => tag.name.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesCategory = selectedCategory === 'All' || 
                           video.tags.some(tag => tag.id === selectedCategory);
    
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="bg-gray-100 min-h-screen">
      {/* Header with search */}
      <header className="bg-white p-4 sticky top-0 z-10 shadow-sm">
        <div className="container mx-auto flex flex-col md:flex-row items-center justify-between">
          <div className="w-full md:w-1/2">
            <div className="relative">
              <input 
                type="text" 
                placeholder="Search videos..." 
                className="w-full py-2 px-4 rounded-full border focus:outline-none focus:ring-2 focus:ring-red-600"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <button className="absolute right-3 top-2">
                <svg className="w-5 h-5 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>
      
      {/* Category filters */}
      <div className="bg-white sticky top-16 z-10 shadow-sm">
        <div className="container mx-auto overflow-x-auto">
          <div className="flex space-x-4 p-2 whitespace-nowrap">
            <button 
              key="all-categories"
              className={`px-4 py-1 rounded-full text-sm ${
                selectedCategory === 'All' 
                  ? 'bg-black text-white' 
                  : 'bg-gray-200 text-black hover:bg-gray-300'
              }`}
              onClick={() => setSelectedCategory('All')}
            >
              All
            </button>
            {availableCategories?.map(category => (
              <button 
                key={category.id} 
                className={`px-4 py-1 rounded-full text-sm ${
                  selectedCategory === category.id 
                    ? 'bg-black text-white' 
                    : 'bg-gray-200 text-black hover:bg-gray-300'
                }`}
                onClick={() => setSelectedCategory(category.id)}
              >
                {category.name}
              </button>
            ))}
          </div>
        </div>
      </div>
      
      {/* Videos grid */}
      <main className="container mx-auto p-4">
        {isLoading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {filteredVideos.length > 0 ? (
                filteredVideos.map(video => (
                  <Link
                    key={video.id} 
                    className="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow cursor-pointer"
                    to={`/videos/${video.id}`}
                  >
                    {/* Thumbnail */}
                    <div className="relative">
                      <img 
                        src={video.thumbnail || thumbnail} 
                        alt={video.title} 
                        className="w-full h-48 object-cover"
                        onError={(e) => {
                          const target = e.target as HTMLImageElement;
                          target.src = thumbnail;
                        }}
                      />
                      {/* {video.duration && (
                        <div className="absolute bottom-2 right-2 bg-black bg-opacity-80 text-white text-xs px-1 py-0.5 rounded">
                          {video.duration}
                        </div>
                      )} */}
                    </div>
                    
                    {/* Video info */}
                    <div className="p-3">
                      <div className="flex">
                        <img 
                          src={thumbnail} 
                          alt={`${video.channel || 'Channel'} avatar`} 
                          className="w-9 h-9 rounded-full mr-3"
                        />
                        <div>
                          <h3 className="font-semibold text-sm line-clamp-2">{video.title}</h3>
                          <p className="text-gray-600 text-xs mt-1">{video.channel || video.category?.name}</p>
                          <p className="text-gray-600 text-xs">{video.views || 0} views • {video.date || 'Unknown date'}</p>
                        </div>
                      </div>
                    </div>
                  </Link>
                ))
              ) : (
                <div className="col-span-full text-center py-8 text-gray-500">
                  No videos found matching your search criteria.
                </div>
              )}
            </div>
            {filteredVideos.length > 0 && hasNextPage && (
              <button 
                onClick={loadMoreVideos}
                disabled={isLoadingMore}
                className="w-full mt-4 text-indigo-600 font-medium py-2 hover:bg-indigo-50 rounded-lg transition-colors disabled:opacity-50">
                {isLoadingMore ? (
                  <span className="flex items-center justify-center">
                    <span className="animate-spin h-4 w-4 mr-2 border-t-2 border-b-2 border-indigo-600 rounded-full"></span>
                    Loading...
                  </span>
                ) : (
                  "Load More Videos"
                )}
              </button>
            )}
          </>
        )}
      </main>
    </div>
  );
};

export default AllVideosPage;