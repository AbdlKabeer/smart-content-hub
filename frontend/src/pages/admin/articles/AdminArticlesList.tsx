import React, { useState, useEffect, FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { 
  Plus, FileText, File, Link as LinkIcon, 
  Edit, Trash2, Eye, Search, Filter 
} from 'lucide-react';
import { useAuth } from '../../../context/authContext';

type ContentType = 'written' | 'pdf' | 'external';

interface Article {
  id: number;
  title: string;
  authors: string;
  publish_date: string;
  content_type: ContentType;
  likes_count?: number;
  top_image?: string;
}

interface FetchResponse {
  results: Article[];
  metadata: {
    count: number;
    page: number;
    page_size: number;
  };
}

const AdminArticlesList: React.FC = () => {
  const { fetchWithAuth, displayNotification } = useAuth();

  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [contentTypeFilter, setContentTypeFilter] = useState<ContentType | ''>('');
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);

  const fetchArticles = async (page = 1): Promise<void> => {
    try {
      setLoading(true);

      let queryParams = `page=${page}&page_size=10`;
      if (searchQuery) queryParams += `&search=${encodeURIComponent(searchQuery)}`;
      if (contentTypeFilter) queryParams += `&content_type=${contentTypeFilter}`;

      const response: FetchResponse = await fetchWithAuth({
        method: 'GET',
        path: `/admin/articles/?${queryParams}`,
      });

      setArticles(response.results);
      setTotalPages(Math.ceil(response.metadata.count / response.metadata.page_size));
      setCurrentPage(response.metadata.page);
    } catch (err) {
      console.error('Error fetching articles:', err);
      displayNotification('error', 'Failed to load articles');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArticles();
  }, []);

  const handleSearch = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    fetchArticles(1);
  };

  const handleDelete = async (id: number, title: string): Promise<void> => {
    if (window.confirm(`Are you sure you want to delete "${title}"?`)) {
      try {
        await fetchWithAuth({
          method: 'DELETE',
          path: `/admin/articles/${id}/`,
        });

        setArticles(prev => prev.filter(article => article.id !== id));
        displayNotification('success', 'Article deleted successfully');
      } catch (err) {
        console.error('Error deleting article:', err);
        displayNotification('error', 'Failed to delete article');
      }
    }
  };

  const getContentTypeIcon = (type: ContentType): JSX.Element => {
    switch (type) {
      case 'written':
        return <FileText size={18} className="text-blue-500" />;
      case 'pdf':
        return <File size={18} className="text-red-500" />;
      case 'external':
        return <LinkIcon size={18} className="text-green-500" />;
      default:
        return <FileText size={18} />;
    }
  };

  const getContentTypeName = (type: ContentType): string => {
    switch (type) {
      case 'written':
        return 'Written';
      case 'pdf':
        return 'PDF';
      case 'external':
        return 'External Link';
      default:
        return 'Unknown';
    }
  };
  
  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Articles</h1>
        <Link 
          to="/admin/article-create"
          className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
        >
          <Plus size={18} className="mr-2" />
          Create New Article
        </Link>
      </div>
      
      {/* Search and Filter */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <input
                type="text"
                placeholder="Search articles..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border rounded-md focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500"
              />
              <Search 
                size={18} 
                className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" 
              />
            </div>
          </div>
          
          <div className="w-full md:w-56">
            <div className="relative">
              <select
                value={contentTypeFilter}
                onChange={(e) => setContentTypeFilter(e.target.value as ContentType | '')}
                className="w-full pl-10 pr-4 py-2 border rounded-md appearance-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500"
              >
                <option value="">All Types</option>
                <option value="written">Written Content</option>
                <option value="pdf">PDF Document</option>
                <option value="external">External Link</option>
              </select>
              <Filter 
                size={18} 
                className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" 
              />
            </div>
          </div>
          
          <button
            type="submit"
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Search
          </button>
        </form>
      </div>
      
      {/* Articles Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          </div>
        ) : articles.length === 0 ? (
          <div className="text-center py-12">
            <FileText size={48} className="mx-auto text-gray-400 mb-4" />
            <h2 className="text-xl font-semibold text-gray-600">No articles found</h2>
            <p className="text-gray-500 mt-2">
              {searchQuery || contentTypeFilter ? 
                'Try changing your search or filter criteria.' : 
                'Create your first article to get started.'}
            </p>
            {!searchQuery && !contentTypeFilter && (
              <Link 
                to="/admin/article-create"
                className="mt-4 inline-block px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              >
                <Plus size={18} className="mr-2 inline" />
                Create New Article
              </Link>
            )}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Title
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Author
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Published
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Likes
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {articles.map(article => (
                  <tr key={article.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {article.top_image ? (
                          <img 
                            src={article.top_image} 
                            alt="" 
                            className="h-10 w-10 rounded-md object-cover mr-3"
                          />
                        ) : (
                          <div className="h-10 w-10 rounded-md bg-gray-200 flex items-center justify-center mr-3">
                            {getContentTypeIcon(article.content_type)}
                          </div>
                        )}
                        <div className="text-sm font-medium text-gray-900 max-w-xs truncate">
                          {article.title}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {getContentTypeIcon(article.content_type)}
                        <span className="ml-1 text-sm text-gray-900">
                          {getContentTypeName(article.content_type)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {article.authors}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(article.publish_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {article.likes_count || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex justify-end space-x-2">
                        <Link 
                          to={`/articles/${article.id}`}
                          className="text-indigo-600 hover:text-indigo-900"
                          title="View"
                        >
                          <Eye size={18} />
                        </Link>
                        <Link 
                          to={`/admin/article-edit/${article.id}`}
                          className="text-blue-600 hover:text-blue-900"
                          title="Edit"
                        >
                          <Edit size={18} />
                        </Link>
                        <button
                          onClick={() => handleDelete(article.id, article.title)}
                          className="text-red-600 hover:text-red-900"
                          title="Delete"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        
        {/* Pagination */}
        {!loading && totalPages > 1 && (
          <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700">
                  Showing page <span className="font-medium">{currentPage}</span> of{" "}
                  <span className="font-medium">{totalPages}</span> pages
                </p>
              </div>
              <div>
                <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                  <button
                    onClick={() => fetchArticles(currentPage - 1)}
                    disabled={currentPage === 1}
                    className={`relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium ${
                      currentPage === 1 
                        ? 'text-gray-300 cursor-not-allowed' 
                        : 'text-gray-500 hover:bg-gray-50'
                    }`}
                  >
                    <span className="sr-only">Previous</span>
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </button>
                  
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    const pageNum = Math.max(1, Math.min(currentPage - 2 + i, totalPages));
                    return (
                      <button
                        key={pageNum}
                        onClick={() => fetchArticles(pageNum)}
                        className={`relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
                          currentPage === pageNum
                            ? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600'
                            : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}
                  
                  <button
                    onClick={() => fetchArticles(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    className={`relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium ${
                      currentPage === totalPages 
                        ? 'text-gray-300 cursor-not-allowed' 
                        : 'text-gray-500 hover:bg-gray-50'
                    }`}
                  >
                    <span className="sr-only">Next</span>
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                    </svg>
                  </button>
                </nav>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}


export default AdminArticlesList;