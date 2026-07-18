//@ts-nocheck
import React, { useState, useEffect } from 'react';
import thumbnail from '../assets/images/thumbnail-im.jpg'
import { useAuth } from '../context/authContext';

// Types
interface UserProfile {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  is_admin: boolean;
  created_at: string;
  role: string;
  preferred_content: string;
  study_preference: string;
  current_year_level: string;
  previous_year_performance: string;
  phone_number: string;
  avatar?: string; // Make this optional
  interests?: string[]; // Make this optional
}

interface PasswordReset {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}

// Modal types for confirmation
type ModalType = 'deleteAccount' | 'passwordUpdate' | 'dataDownload' | null;

const ProfileManagementPage: React.FC = () => {
  const { fetchWithAuth, displayNotification, setUser, setAuthToken, setGlobalLoading, setGlobalLoadingText } = useAuth(); 
  
  // Initial profile state with the correct structure
  const [profile, setProfile] = useState<UserProfile>({
    id: '',
    email: '',
    first_name: '',
    last_name: '',
    is_admin: false,
    created_at: '',
    role: '',
    preferred_content: '',
    study_preference: '',
    current_year_level: '',
    previous_year_performance: '',
    phone_number: '',
    avatar: thumbnail,
    interests: []
  });

  // Form states
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [profileForm, setProfileForm] = useState<UserProfile>({ ...profile });
  const [passwordForm, setPasswordForm] = useState<PasswordReset>({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [newInterest, setNewInterest] = useState('');
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [activeTab, setActiveTab] = useState<'profile' | 'password' | 'interests'>('profile');
  
  // Modal state
  const [modalOpen, setModalOpen] = useState<ModalType>(null);
  const [deleteConfirmText, setDeleteConfirmText] = useState('');

  // Fetch user profile after the token is available or on token update
  const fetchUserProfile = async () => {
    try {
      const data = await fetchWithAuth({
        method: 'GET',
        path: `/account/`,
      });
      console.log(data);
      
      // Ensure interests exist, even if not in API response
      const profileData = data?.data;
      if (!profileData.interests) {
        profileData.interests = [];
      }
      if (!profileData.avatar) {
        profileData.avatar = thumbnail;
      }
      
      setProfile(profileData);
      setUser(profileData);
    } catch (error) {
      console.error('Error fetching user profile:', error);
    }
  };

  // Reset forms when canceling edit modes
  useEffect(() => {
    if (!isEditingProfile) {
      setProfileForm({ ...profile });
    }
    if (!isChangingPassword) {
      setPasswordForm({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
      setFormErrors({});
    }

    fetchUserProfile();
  }, []);

  // Handle profile form changes
  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setProfileForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Handle password form changes
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPasswordForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Validate password form
  const validatePasswordForm = (): boolean => {
    const errors: Record<string, string> = {};
    
    if (!passwordForm.currentPassword) {
      errors.currentPassword = 'Current password is required';
    }
    
    if (!passwordForm.newPassword) {
      errors.newPassword = 'New password is required';
    } else if (passwordForm.newPassword.length < 8) {
      errors.newPassword = 'Password must be at least 8 characters';
    }
    
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Handle profile update
  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      // Update with real API call
      const response = await fetchWithAuth({
        method: 'PUT',
        path: '/account/',
        body: profileForm
      });
      
      setUser(response?.data || profileForm);
      setProfile(response?.data || profileForm);
      setIsEditingProfile(false);
      displayNotification?.('success','Profile updated successfully');
    } catch (error) {
      console.error('Error updating profile:', error);
      displayNotification?.('error','Failed to update profile');
    }
  };

  // Handle password form submission - now opens confirmation modal
  const handlePasswordFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validatePasswordForm()) {
      setModalOpen('passwordUpdate');
    }
  };

  // Handle password reset after confirmation
  const handlePasswordReset = async () => {
    try {
      // Implement actual API call
      await fetchWithAuth({
        method: 'POST',
        path: '/account/change-password/',
        body: {
          current_password: passwordForm.currentPassword,
          new_password: passwordForm.newPassword,
          confirm_new_password: passwordForm.newPassword
        }
      });
      
      setIsChangingPassword(false);
      setModalOpen(null);
      displayNotification?.('success','Password changed successfully');
      setPasswordForm({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
    } catch (error) {
      console.error('Error changing password:', error);
      displayNotification?.('error','Failed to change password');
    }
  };

  // Handle adding a new interest
  const handleAddInterest = () => {
    if (newInterest.trim() && !profile.interests?.includes(newInterest.trim())) {
      const updatedInterests = [...(profile.interests || []), newInterest.trim()];
      setProfile(prev => ({
        ...prev,
        interests: updatedInterests
      }));
      setNewInterest('');
      displayNotification?.('Interest added', 'success');
    } else if (profile.interests?.includes(newInterest.trim())) {
      displayNotification?.('error','Interest already exists');
    }
  };

  // Handle removing an interest
  const handleRemoveInterest = (interest: string) => {
    const updatedInterests = profile.interests?.filter(item => item !== interest) || [];
    setProfile(prev => ({
      ...prev,
      interests: updatedInterests
    }));
    displayNotification?.( 'success','Interest removed');
  };

  // Format date
  const formatDate = (dateString: string): string => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date);
  };

  // Get full name
  const getFullName = (): string => {
    return `${profile.first_name || ''} ${profile.last_name || ''}`.trim();
  };

  // Handle account deletion
  const handleDeleteAccount = async () => {
    if (deleteConfirmText === 'DELETE') {
      try {
        // Implement actual API call
        await fetchWithAuth({
          method: 'DELETE',
          path: '/account/'
        });
        
        setModalOpen(null);
        setDeleteConfirmText('');
        displayNotification?.('success','Account deleted successfully');
        setAuthToken?.(null); // Log out user
      } catch (error) {
        console.error('Error deleting account:', error);
        displayNotification?.('error','Failed to delete account');
      }
    }
  };

  // Handle data download
  const handleDataDownload = async () => {
    try {
      // Implement actual API call
      await fetchWithAuth({
        method: 'GET',
        path: '/account/download-data/'
      });
      
      displayNotification?.('Your data is being prepared and will be available for download soon.', 'success');
      setModalOpen(null);
    } catch (error) {
      console.error('Error requesting data download:', error);
      displayNotification?.( 'error','Failed to request data download');
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Profile Management</h1>
      
      {/* Tabs */}
      <div className="flex border-b mb-6">
        <button
          className={`py-2 px-4 font-medium ${activeTab === 'profile' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
          onClick={() => setActiveTab('profile')}
        >
          Profile Information
        </button>
        <button
          className={`py-2 px-4 font-medium ${activeTab === 'password' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
          onClick={() => setActiveTab('password')}
        >
          Change Password
        </button>
        {/* <button
          className={`py-2 px-4 font-medium ${activeTab === 'interests' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
          onClick={() => setActiveTab('interests')}
        >
          Interests
        </button> */}
      </div>
      
      {/* Profile Tab */}
      {activeTab === 'profile' && (
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold">Profile Information</h2>
            <button
              className={`px-4 py-2 rounded ${isEditingProfile ? 'bg-gray-200 text-gray-800' : 'px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 '}`}
              onClick={() => setIsEditingProfile(!isEditingProfile)}
            >
              {isEditingProfile ? 'Cancel' : 'Edit Profile'}
            </button>
          </div>
          
          {isEditingProfile ? (
            <form onSubmit={handleProfileUpdate}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                  <input
                    type="text"
                    name="first_name"
                    value={profileForm.first_name || ''}
                    onChange={handleProfileChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                  <input
                    type="text"
                    name="last_name"
                    value={profileForm.last_name || ''}
                    onChange={handleProfileChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    name="email"
                    value={profileForm.email || ''}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-100"
                    disabled
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                  <input
                    type="text"
                    name="phone_number"
                    value={profileForm.phone_number || ''}
                    onChange={handleProfileChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Current Year Level</label>
                  <input
                    type="text"
                    name="current_year_level"
                    disabled
                    value={profileForm.current_year_level || ''}
                    onChange={handleProfileChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Previous Year Performance</label>
                  <input
                    type="text"
                    name="previous_year_performance"
                    disabled
                    value={profileForm.previous_year_performance || ''}
                    onChange={handleProfileChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Preferred Content</label>
                  <select
                    name="preferred_content"
                    value={profileForm.preferred_content || ''}
                    onChange={handleProfileChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="">Select Preference</option>
                    <option value="Video">Video</option>
                    <option value="Article">Article</option>
                    <option value="Quiz">Quiz</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Study Preference</label>
                  <select
                    name="study_preference"
                    value={profileForm.study_preference || ''}
                    onChange={handleProfileChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="">Select Preference</option>
                    <option value="Morning">Morning</option>
                    <option value="Night">Night</option>
                  </select>
                </div>
              </div>
              
              <div className="flex justify-end mt-6">
                <button
                  type="button"
                  className="px-4 py-2 mr-3 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                  onClick={() => setIsEditingProfile(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                >
                  Save Changes
                </button>
              </div>
            </form>
          ) : (
            <div className="flex flex-col md:flex-row">
              <div className="md:w-1/3 mb-6 md:mb-0">
                {/* <img
                  src={profile.avatar || thumbnail}
                  alt={getFullName()}
                  className="w-32 h-32 rounded-full"
                /> */}
                <div className="h-48 w-48 rounded-full bg-blue-500 text-white flex items-center justify-center text-5xl font-semibold mx-auto">
                  {`${profile?.first_name[0]}${profile?.last_name[0]}`}
                </div>
                <div className="mt-4 text-sm text-gray-500">
                  Member since {formatDate(profile.created_at)}
                </div>
              </div>
              
              <div className="md:w-2/3">
                <div className="grid grid-cols-1 gap-4">
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Name</h3>
                    <p className="mt-1">{getFullName()}</p>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Email</h3>
                    <p className="mt-1">{profile.email}</p>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Phone Number</h3>
                    <p className="mt-1">{profile.phone_number || 'Not provided'}</p>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Role</h3>
                    <p className="mt-1">{profile.role || 'User'}</p>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Current Year Level</h3>
                    <p className="mt-1">{profile.current_year_level || 'Not specified'}</p>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Previous Year Performance</h3>
                    <p className="mt-1">{profile.previous_year_performance || 'Not specified'}</p>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Preferred Content</h3>
                    <p className="mt-1">{profile.preferred_content || 'Not specified'}</p>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Study Preference</h3>
                    <p className="mt-1">{profile.study_preference || 'Not specified'}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
      
      {/* Password Tab */}
      {activeTab === 'password' && (
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold">Change Password</h2>
          </div>
          
          <form onSubmit={handlePasswordFormSubmit}>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Current Password</label>
                <input
                  type="password"
                  name="currentPassword"
                  value={passwordForm.currentPassword}
                  onChange={handlePasswordChange}
                  className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                    formErrors.currentPassword ? 'border-red-500' : 'border-gray-300'
                  }`}
                />
                {formErrors.currentPassword && (
                  <p className="mt-1 text-sm text-red-600">{formErrors.currentPassword}</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">New Password</label>
                <input
                  type="password"
                  name="newPassword"
                  value={passwordForm.newPassword}
                  onChange={handlePasswordChange}
                  className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                    formErrors.newPassword ? 'border-red-500' : 'border-gray-300'
                  }`}
                />
                {formErrors.newPassword && (
                  <p className="mt-1 text-sm text-red-600">{formErrors.newPassword}</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Confirm New Password</label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={passwordForm.confirmPassword}
                  onChange={handlePasswordChange}
                  className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                    formErrors.confirmPassword ? 'border-red-500' : 'border-gray-300'
                  }`}
                />
                {formErrors.confirmPassword && (
                  <p className="mt-1 text-sm text-red-600">{formErrors.confirmPassword}</p>
                )}
              </div>
            </div>
            
            <div className="mt-6">
              <button
                type="submit"
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              >
                Update Password
              </button>
            </div>
          </form>
          
          <div className="mt-6 p-4 bg-yellow-50 border border-yellow-100 rounded-md">
            <h3 className="text-sm font-medium text-yellow-800">Password requirements:</h3>
            <ul className="mt-2 text-sm text-yellow-700 list-disc list-inside">
              <li>Minimum 8 characters long</li>
              <li>Include at least one uppercase letter</li>
              <li>Include at least one number</li>
              <li>Include at least one special character</li>
            </ul>
          </div>
        </div>
      )}
      
      {/* Interests Tab */}
      {activeTab === 'interests' && (
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold">Manage Interests</h2>
          </div>
          
          <div className="mb-6">
            <div className="flex">
              <input
                type="text"
                value={newInterest}
                onChange={(e) => setNewInterest(e.target.value)}
                placeholder="Add a new interest"
                className="flex-grow px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <button
                type="button"
                onClick={handleAddInterest}
                disabled={!newInterest.trim()}
                className="px-4 py-2 bg-indigo-600 text-white rounded-r-md hover:bg-indigo-700 disabled:bg-indigo-300"
              >
                Add
              </button>
            </div>
          </div>
          
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-3">Your interests</h3>
            <div className="flex flex-wrap gap-2">
              {profile.interests && profile.interests.length > 0 ? (
                profile.interests.map((interest, index) => (
                  <div
                    key={index}
                    className="flex items-center bg-indigo-50 text-indigo-800 px-3 py-1 rounded-full"
                  >
                    <span>{interest}</span>
                    <button
                      type="button"
                      onClick={() => handleRemoveInterest(interest)}
                      className="ml-2 text-indigo-600 hover:text-indigo-800 focus:outline-none"
                    >
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                      </svg>
                    </button>
                  </div>
                ))
              ) : (
                <p className="text-gray-500">You haven't added any interests yet.</p>
              )}
            </div>
          </div>
          
          <div className="mt-6 p-4 bg-indigo-50 border border-indigo-100 rounded-md">
            <p className="text-sm text-indigo-800">
              Your interests help us personalize your experience and suggest relevant content. They're also visible on your public profile.
            </p>
          </div>
        </div>
      )}
      
      {/* Account Danger Zone */}
      <div className="bg-white rounded-lg shadow-sm p-6 border border-red-200">
        <h2 className="text-xl font-semibold text-red-600 mb-4">Danger Zone</h2>
        <p className="text-gray-600 mb-4">
          Actions in this section can permanently affect your account. Please proceed with caution.
        </p>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-md">
            <div>
              <h3 className="font-medium">Delete Account</h3>
              <p className="text-sm text-gray-500">
                This will permanently delete your account and all associated data.
              </p>
            </div>
            <button
              type="button"
              onClick={() => setModalOpen('deleteAccount')}
              className="px-4 py-2 bg-white border border-red-500 text-red-600 rounded-md hover:bg-red-50"
            >
              Delete Account
            </button>
          </div>
          
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-md">
            <div>
              <h3 className="font-medium">Download Personal Data</h3>
              <p className="text-sm text-gray-500">
                Download a copy of your personal data and content.
              </p>
            </div>
            <button
              type="button"
              onClick={() => setModalOpen('dataDownload')}
              className="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
            >
              Request Data
            </button>
          </div>
        </div>
      </div>

      {/* Password Update Confirmation Modal */}
      {modalOpen === 'passwordUpdate' && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6 shadow-xl">
            <h3 className="text-lg font-semibold mb-4">Confirm Password Update</h3>
            <p className="text-gray-600 mb-6">
              Are you sure you want to update your password? You will be logged out of all devices except this one.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => setModalOpen(null)}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handlePasswordReset}
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              >
                Confirm Update
              </button>
            </div>
          </div>
        </div>
      )}


      {/* Delete Account Confirmation Modal */}
      {modalOpen === 'deleteAccount' && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6 shadow-xl">
            <h3 className="text-lg font-semibold mb-2 text-red-600">Delete Account</h3>
            <p className="text-gray-600 mb-4">
              This action is <span className="font-bold">permanent and irreversible</span>. All your data, posts, and personal information will be permanently deleted.
            </p>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Type "DELETE" to confirm
              </label>
              <input
                type="text"
                value={deleteConfirmText}
                onChange={(e) => setDeleteConfirmText(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
              />
            </div>
            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => {
                  setModalOpen(null);
                  setDeleteConfirmText('');
                }}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleDeleteAccount}
                disabled={deleteConfirmText !== 'DELETE'}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:bg-red-300"
              >
                Delete Permanently
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Data Download Confirmation Modal */}
      {modalOpen === 'dataDownload' && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6 shadow-xl">
            <h3 className="text-lg font-semibold mb-4">Request Data Download</h3>
            <p className="text-gray-600 mb-4">
              We'll prepare your personal data for download. This process may take up to 48 hours. You'll receive an email with a download link when your data is ready.
            </p>
            <div className="p-3 bg-blue-50 text-blue-700 text-sm rounded-md mb-4">
              The download link will be sent to: <strong>{profile.email}</strong>
            </div>
            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => setModalOpen(null)}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleDataDownload}
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              >
                Request Download
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfileManagementPage;