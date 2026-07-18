import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import thumbnail from '../../../assets/images/thumbnail-im.jpg';

// Types
interface Video {
  id: string;
  title: string;
  description: string;
  channel: string;
  category: string;
  visibility: 'Public' | 'Unlisted' | 'Private';
  duration: number; // in seconds
  views: number;
  likes: number;
  uploadDate: string;
  tags: string[];
  thumbnail: string;
  videoUrl: string;
}

const VideoListingPage: React.FC = () => {
  // State
  const [videos, setVideos] = useState<Video[]>([]);
  const [filteredVideos, setFilteredVideos] = useState<Video[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [visibilityFilter, setVisibilityFilter] = useState<string>('');
  const [categoryFilter, setCategoryFilter] = useState<string>('');
  const [durationFilter, setDurationFilter] = useState<string>('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [availableTags, setAvailableTags] = useState<string[]>([]);
  const [availableCategories, setAvailableCategories] = useState<string[]>([]);
  const [sortBy, setSortBy] = useState<string>('uploadDate');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  // Mock data - In a real application, this would come from an API
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      const mockVideos: Video[] = [
        {
          id: '1',
          title: 'How to Build a React App with Tailwind CSS',
          description: 'In this video, we explore how to build responsive UIs with React and Tailwind CSS. We\'ll cover component structure, responsive design principles, and best practices for modern web development.',
          channel: 'WebDev Mastery',
          category: 'Web Development',
          visibility: 'Public',
          duration: 1458, // 24:18
          views: 1200000,
          likes: 45000,
          uploadDate: '2025-02-15T14:22:18Z',
          tags: ['React', 'Tailwind CSS', 'Web Development', 'Frontend'],
          thumbnail: thumbnail,
          videoUrl: 'https://www.example.com/videos/react-tailwind.mp4',
        },
        {
          id: '2',
          title: 'Advanced React Hooks Tutorial',
          description: 'Learn how to use React Hooks including useState, useEffect, useContext, useReducer, and custom hooks to build powerful functional components.',
          channel: 'React Masters',
          category: 'Web Development',
          visibility: 'Public',
          duration: 1104, // 18:24
          views: 856000,
          likes: 32000,
          uploadDate: '2025-01-20T09:15:00Z',
          tags: ['React', 'React Hooks', 'JavaScript', 'Frontend'],
          thumbnail: thumbnail,
          videoUrl: 'https://www.example.com/videos/react-hooks.mp4',
        },
        {
          id: '3',
          title: 'CSS Grid Layout Basics',
          description: 'Master CSS Grid to create responsive layouts for modern web applications with minimal code.',
          channel: 'CSS Wizards',
          category: 'Web Design',
          visibility: 'Public',
          duration: 765, // 12:45
          views: 543000,
          likes: 28000,
          uploadDate: '2025-02-10T11:30:45Z',
          tags: ['CSS', 'Grid', 'Web Design', 'Responsive Design'],
          thumbnail: thumbnail,
          videoUrl: 'https://www.example.com/videos/css-grid.mp4',
        },
        {
          id: '4',
          title: 'Build a Full-Stack App with React and Node',
          description: 'Learn how to build a complete full-stack application with React for frontend and Node.js/Express for backend. Includes authentication and database integration.',
          channel: 'Full Stack Journey',
          category: 'Full Stack',
          visibility: 'Public',
          duration: 1930, // 32:10
          views: 1800000,
          likes: 76000,
          uploadDate: '2024-10-05T16:42:30Z',
          tags: ['React', 'Node.js', 'Express', 'MongoDB', 'Full Stack'],
          thumbnail: thumbnail,
          videoUrl: 'https://www.example.com/videos/fullstack-app.mp4',
        },
        {
          id: '5',
          title: 'Introduction to TypeScript for React Developers',
          description: 'Learn how to use TypeScript with React to create type-safe components and applications.',
          channel: 'TypeScript Tutorials',
          category: 'Web Development',
          visibility: 'Private',
          duration: 1320, // 22:00
          views: 420000,
          likes: 18000,
          uploadDate: '2025-02-28T13:20:15Z',
          tags: ['TypeScript', 'React', 'JavaScript', 'Web Development'],
          thumbnail: thumbnail,
          videoUrl: 'https://www.example.com/videos/typescript-react.mp4',
        },
        {
          id: '6',
          title: 'Modern CSS Techniques Every Developer Should Know',
          description: 'Explore the latest CSS features and techniques that will revolutionize your web development workflow.',
          channel: 'CSS Wizards',
          category: 'Web Design',
          visibility: 'Unlisted',
          duration: 1860, // 31:00
          views: 640000,
          likes: 29000,
          uploadDate: '2025-03-08T10:15:45Z',
          tags: ['CSS', 'Web Design', 'Frontend', 'UI Design'],
          thumbnail: thumbnail,
          videoUrl: 'https://www.example.com/videos/modern-css.mp4',
        },
      ];

      setVideos(mockVideos);
      setFilteredVideos(mockVideos);
      setIsLoading(false);

      // Extract all unique tags
      const allTags = Array.from(
        new Set(
          mockVideos.flatMap(video => video.tags)
        )
      );
      setAvailableTags(allTags);
      console.log(allTags)

      // Extract all unique categories
      const allCategories = Array.from(
        new Set(
          mockVideos.map(video => video.category)
        )
      );
      setAvailableCategories(allCategories);
    }, 1000);
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
        video.channel.toLowerCase().includes(term) ||
        video.category.toLowerCase().includes(term)
      );
    }

    // Apply visibility filter
    if (visibilityFilter) {
      result = result.filter(video => video.visibility === visibilityFilter);
    }

    // Apply category filter
    if (categoryFilter) {
      result = result.filter(video => video.category === categoryFilter);
    }

    // Apply duration filter
    if (durationFilter) {
      switch (durationFilter) {
        case 'short':
          result = result.filter(video => video.duration < 600); // < 10 mins
          break;
        case 'medium':
          result = result.filter(video => video.duration >= 600 && video.duration < 1200); // 10-20 mins
          break;
        case 'long':
          result = result.filter(video => video.duration >= 1200); // > 20 mins
          break;
      }
    }

    // Apply tag filters
    if (selectedTags.length > 0) {
      result = result.filter(video => 
        selectedTags.some(tag => video.tags.includes(tag))
      );
    }

    // Apply sorting
    result = [...result].sort((a, b) => {
      let valA = a[sortBy as keyof Video];
      let valB = b[sortBy as keyof Video];
      
      // Handle special case for dates
      if (sortBy === 'uploadDate') {
        valA = new Date(valA as string).getTime();
        valB = new Date(valB as string).getTime();
      }
      
      if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
      if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });

    setFilteredVideos(result);
  }, [videos, searchTerm, visibilityFilter, categoryFilter, durationFilter, selectedTags, sortBy, sortOrder]);

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    }).format(date);
  };

  // Format duration (from seconds to MM:SS or HH:MM:SS)
  const formatDuration = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
      return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
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
  const toggleTag = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag)
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  // Clear all filters
  const clearFilters = () => {
    setSearchTerm('');
    setVisibilityFilter('');
    setCategoryFilter('');
    setDurationFilter('');
    setSelectedTags([]);
    setSortBy('uploadDate');
    setSortOrder('desc');
  };

  // Toggle sort order
  const toggleSortOrder = () => {
    setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc');
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
              placeholder="Search by title, description, or channel"
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
                <option key={category} value={category}>{category}</option>
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

          <div>
            <label htmlFor="duration" className="block text-sm font-medium text-gray-700 mb-1">
              Duration
            </label>
            <select
              id="duration"
              value={durationFilter}
              onChange={(e) => setDurationFilter(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">All Durations</option>
              <option value="short">Short ( 10 mins)</option>
              <option value="medium">Medium (10-20 mins)</option>
              <option value="long">Long ( 20 mins)</option>
            </select>
          </div>

          <div>
            <label htmlFor="sortBy" className="block text-sm font-medium text-gray-700 mb-1">
              Sort By
            </label>
            <div className="flex">
              <select
                id="sortBy"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-l-md"
              >
                <option value="uploadDate">Upload Date</option>
                <option value="title">Title</option>
                <option value="views">Views</option>
                <option value="likes">Likes</option>
                <option value="duration">Duration</option>
              </select>
              <button
                onClick={toggleSortOrder}
                className="px-3 py-2 border border-gray-300 border-l-0 rounded-r-md bg-gray-50"
                title={sortOrder === 'asc' ? 'Ascending' : 'Descending'}
              >
                {sortOrder === 'asc' ? (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12"></path>
                  </svg>
                ) : (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4"></path>
                  </svg>
                )}
              </button>
            </div>
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
                key={tag}
                onClick={() => toggleTag(tag)}
                className={`px-3 py-1 rounded-full text-sm ${
                  selectedTags.includes(tag)
                    ? 'bg-indigo-100 text-indigo-800 border border-indigo-300'
                    : 'bg-gray-100 text-gray-800 border border-gray-200 hover:bg-gray-200'
                }`}
              >
                {tag}
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
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell">
                    Kab
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden lg:table-cell">
                    Category
                  </th>
                  <th scope="col" className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider hidden sm:table-cell">
                    Duration
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
                          <div className="absolute bottom-1 right-1 bg-black bg-opacity-75 text-white text-xs px-1 rounded">
                            {formatDuration(video.duration)}
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">{video.title}</div>
                          <div className="text-xs text-gray-500 truncate max-w-xs">{video.description}</div>
                          <div className="mt-1 flex flex-wrap gap-1 sm:hidden">
                            {video.tags.slice(0, 2).map(tag => (
                              <span key={tag} className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-100 text-indigo-800">
                                {tag}
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
                    <td className="px-6 py-4 whitespace-nowrap hidden md:table-cell">
                      <div className="text-sm text-gray-900">{video.channel}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap hidden lg:table-cell">
                      <div className="text-sm text-gray-900">{video.category}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-500 hidden sm:table-cell">
                      {formatDuration(video.duration)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-500 hidden lg:table-cell">
                      {formatViews(video.views)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap hidden sm:table-cell">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full text-center
                        ${video.visibility === 'Public' ? 'bg-green-100 text-green-800' : 
                          video.visibility === 'Unlisted' ? 'bg-yellow-100 text-yellow-800' : 
                          'bg-gray-100 text-gray-800'}`}>
                        {video.visibility}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 hidden md:table-cell">
                      {formatDate(video.uploadDate)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <Link
                        to={`/videos/${video.id}`}
                        className="text-indigo-600 hover:text-indigo-900 mr-4"
                        target="_blank"
                      >
                        View
                      </Link>
                      <Link
                        to={`/admin/video-edit/${video.id}`}
                        className="text-gray-600 hover:text-gray-900 mr-4"
                      >
                        Edit
                      </Link>
                      <button
                        className="text-red-600 hover:text-red-900"
                        onClick={() => {
                          if (window.confirm('Are you sure you want to delete this video?')) {
                            console.log('Deleting video:', video.id);
                            // In a real app, you would call an API here
                          }
                        }}
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
    </div>
  );
};

export default VideoListingPage;