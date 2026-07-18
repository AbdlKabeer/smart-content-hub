import React from 'react';

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
    status?: 'Public' | 'Unlisted' | 'Private'; // Making optional as it's not in your API response
  }

interface VideoDetailsProps {
  video: Video;
  onClose: () => void;
}


const VideoDetails: React.FC<VideoDetailsProps> = ({ video, onClose }) => {


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
  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full shadow-xl">
            <div className="p-4 border-b border-gray-200 flex justify-between items-center">
              <h3 className="text-lg font-medium text-gray-900">{video.title}</h3>
              <button 
                onClick={onClose}
                className="text-gray-500 hover:text-gray-700"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            <div className="p-0 bg-black">
              <div className="relative pt-[56.25%]"> {/* 16:9 aspect ratio */}
                <video 
                  className="absolute inset-0 w-full h-full"
                  controls
                  poster={video.thumbnail}
                  src={video.video_file}
                >
                  Your browser does not support the video tag.
                </video>
              </div>
            </div>
            <div className="p-4">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h4 className="text-xl font-semibold mb-1">{video.title}</h4>
                  <p className="text-gray-500 text-sm">
                    {formatViews(video.views)} views • Uploaded {formatDate(video.created_at)}
                  </p>
                </div>
                <span className={`px-2 py-1 text-xs font-semibold rounded-full
                  ${video.status === 'Public' ? 'bg-green-100 text-green-800' : 
                    video.status === 'Unlisted' ? 'bg-yellow-100 text-yellow-800' : 
                    'bg-gray-100 text-gray-800'}`}>
                  {video.status}
                </span>
              </div>
              <p className="text-gray-700 mb-4">{video.description}</p>
              <div className="flex flex-wrap gap-2 mb-2">
                {video.tags.map(tag => (
                  <span key={tag.id} className="px-2 py-1 bg-gray-100 text-gray-800 text-xs rounded-full">
                    {tag.name}
                  </span>
                ))}
              </div>
              <div className="border-t border-gray-200 pt-4 flex justify-end">
                <button
                  onClick={onClose}
                  className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>

  );
};


export default VideoDetails;