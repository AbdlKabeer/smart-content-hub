import React, { useState, useEffect } from 'react';
// import avatar from '../../../assets/images/thumbnail-im.jpg';
import { useAuth } from '../../../context/authContext';

// Updated Types to match actual API response
interface Student {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  previous_year_performance: string | null;
  preferred_content: string;
  study_preference: string | null;
  current_year_level: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
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
  results: Student[];
}

// Confirmation Modal Component
const ConfirmationModal: React.FC<{
  isOpen: boolean;
  title: string;
  message: string;
  confirmText: string;
  cancelText: string;
  confirmButtonClass: string;
  onConfirm: () => void;
  onCancel: () => void;
}> = ({ isOpen, title, message, confirmText, cancelText, confirmButtonClass, onConfirm, onCancel }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full p-6">
        <h3 className="text-lg font-bold mb-2">{title}</h3>
        <p className="mb-6 text-gray-600">{message}</p>
        <div className="flex justify-end space-x-3">
          <button
            onClick={onCancel}
            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            className={`px-4 py-2 text-white rounded-md ${confirmButtonClass}`}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
};

// Student View Modal Component - Updated to match new Student interface
const StudentViewModal: React.FC<{
  student: Student | null;
  closeModal: () => void;
  onStatusChange: (studentId: string, newStatus: boolean) => void;
  onDeleteStudent: (studentId: string) => void;
}> = ({ student, closeModal, onStatusChange, onDeleteStudent }) => {
  const [showStatusConfirmation, setShowStatusConfirmation] = useState(false);
  const [showDeleteConfirmation, setShowDeleteConfirmation] = useState(false);

  if (!student) return null;

  const handleStatusChange = () => {
    onStatusChange(student.id, !student.is_active);
    setShowStatusConfirmation(false);
    closeModal();
  };

  const handleDeleteStudent = () => {
    onDeleteStudent(student.id);
    setShowDeleteConfirmation(false);
    closeModal();
  };

  const isActive = student.is_active;
  const fullName = `${student.first_name} ${student.last_name}`;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-start">
            <h2 className="text-2xl font-bold">{fullName}</h2>
            <button
              onClick={closeModal}
              className="text-gray-500 hover:text-gray-700 focus:outline-none"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-1">
              {/* <img 
                src={avatar} 
                alt={fullName} 
                className="h-48 w-48 rounded-full mx-auto object-cover" 
              /> */}
              <div className="h-48 w-48 rounded-full bg-blue-500 text-white flex items-center justify-center text-5xl font-semibold mx-auto">
                {`${student?.first_name[0]}${student?.last_name[0]}`}
              </div>
              
              <div className="mt-4 text-center">
                <span className={`px-3 py-1 inline-flex text-sm font-medium rounded-full 
                  ${isActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}
                >
                  {isActive ? 'Active' : 'Inactive'}
                </span>
              </div>
            </div>

            <div className="md:col-span-2">
              <h3 className="text-lg font-medium border-b pb-2 mb-4">Student Information</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">Email</p>
                  <p className="font-medium">{student.email}</p>
                </div>
                
                <div>
                  <p className="text-sm text-gray-500">Phone Number</p>
                  <p className="font-medium">{student.phone_number}</p>
                </div>
                
                <div>
                  <p className="text-sm text-gray-500">Year Level</p>
                  <p className="font-medium">{student.current_year_level}</p>
                </div>
                
                <div>
                  <p className="text-sm text-gray-500">Preferred Content</p>
                  <p className="font-medium">{student.preferred_content}</p>
                </div>
                
                <div>
                  <p className="text-sm text-gray-500">Registration Date</p>
                  <p className="font-medium">{new Date(student.created_at).toLocaleDateString()}</p>
                </div>

                {student.study_preference && (
                  <div>
                    <p className="text-sm text-gray-500">Study Preference</p>
                    <p className="font-medium">{student.study_preference}</p>
                  </div>
                )}
              </div>

              {student.previous_year_performance && (
                <>
                  <h3 className="text-lg font-medium border-b pb-2 mt-6 mb-4">Performance</h3>
                  <p className="font-medium">{student.previous_year_performance}</p>
                </>
              )}
            </div>
          </div>

          <div className="mt-8 flex flex-wrap justify-end space-x-3">
            <button
              onClick={closeModal}
              className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
            >
              Close
            </button>
            <button
              onClick={() => setShowStatusConfirmation(true)}
              className={`px-4 py-2 text-white rounded-md ${
                isActive ? 'bg-orange-500 hover:bg-orange-600' : 'bg-green-500 hover:bg-green-600'
              }`}
            >
              {isActive ? 'Disable Account' : 'Enable Account'}
            </button>
            <button
              onClick={() => setShowDeleteConfirmation(true)}
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
            >
              Delete Account
            </button>
          </div>
        </div>
      </div>

      {/* Status Change Confirmation Modal */}
      <ConfirmationModal
        isOpen={showStatusConfirmation}
        title={isActive ? 'Disable Student Account' : 'Enable Student Account'}
        message={isActive 
          ? `Are you sure you want to disable ${fullName}'s account? They will no longer be able to access the system.`
          : `Are you sure you want to enable ${fullName}'s account? They will regain access to the system.`
        }
        confirmText={isActive ? 'Disable Account' : 'Enable Account'}
        cancelText="Cancel"
        confirmButtonClass={isActive ? 'bg-orange-500 hover:bg-orange-600' : 'bg-green-500 hover:bg-green-600'}
        onConfirm={handleStatusChange}
        onCancel={() => setShowStatusConfirmation(false)}
      />

      {/* Delete Confirmation Modal */}
      <ConfirmationModal
        isOpen={showDeleteConfirmation}
        title="Delete Student Account"
        message={`Are you sure you want to permanently delete ${fullName}'s account? This action cannot be undone.`}
        confirmText="Delete Account"
        cancelText="Cancel"
        confirmButtonClass="bg-red-600 hover:bg-red-700"
        onConfirm={handleDeleteStudent}
        onCancel={() => setShowDeleteConfirmation(false)}
      />
    </div>
  );
};

const StudentListingPage: React.FC = () => {
  // State
  const { fetchWithAuth, displayNotification } = useAuth();
  const [students, setStudents] = useState<Student[]>([]);
  const [filteredStudents, setFilteredStudents] = useState<Student[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [nextPageUrl, setNextPageUrl] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [yearLevelFilter, setYearLevelFilter] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [contentPreferenceFilter, setContentPreferenceFilter] = useState<string>('');
  const [availableYearLevels, setAvailableYearLevels] = useState<string[]>([]);
  const [availableContentPreferences, setAvailableContentPreferences] = useState<string[]>([]);
  const [viewingStudent, setViewingStudent] = useState<Student | null>(null);

  // Fetch students data
  useEffect(() => {
    fetchStudents();
  }, []);

  // Method to fetch students
  const fetchStudents = async (page: number = 1) => {
    try {
      setIsLoading(true);
      const response = await fetchWithAuth({
        method: 'GET',
        path: `/admin/students?page=${page}&page_size=20`,
      });
      
      const data: ApiResponse = response;
      
      if (page === 1) {
        setStudents(data?.results || []);
        setFilteredStudents(data?.results || []);
      } else {
        const updatedStudents = [...students, ...data?.results];
        setStudents(updatedStudents);
        setFilteredStudents(updatedStudents);
      }
      
      setNextPageUrl(data.metadata.next);
      setCurrentPage(data.metadata.page);
      
      // Extract all unique year levels
      const allYearLevels = Array.from(
        new Set(
          data?.results.map(student => student.current_year_level).filter(Boolean) as string[]
        )
      );
      setAvailableYearLevels(allYearLevels);

      // Extract all unique content preferences
      const allContentPreferences = Array.from(
        new Set(
          data?.results.map(student => student.preferred_content).filter(Boolean) as string[]
        )
      );
      setAvailableContentPreferences(allContentPreferences);
      
      setIsLoading(false);
    } catch (err) {
      console.error('Error fetching students:', err);
      setIsLoading(false);
      displayNotification('error', 'Failed to fetch students');
    }
  };

  // Apply filters
  useEffect(() => {
    let result = students;

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      result = result.filter(student => 
        `${student.first_name} ${student.last_name}`.toLowerCase().includes(term) || 
        student.email.toLowerCase().includes(term)
      );
    }

    // Apply year level filter
    if (yearLevelFilter) {
      result = result.filter(student => student.current_year_level === yearLevelFilter);
    }

    // Apply status filter
    if (statusFilter !== '') {
      const isActive = statusFilter === 'Active';
      result = result.filter(student => student.is_active === isActive);
    }

    // Apply content preference filter
    if (contentPreferenceFilter) {
      result = result.filter(student => student.preferred_content === contentPreferenceFilter);
    }

    setFilteredStudents(result);
  }, [students, searchTerm, yearLevelFilter, statusFilter, contentPreferenceFilter]);

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    }).format(date);
  };

  // Clear all filters
  const clearFilters = () => {
    setSearchTerm('');
    setYearLevelFilter('');
    setStatusFilter('');
    setContentPreferenceFilter('');
  };

  // Handle student status change
  const handleStatusChange = async (studentId: string, isActive: boolean) => {
    try {
      // In a real app, make API call to update student status
      // await fetchWithAuth({
      //   method: 'PATCH',
      //   path: `/admin/students/${studentId}/`,
      //   body: { is_active: isActive }
      // });

      // Update local state
      const updatedStudents = students.map(student => 
        student.id === studentId 
          ? { ...student, is_active: isActive } 
          : student
      );
      
      setStudents(updatedStudents);
      displayNotification('success', `Student status updated successfully`);
    } catch (err) {
      console.error('Error updating student status:', err);
      displayNotification('error', 'Failed to update student status');
    }
  };

  // Handle student deletion
  const handleDeleteStudent = async (studentId: string) => {
    try {
      // In a real app, make API call to delete student
      // await fetchWithAuth({
      //   method: 'DELETE',
      //   path: `/admin/students/${studentId}/`
      // });

      // Update local state
      const updatedStudents = students.filter(student => student.id !== studentId);
      setStudents(updatedStudents);
      displayNotification('success', 'Student deleted successfully');
    } catch (err) {
      console.error('Error deleting student:', err);
      displayNotification('error', 'Failed to delete student');
    }
  };

  // Open student view modal
  const openStudentView = (student: Student) => {
    setViewingStudent(student);
  };

  // Close student view modal
  const closeStudentView = () => {
    setViewingStudent(null);
  };

  // Load more students
  const loadMoreStudents = () => {
    if (nextPageUrl) {
      fetchStudents(currentPage + 1);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6 bg-gray-50 min-h-screen">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">Students</h1>
          <p className="text-gray-600 mt-1">Browse and filter student records</p>
        </div>
        <div className="mt-4 md:mt-0">
          {/* Add button for adding new student if needed */}
        </div>
      </div>

      {/* Filters section */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
              Search
            </label>
            <input
              type="text"
              id="search"
              placeholder="Search by name or email"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label htmlFor="yearLevel" className="block text-sm font-medium text-gray-700 mb-1">
              Year Level
            </label>
            <select
              id="yearLevel"
              value={yearLevelFilter}
              onChange={(e) => setYearLevelFilter(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">All Year Levels</option>
              {availableYearLevels.map(level => (
                <option key={level} value={level}>{level}</option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              id="status"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">All Statuses</option>
              <option value="Active">Active</option>
              <option value="Inactive">Inactive</option>
            </select>
          </div>

          <div>
            <label htmlFor="contentPreference" className="block text-sm font-medium text-gray-700 mb-1">
              Content Preference
            </label>
            <select
              id="contentPreference"
              value={contentPreferenceFilter}
              onChange={(e) => setContentPreferenceFilter(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">All Content Preferences</option>
              {availableContentPreferences.map(preference => (
                <option key={preference} value={preference}>{preference}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={clearFilters}
            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
          >
            Clear Filters
          </button>
        </div>
      </div>

      {/* Students listing */}
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      ) : filteredStudents.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm p-12 text-center">
          <h3 className="text-lg font-medium text-gray-700 mb-2">No students found</h3>
          <p className="text-gray-500">Try adjusting your filter criteria or add a new student.</p>
        </div>
      ) : (
        <div className="overflow-hidden bg-white shadow-sm rounded-lg">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Student
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell">
                    Content Preference
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden sm:table-cell">
                    Year Level
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell">
                    Status
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden lg:table-cell">
                    Registration Date
                  </th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredStudents.map((student) => (
                  <tr key={student.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {/* <div className="flex-shrink-0 h-10 w-10">
                          <img className="h-10 w-10 rounded-full" src={avatar} alt="" />
                        </div> */}
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">{student.first_name} {student.last_name}</div>
                          <div className="text-sm text-gray-500">{student.email}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap hidden md:table-cell">
                      <div className="text-sm text-gray-900">{student.preferred_content}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap hidden sm:table-cell">
                      <div className="text-sm text-gray-900">{student.current_year_level}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap hidden md:table-cell">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                        ${student.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {student.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 hidden lg:table-cell">
                      {formatDate(student.created_at)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => openStudentView(student)}
                        className="text-indigo-600 hover:text-indigo-900 mr-4"
                      >
                        View
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {/* Load more button */}
          {nextPageUrl && (
            <div className="px-6 py-4 flex justify-center">
              <button 
                onClick={loadMoreStudents}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
              >
                Load More
              </button>
            </div>
          )}
        </div>
      )}

      {/* Student View Modal with Account Management */}
      {viewingStudent && (
        <StudentViewModal 
          student={viewingStudent} 
          closeModal={closeStudentView}
          onStatusChange={handleStatusChange}
          onDeleteStudent={handleDeleteStudent}
        />
      )}
    </div>
  );
};

export default StudentListingPage;