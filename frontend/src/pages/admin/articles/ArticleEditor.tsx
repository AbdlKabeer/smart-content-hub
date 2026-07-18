import React, { useState, useEffect, useRef, ChangeEvent, FormEvent } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../../context/authContext';
import { Save, Upload, Link as LinkIcon, FileText, X, Loader } from 'lucide-react';

interface ArticleData {
  title: string;
  authors: string;
  publish_date: string;
  text: string;
  meta_description: string;
  content_type: 'written' | 'pdf' | 'external';
  pdf_file: File | null;
  external_link: string;
  top_image: File | null;
}


const ArticleEditor: React.FC = () => {
  const { id } = useParams<any>();
  const navigate = useNavigate();
  const { fetchWithAuth, displayNotification } = useAuth();
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [article, setArticle] = useState<ArticleData>({
    title: '',
    authors: '',
    publish_date: '',
    text: '',
    meta_description: '',
    content_type: 'written',
    pdf_file: null,
    external_link: '',
    top_image: null,
  });

  const [previewImage, setPreviewImage] = useState<string | null>(null);
  const [originalContentType, setOriginalContentType] = useState<'written' | 'pdf' | 'external'>('written');

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        setIsLoading(true);
        const response = await fetchWithAuth({
          method: 'GET',
          path: `/admin/articles/${id}/edit/`,
        });

        let formattedDate = '';
        if (response.publish_date) {
          const date = new Date(response.publish_date);
          formattedDate = date.toISOString().split('T')[0];
        }

        setArticle({
          title: response.title || '',
          authors: response.authors || '',
          publish_date: formattedDate,
          text: response.text || '',
          meta_description: response.meta_description || '',
          content_type: response.content_type || 'written',
          pdf_file: null,
          external_link: response.external_link || '',
          top_image: null,
        });

        setOriginalContentType(response.content_type || 'written');

        if (response.top_image) {
          setPreviewImage(response.top_image);
        }

        setIsLoading(false);
      } catch (err) {
        console.error('Error fetching article:', err);
        setIsLoading(false);
        displayNotification('error', 'Failed to load article for editing');
        navigate('/admin/articles');
      }
    };

    fetchArticle();
  }, [id, fetchWithAuth, navigate]);

  const handleContentTypeChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (originalContentType && originalContentType !== e.target.value) {
      const confirmed = window.confirm(
        "Changing content type might result in loss of content. Are you sure you want to proceed?"
      );
      if (!confirmed) return;
    }

    setArticle({ ...article, content_type: e.target.value as ArticleData['content_type'] });
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setArticle({ ...article, [name]: value });
  };

  const handleImageUpload = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setPreviewImage(reader.result as string);
      reader.readAsDataURL(file);
      setArticle({ ...article, top_image: file });
    }
  };

  const handlePdfUpload = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setArticle({ ...article, pdf_file: file });
    }
  };

  const clearImage = () => {
    setPreviewImage(null);
    setArticle({ ...article, top_image: null });
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const validateForm = (): boolean => {
    if (!article.title.trim()) {
      displayNotification('error', 'Title is required');
      return false;
    }

    if (!article.authors.trim()) {
      displayNotification('error', 'At least one author is required');
      return false;
    }

    if (article.content_type === 'written' && !article.text.trim()) {
      displayNotification('error', 'Article content is required for written articles');
      return false;
    }

    if (article.content_type === 'external' && !article.external_link.trim()) {
      displayNotification('error', 'External link is required for external type articles');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!validateForm()) return;
    setIsSubmitting(true);

    try {
      const formData = new FormData();
      formData.append('title', article.title);
      formData.append('authors', article.authors);
      formData.append('publish_date', article.publish_date);
      formData.append('content_type', article.content_type);
      formData.append('meta_description', article.meta_description);

      if (article.content_type === 'written') {
        formData.append('text', article.text);
      } else if (article.content_type === 'pdf' && article.pdf_file) {
        formData.append('pdf_file', article.pdf_file);
      } else if (article.content_type === 'external') {
        formData.append('external_link', article.external_link);
      }

      if (article.top_image) {
        formData.append('top_image', article.top_image);
      }

      if (previewImage === null) {
        formData.append('remove_image', 'true');
      }

      await fetchWithAuth({
        method: 'PATCH',
        path: `/admin/articles/${id}/edit/`,
        body: formData,
        isFormData: true,
      });

      displayNotification('success', 'Article updated successfully!');
      navigate('/admin/articles');
    } catch (error) {
      console.error('Error updating article:', error);
      displayNotification('error', 'Failed to update article. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }
  return (
    <div className="container mx-auto p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold mb-6">Edit Article</h1>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Content Type Selection */}
        <div className="flex flex-col space-y-2">
          <label className="font-medium text-gray-700">Content Type</label>
          <div className="flex space-x-4">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input 
                type="radio" 
                value="written" 
                checked={article.content_type === 'written'} 
                onChange={handleContentTypeChange}
                className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300"
              />
              <span className="flex items-center"><FileText size={18} className="mr-1" /> Written Content</span>
            </label>
            
            <label className="flex items-center space-x-2 cursor-pointer">
              <input 
                type="radio" 
                value="pdf" 
                checked={article.content_type === 'pdf'} 
                onChange={handleContentTypeChange}
                className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300"
              />
              <span className="flex items-center"><Upload size={18} className="mr-1" /> PDF Document</span>
            </label>
            
            <label className="flex items-center space-x-2 cursor-pointer">
              <input 
                type="radio" 
                value="external" 
                checked={article.content_type === 'external'} 
                onChange={handleContentTypeChange}
                className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300"
              />
              <span className="flex items-center"><LinkIcon size={18} className="mr-1" /> External Link</span>
            </label>
          </div>
        </div>
        
        {/* Common Fields */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex flex-col space-y-2">
            <label htmlFor="title" className="font-medium text-gray-700">Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={article.title}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
          
          <div className="flex flex-col space-y-2">
            <label htmlFor="authors" className="font-medium text-gray-700">Authors *</label>
            <input
              type="text"
              id="authors"
              name="authors"
              value={article.authors}
              onChange={handleChange}
              placeholder="Comma separated author names"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
          
          <div className="flex flex-col space-y-2">
            <label htmlFor="publish_date" className="font-medium text-gray-700">Publish Date</label>
            <input
              type="date"
              id="publish_date"
              name="publish_date"
              value={article.publish_date}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
          
          <div className="flex flex-col space-y-2">
            <label htmlFor="meta_description" className="font-medium text-gray-700">Description</label>
            <input
              type="text"
              id="meta_description"
              name="meta_description"
              value={article.meta_description}
              onChange={handleChange}
              placeholder="Brief description of the article"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
        </div>
        
        {/* Featured Image */}
        <div className="flex flex-col space-y-2">
          <label className="font-medium text-gray-700">Featured Image</label>
          <div className="mt-1 flex items-center">
            <input
              type="file"
              ref={fileInputRef}
              accept="image/*"
              onChange={handleImageUpload}
              className="hidden"
              id="image-upload"
            />
            <label
              htmlFor="image-upload"
              className="cursor-pointer px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {previewImage ? 'Change Image' : 'Upload Image'}
            </label>
            {previewImage && (
              <div className="ml-4 relative">
                <img src={previewImage} alt="Preview" className="h-16 w-auto object-cover" />
                <button
                  type="button"
                  onClick={clearImage}
                  className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
                >
                  <X size={14} />
                </button>
              </div>
            )}
          </div>
        </div>
        
        {/* Content Type Specific Fields */}
        {article.content_type === 'written' && (
          <div className="flex flex-col space-y-2">
            <label htmlFor="text" className="font-medium text-gray-700">Article Content *</label>
            <textarea
              id="text"
              name="text"
              value={article.text}
              onChange={handleChange}
              rows={10}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            ></textarea>
          </div>
        )}
        
        {article.content_type === 'pdf' && (
          <div className="flex flex-col space-y-2">
            <label className="font-medium text-gray-700">PDF Document {originalContentType !== 'pdf' && '*'}</label>
            <div className="mt-1 flex items-center">
              <input
                type="file"
                accept="application/pdf"
                onChange={handlePdfUpload}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
                required={originalContentType !== 'pdf'}
              />
            </div>
            {article.pdf_file && (
              <p className="text-sm text-gray-500">
                Selected new file: {article.pdf_file.name}
              </p>
            )}
            {originalContentType === 'pdf' && !article.pdf_file && (
              <p className="text-sm text-gray-500">
                Current PDF file will be kept. Upload a new one to replace it.
              </p>
            )}
          </div>
        )}
        
        {article.content_type === 'external' && (
          <div className="flex flex-col space-y-2">
            <label htmlFor="external_link" className="font-medium text-gray-700">External Link *</label>
            <input
              type="url"
              id="external_link"
              name="external_link"
              value={article.external_link}
              onChange={handleChange}
              placeholder="https://example.com/article"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
        )}
        
        {/* Submit Button */}
        <div className="flex items-center justify-between pt-4">
          <button
            type="button"
            onClick={() => navigate('/admin/articles')}
            className="px-4 py-2 bg-gray-200 text-gray-700 font-medium rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
          >
            Cancel
          </button>
          
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex items-center justify-center px-6 py-3 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            {isSubmitting ? (
              <>
                <Loader size={18} className="mr-2 animate-spin" />
                Updating...
              </>
            ) : (
              <>
                <Save size={18} className="mr-2" />
                Update Article
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ArticleEditor;