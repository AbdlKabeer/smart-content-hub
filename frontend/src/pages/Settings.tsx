import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/authContext';

interface UserProfile {
  first_name: string;
  last_name: string;
  email: string;
}

interface PasswordReset {
    current_password: string;
    new_password: string;
    confirm_new_password: string;
}

const Settings: React.FC = () => {
  const { fetchWithAuth, displayNotification, setUser, user } = useAuth();

  // User Profile State
  const [profile, setProfile] = useState<UserProfile>({
    first_name: '',
    last_name: '',
    email: '',
  });
  const [profileError, setProfileError] = useState<string | null>(null);

  // Password Reset State
  const [password, setPassword] = useState<PasswordReset>({
    current_password: '',
    new_password: '',
    confirm_new_password: '',
  });
  const [passwordError, setPasswordError] = useState<string | null>(null);

  // Modal state for password update confirmation
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Pre-fill profile state when user data is available
  useEffect(() => {
    if (user) {
      setProfile({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
      });
    }
  }, [user]); // Runs only when the user data changes

  // Handle Profile Change
  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProfile((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const updateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfileError(null);

    try {
      const response = await fetchWithAuth({
        method: 'PUT',
        path: '/account/', 
        body: profile,
      });

      // Assuming response has a "data" object with user data
      setUser(response?.data?.user);
      displayNotification('success', 'Profile updated successfully');
    } catch (error) {
      console.error('Error updating profile:', error);
      displayNotification('error','Failed to update profile');
    }
  };

  // Handle Password Change
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPassword((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const resetPassword = (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError(null);

    if (password.new_password !== password.confirm_new_password) {
      displayNotification('error','Passwords do not match');
      return;
    }

    // Open the confirmation modal before actually resetting the password
    setIsModalOpen(true);
  };

  // Handle password reset confirmation
  const confirmPasswordReset = async () => {
    try {
      const response = await fetchWithAuth({
        method: 'POST',
        path: '/account/change-password', 
        body: password,
      });
      console.log(response)
      displayNotification('success', 'Password reset successful');
      setIsModalOpen(false);
    //   navigate('/home'); 
    } catch (error) {
      console.error('Error resetting password:', error);
      displayNotification('error','Failed to reset password');
      setIsModalOpen(false); 
    }
  };

  // Handle modal cancellation
  const cancelPasswordReset = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="container mx-auto md:p-6">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow-xl">
        {/* Profile Section */}
        <h2 className="text-2xl font-semibold mb-4">Profile Settings</h2>
        <form onSubmit={updateProfile}>
          {profileError && <p className="text-red-500">{profileError}</p>}
          <div className="mb-4">
            <label className="block text-gray-700">First Name</label>
            <input
              type="text"
              name="first_name"
              value={profile.first_name}
              onChange={handleProfileChange}
              className="w-full p-3 border border-gray-300 rounded-md"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Last Name</label>
            <input
              type="text"
              name="last_name"
              value={profile.last_name}
              onChange={handleProfileChange}
              className="w-full p-3 border border-gray-300 rounded-md"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Email</label>
            <input
              type="email"
              name="email"
              disabled
              value={profile.email}
              onChange={handleProfileChange}
              className="w-full p-3 border border-gray-300 rounded-md"
            />
          </div>
          <button type="submit" className="w-full max-w-[150px] bg-blue-600 text-white p-3 rounded-md">
            Update Profile
          </button>
        </form>

        {/* Password Reset Section */}
        <h2 className="text-2xl font-semibold mt-8 mb-4">Change Password</h2>
        <form onSubmit={resetPassword}>
          {passwordError && <p className="text-red-500">{passwordError}</p>}
          <div className="mb-4">
            <label className="block text-gray-700">Current Password</label>
            <input
              type="password"
              name="current_password"
              value={password.current_password}
              onChange={handlePasswordChange}
              className="w-full p-3 border border-gray-300 rounded-md"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">New Password</label>
            <input
              type="password"
              name="new_password"
              value={password.new_password}
              onChange={handlePasswordChange}
              className="w-full p-3 border border-gray-300 rounded-md"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Confirm New Password</label>
            <input
              type="password"
              name="confirm_new_password"
              value={password.confirm_new_password}
              onChange={handlePasswordChange}
              className="w-full p-3 border border-gray-300 rounded-md"
              required
            />
          </div>
          <button type="submit" className="w-full max-w-[150px] bg-blue-600 text-white p-3 rounded-md">
            Reset Password
          </button>
        </form>
      </div>

      {/* Confirmation Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 flex justify-center items-center bg-gray-500 bg-opacity-50 z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl max-w-md w-full">
            <h3 className="text-lg font-semibold mb-4">Confirm Password Reset</h3>
            <p className="mb-4">Are you sure you want to reset your password? This action cannot be undone.</p>
            <div className="flex justify-end space-x-4">
              <button
                className="bg-gray-500 text-white p-2 rounded-md"
                onClick={cancelPasswordReset}
              >
                Cancel
              </button>
              <button
                className="bg-blue-600 text-white p-2 rounded-md"
                onClick={confirmPasswordReset}
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Settings;
