import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../../context/authContext';
import VideoDetails from './VideoDetails';

// Types
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


const VideoListingPage: React.FC = () => {
  const { fetchWithAuth, displayNotification } = useAuth();
  
  // State
  const [videos, setVideos] = useState<Video[]>([]);
  const [filteredVideos, setFilteredVideos] = useState<Video[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isDeleting, setIsDeleting] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [visibilityFilter, setVisibilityFilter] = useState<string>('');
  const [categoryFilter, setCategoryFilter] = useState<string>('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [availableTags, setAvailableTags] = useState<Tag[]>([]);
  const [availableCategories, setAvailableCategories] = useState<Category[]>([]);
  
  // Modal states
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [videoToDelete, setVideoToDelete] = useState<string | null>(null);
  const [showViewModal, setShowViewModal] = useState(false);
  const [videoToView, setVideoToView] = useState<Video | null>(null);

  async function fetchTags() {
    try {
        const data = await fetchWithAuth({
            method: 'GET',
            path: `/admin/tags/`,
        });
        setAvailableTags(data);
    } catch (error) {
        console.error('Error fetching tags:', error);
        displayNotification("error", "Failed to fetch tags.");
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
        displayNotification("error", "Failed to fetch categories.");
    }
  }

  async function fetchVideos() {
    try {
        const data: ApiResponse = await fetchWithAuth({
            method: 'GET',
            path: `/admin/videos/`,
        });
        
        // Set default status if not provided in API
        const videosWithStatus = data.results.map(video => ({
            ...video,
            status: video.status || 'Public' // Default to 'Public' if status is not provided
        }));
        
        setVideos(videosWithStatus);
    } catch (error) {
        console.error('Error fetching videos:', error);
        displayNotification("error", "Failed to fetch videos.");
    } finally {
        setIsLoading(false);
    }
  }

  useEffect(() => {
    fetchVideos();
    fetchTags();
    fetchCategories();
  }, []);

  // Apply filters and sorting
  useEffect(() => {
    let result = videos;

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      result = result.filter(video => 
        video.title.toLowerCase().includes(term) || 
        video.description.toLowerCase().includes(term) ||
        video.category?.name.toLowerCase().includes(term)
      );
    }

    // Apply visibility filter
    if (visibilityFilter) {
      result = result.filter(video => video.status === visibilityFilter);
    }

    // Apply category filter
    if (categoryFilter) {
      result = result.filter(video => video.category?.id === categoryFilter);
    }

    // Apply tag filters
    if (selectedTags.length > 0) {
      result = result.filter(video => 
        selectedTags.some(tagId => video.tags?.some(tag => tag.id === tagId))
      );
    }

    setFilteredVideos(result);
  }, [videos, searchTerm, visibilityFilter, categoryFilter, selectedTags]);

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    }).format(date);
  };


  // Format view count
  const formatViews = (viewCount: number) => {
    if (viewCount >= 1000000) {
      return `${(viewCount / 1000000).toFixed(1)}M`;
    } else if (viewCount >= 1000) {
      return `${(viewCount / 1000).toFixed(1)}K`;
    } else {
      return viewCount.toString();
    }
  };

  // Toggle tag selection
  const toggleTag = (tagId: string) => {
    setSelectedTags(prev => 
      prev.includes(tagId)
        ? prev.filter(t => t !== tagId)
        : [...prev, tagId]
    );
  };

  // Clear all filters
  const clearFilters = () => {
    setSearchTerm('');
    setVisibilityFilter('');
    setCategoryFilter('');
    setSelectedTags([]);
  };

  // Handle delete confirmation
  const handleDeleteClick = (videoId: string) => {
    setVideoToDelete(videoId);
    setShowDeleteModal(true);
  };

  // Confirm delete
  const confirmDelete = async () => {
    if (videoToDelete) {
      
      try {
        setIsDeleting(true)
        await fetchWithAuth({
          method: 'DELETE',
          path: `/admin/videos/${videoToDelete}/`,
        });
        
        // After successful deletion, update the videos state
        setVideos(prev => prev.filter(video => video.id !== videoToDelete));
        displayNotification("success", "Video deleted successfully.");
      } catch (error) {
        console.error('Error deleting video:', error);
        displayNotification("error", "Failed to delete video.");
      }finally{
        setIsDeleting(false)
      }
    }
    setShowDeleteModal(false);
    setVideoToDelete(null);
  };

  // Handle view video
  const handleViewClick = (video: Video) => {
    setVideoToView(video);
    setShowViewModal(true);
  };

  // Close view modal
  const closeViewModal = () => {
    setShowViewModal(false);
    setVideoToView(null);
  };

  return (
    <div className="max-w-7xl mx-auto p-6 bg-gray-50 min-h-screen">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">Video Library</h1>
          <p className="text-gray-600 mt-1">Manage and organize your videos</p>
        </div>
        <div className="mt-4 md:mt-0">
          <Link 
            to="/admin/video-upload" 
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Upload New Video
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
            <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
              Category
            </label>
            <select
              id="category"
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">All Categories</option>
              {availableCategories.map(category => (
                <option key={category.id} value={category.id}>{category.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="visibility" className="block text-sm font-medium text-gray-700 mb-1">
              Visibility
            </label>
            <select
              id="visibility"
              value={visibilityFilter}
              onChange={(e) => setVisibilityFilter(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">All</option>
              <option value="Public">Public</option>
              <option value="Unlisted">Unlisted</option>
              <option value="Private">Private</option>
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

      {/* Videos listing */}
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      ) : filteredVideos.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm p-12 text-center">
          <h3 className="text-lg font-medium text-gray-700 mb-2">No videos found</h3>
          <p className="text-gray-500">Try adjusting your filter criteria or upload a new video.</p>
        </div>
      ) : (
        <div className="overflow-hidden bg-white shadow-sm rounded-lg">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Video
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden lg:table-cell">
                    Category
                  </th>
                  <th scope="col" className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider hidden lg:table-cell">
                    Views
                  </th>
                  <th scope="col" className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider hidden sm:table-cell">
                    Status
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell">
                    Uploaded
                  </th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredVideos.map((video) => (
                  <tr key={video.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-16 w-24 relative">
                          <img 
                            className="h-full w-full object-cover rounded" 
                            src={video.thumbnail} 
                            alt={video.title} 
                          />
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">{video.title}</div>
                          <div className="text-xs text-gray-500 truncate max-w-xs">{video.description}</div>
                          <div className="mt-1 flex flex-wrap gap-1 sm:hidden">
                            {video.tags.slice(0, 2).map(tag => (
                              <span key={tag.id} className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-100 text-indigo-800">
                                {tag.name}
                              </span>
                            ))}
                            {video.tags.length > 2 && (
                              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                                +{video.tags.length - 2}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap hidden lg:table-cell">
                      <div className="text-sm text-gray-900">{video.category?.name || 'Uncategorized'}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-500 hidden lg:table-cell">
                      {formatViews(video.views)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap hidden sm:table-cell">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full text-center
                        ${video.status === 'Public' ? 'bg-green-100 text-green-800' : 
                          video.status === 'Unlisted' ? 'bg-yellow-100 text-yellow-800' : 
                          'bg-gray-100 text-gray-800'}`}>
                        {video.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 hidden md:table-cell">
                      {formatDate(video.created_at)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleViewClick(video)}
                        className="text-indigo-600 hover:text-indigo-900 mr-4"
                      >
                        View
                      </button>
                      <Link
                        to={`/admin/video-edit/${video.id}`}
                        className="text-gray-600 hover:text-gray-900 mr-4"
                      >
                        Edit
                      </Link>
                      <button
                        className="text-red-600 hover:text-red-900"
                        onClick={() => handleDeleteClick(video.id)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6 shadow-xl">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Confirm Deletion</h3>
            <p className="text-gray-600 mb-6">
              Are you sure you want to delete this video? This action cannot be undone.
            </p>
            <div className="flex justify-end space-x-4">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={confirmDelete}
                className={`px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 ${
                  isDeleting ? 'opacity-50 cursor-not-allowed' : ''
                }`}
                disabled={isDeleting}
              >
                {isDeleting ? 'Processing...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}


      {/* Video View Modal */}
      {showViewModal && videoToView && (
        <VideoDetails video={videoToView} onClose={closeViewModal} />
      )}
    </div>
  );
};

export default VideoListingPage;