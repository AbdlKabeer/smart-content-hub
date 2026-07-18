import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../../../context/authContext';

interface Tag {
  id: string;
  name: string;
}

interface Category {
  id: string;
  name: string;
  slug: string;
}

interface UploadFormData {
  title: string;
  description: string;
  category_id: string;
  tags_ids: string[];
  thumbnail: File | null;
  video_file: File | null;
}

const VideoUploadPage: React.FC = () => {
  const { fetchWithAuth, displayNotification, BACKEND_URL } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState<UploadFormData>({
    title: '',
    description: '',
    category_id: '',
    tags_ids: [],
    thumbnail: null,
    video_file: null,
  });
  const [selectedTags, setSelectedTags] = useState<Tag[]>([]);
  const [thumbnailPreview, setThumbnailPreview] = useState<string | null>(null);
  const [videoPreview, setVideoPreview] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [availableTags, setAvailableTags] = useState<Tag[]>([]);
  const [availableCategories, setAvailableCategories] = useState<Category[]>([]);
  const [selectedCategoryName, setSelectedCategoryName] = useState<string>('');
  const [showProgressModal, setShowProgressModal] = useState<boolean>(false);
  const videoInputRef = useRef<HTMLInputElement>(null);
  const thumbnailInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetchCategories();
    fetchTags();
  }, []);

  // Show/hide progress modal based on upload state
  useEffect(() => {
    if (isUploading) {
      setShowProgressModal(true);
    } else if (!isUploading && uploadProgress === 100) {
      // Keep modal open for a moment after completion
      setTimeout(() => {
        setShowProgressModal(false);
        setUploadProgress(0);
      }, 1000);
    } else if (!isUploading) {
      setShowProgressModal(false);
    }else{
      console.log(selectedCategoryName)
    }
  }, [isUploading, uploadProgress]);

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

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const categoryId = e.target.value;
    setFormData({
      ...formData,
      category_id: categoryId,
    });
    
    // Set the selected category name for display purposes
    const selectedCategory = availableCategories.find(cat => cat.id === categoryId);
    if (selectedCategory) {
      setSelectedCategoryName(selectedCategory.name);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, files } = e.target;
    if (files && files.length > 0) {
      const file = files[0];
      
      // Update the key to match the serializer field
      const fieldName = name === 'video' ? 'video_file' : name;
      
      setFormData({
        ...formData,
        [fieldName]: file,
      });

      // Create preview
      const reader = new FileReader();
      reader.onload = () => {
        if (name === 'thumbnail') {
          setThumbnailPreview(reader.result as string);
        } else if (name === 'video') {
          setVideoPreview(reader.result as string);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleTagSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const tagId = e.target.value;
    if (tagId && !formData.tags_ids.includes(tagId)) {
      const selectedTag = availableTags.find(tag => tag.id === tagId);
      if (selectedTag) {
        setSelectedTags([...selectedTags, selectedTag]);
        setFormData({
          ...formData,
          tags_ids: [...formData.tags_ids, tagId],
        });
      }
    }
    // Reset the select value
    e.target.value = '';
  };

  const handleRemoveTag = (tagId: string) => {
    setSelectedTags(selectedTags.filter(tag => tag.id !== tagId));
    setFormData({
      ...formData,
      tags_ids: formData.tags_ids.filter(id => id !== tagId),
    });
  };

  const triggerFileInput = (inputRef: React.RefObject<HTMLInputElement>) => {
    if (inputRef.current) {
      inputRef.current.click();
    }
  };


  
  

  const uploadVideo = async () => {
    setIsUploading(true);
    setUploadProgress(0);
    setUploadError(null);
    setShowProgressModal(true);
    
    try {
      // Create form data for multipart/form-data
      const formDataToSend = new FormData();
      formDataToSend.append('title', formData.title);
      formDataToSend.append('description', formData.description);
      formDataToSend.append('category_id', formData.category_id);
      

      const tags = formData.tags_ids.join(',');  // Join elements with a comma
      // Add tags as a JSON string
      formDataToSend.append('tags_ids', tags);
      
      // Add files
      if (formData.thumbnail) {
        formDataToSend.append('thumbnail', formData.thumbnail);
      }
      
      if (formData.video_file) {
        formDataToSend.append('video_file', formData.video_file);
      }

      const axiosInstance = axios.create({
        baseURL: '', // Don't set any base URL here
      });
      
      // Send the request with progress tracking
      const response = await axiosInstance.post(`${BACKEND_URL}/admin/videos/`, formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setUploadProgress(percentCompleted);
          }
        },
      });
      console.log(response)
      
      // Handle successful upload
      setUploadProgress(100); // Ensure it shows 100% completion
      displayNotification("success", 'Video uploaded successfully!');
      
      // Add a slight delay before redirecting to show 100% completion
      setTimeout(() => {
        navigate('/admin/video-list');
      }, 1000);
      
    } catch (error) {
      setUploadError('Error uploading video. Please try again.');
      displayNotification('error', 'Error uploading video. Please try again.');
      console.error('Upload error:', error);
    } finally {
      // Keep isUploading true until we redirect or handle the error
      setTimeout(() => {
        setIsUploading(false);
      }, 500);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate form
    if (!formData.title || !formData.category_id || !formData.video_file || !formData.thumbnail) {
      displayNotification('error', 'Please fill in all required fields and upload both video and thumbnail.');
      return;
    }
    
    // Upload the video
    uploadVideo();
  };

  // Progress Modal Component
  const UploadProgressModal = () => {
    if (!showProgressModal) return null;
    
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
          <h2 className="text-xl font-semibold mb-4">Uploading Video</h2>
          
          {uploadError ? (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              <p className="font-medium">Upload Failed</p>
              <p>{uploadError}</p>
              <div className="mt-4 flex justify-end">
                <button 
                  onClick={() => setShowProgressModal(false)}
                  className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                >
                  Close
                </button>
              </div>
            </div>
          ) : (
            <>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">
                  {uploadProgress < 100 ? 'Uploading...' : 'Upload Complete!'}
                </span>
                <span className="text-sm font-medium text-indigo-700">{uploadProgress}%</span>
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
                <div 
                  className={`h-4 rounded-full transition-all duration-300 ${
                    uploadProgress < 100 ? 'bg-indigo-600' : 'bg-green-500'
                  }`}
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
              
              <p className="text-sm text-gray-600 mb-4">
                {uploadProgress < 100 
                  ? "Please wait while your video is being uploaded. Do not close this window."
                  : "Upload completed successfully!"}
              </p>
              
              {/* Only show cancel button during upload, not after completion */}
              {uploadProgress < 100 && (
                <div className="flex justify-end">
                  <button
                    type="button"
                    onClick={() => {
                      // In a real app, you would also need to cancel the axios request
                      setIsUploading(false);
                      setShowProgressModal(false);
                    }}
                    className="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-gray-100 min-h-screen p-6">
      {/* Upload Progress Modal */}
      <UploadProgressModal />
      
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold mb-6">Upload New Video</h1>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                Video Title *
              </label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded focus:ring-indigo-500 focus:border-indigo-500"
                required
              />
            </div>
            
            <div>
              <label htmlFor="category_id" className="block text-sm font-medium text-gray-700 mb-1">
                Category *
              </label>
              <select
                id="category_id"
                name="category_id"
                value={formData.category_id}
                onChange={handleCategoryChange}
                className="w-full p-2 border border-gray-300 rounded focus:ring-indigo-500 focus:border-indigo-500"
                required
              >
                <option value="">Select a category</option>
                {availableCategories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
          
          {/* Description */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={4}
              className="w-full p-2 border border-gray-300 rounded focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          
          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Tags
            </label>
            <div className="flex items-center">
              <select
                onChange={handleTagSelect}
                className="flex-grow p-2 border border-gray-300 rounded focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">Select tags to add</option>
                {availableTags.map((tag) => (
                  <option 
                    key={tag.id} 
                    value={tag.id}
                    disabled={formData.tags_ids.includes(tag.id)}
                  >
                    {tag.name}
                  </option>
                ))}
              </select>
            </div>
            
            {selectedTags.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {selectedTags.map((tag) => (
                  <div 
                    key={tag.id}
                    className="bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full text-sm flex items-center"
                  >
                    {tag.name}
                    <button
                      type="button"
                      onClick={() => handleRemoveTag(tag.id)}
                      className="ml-1 text-indigo-600 hover:text-indigo-800"
                    >
                      <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        width="16" 
                        height="16" 
                        viewBox="0 0 24 24" 
                        fill="none" 
                        stroke="currentColor" 
                        strokeWidth="2" 
                        strokeLinecap="round" 
                        strokeLinejoin="round"
                      >
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          {/* File Upload Section */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Video Upload */}
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
              <input
                type="file"
                id="video"
                name="video"
                ref={videoInputRef}
                onChange={handleFileChange}
                accept="video/*"
                className="hidden"
              />
              
              {videoPreview ? (
                <div className="relative w-full pt-0 pb-0 h-0" style={{ paddingBottom: '56.25%' }}>
                  <video 
                    src={videoPreview} 
                    controls 
                    className="absolute inset-0 w-full h-full object-cover"
                  />
                  <button
                    type="button"
                    onClick={() => triggerFileInput(videoInputRef)}
                    className="mt-2 bg-indigo-500 text-white py-1 px-3 rounded text-sm hover:bg-indigo-600 absolute bottom-2 right-2"
                  >
                    Change Video
                  </button>
                </div>
              ) : (
                <div 
                  onClick={() => triggerFileInput(videoInputRef)}
                  className="cursor-pointer py-8"
                >
                  <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 4v16M17 4v16M3 8h18M3 16h18M4 12h16M8 20h8" />
                  </svg>
                  <p className="mt-1 text-sm text-gray-600">Upload Video File *</p>
                  <p className="mt-1 text-xs text-gray-500">MP4, WebM or AVI</p>
                  <button
                    type="button"
                    className="mt-2 bg-indigo-500 text-white py-1 px-3 rounded text-sm hover:bg-indigo-600"
                  >
                    Select File
                  </button>
                </div>
              )}
            </div>
            
            {/* Thumbnail Upload */}
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
              <input
                type="file"
                id="thumbnail"
                name="thumbnail"
                ref={thumbnailInputRef}
                onChange={handleFileChange}
                accept="image/*"
                className="hidden"
              />
              
              {thumbnailPreview ? (
                <div className="relative w-full pt-0 pb-0 h-0" style={{ paddingBottom: '56.25%' }}>
                  <img 
                    src={thumbnailPreview} 
                    alt="Thumbnail preview" 
                    className="absolute inset-0 w-full h-full object-cover"
                  />
                  <button
                    type="button"
                    onClick={() => triggerFileInput(thumbnailInputRef)}
                    className="mt-2 bg-indigo-500 text-white py-1 px-3 rounded text-sm hover:bg-indigo-600 absolute bottom-2 right-2"
                  >
                    Change Thumbnail
                  </button>
                </div>
              ) : (
                <div 
                  onClick={() => triggerFileInput(thumbnailInputRef)}
                  className="cursor-pointer py-8"
                >
                  <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <p className="mt-1 text-sm text-gray-600">Upload Thumbnail *</p>
                  <p className="mt-1 text-xs text-gray-500">JPG, PNG or GIF</p>
                  <button
                    type="button"
                    className="mt-2 bg-indigo-500 text-white py-1 px-3 rounded text-sm hover:bg-indigo-600"
                  >
                    Select File
                  </button>
                </div>
              )}
            </div>
          </div>
          
          
          
          {/* Action Buttons */}
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => navigate('/admin/video-list')}
              className="py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              disabled={isUploading}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isUploading}
              className={`py-2 px-4 rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
                isUploading ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'
              }`}
            >
              {isUploading ? 'Uploading...' : 'Upload Video'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default VideoUploadPage;