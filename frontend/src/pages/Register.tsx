import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/authContext';
import InputField from '../components/InputField'; // Import the reusable InputField component

const Register: React.FC = () => {
  const { fetchWithAuth, displayNotification, setUser,setAuthToken , setGlobalLoading, setGlobalLoadingText } = useAuth(); // Assuming 'authToken' is provided from context
  const navigate = useNavigate();

  // State to hold form data
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    current_year_level: '',
    // previous_year_performance: '',
    preferred_content: '',
    // study_preference: '',
    password: '',
    confirmPassword: '',
  });

  // State to toggle password visibility
  const [passwordVisible, setPasswordVisible] = useState(false);

  // Handle form input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  // Submit the form data to the backend
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setGlobalLoading(true);
      setGlobalLoadingText('Registering...');
      const response = await fetchWithAuth({
        method: 'POST',
        path: `/auth/register`, // Submit quiz answers
        body: formData,
      });

      setAuthToken(response?.data?.tokens)
      localStorage.setItem('tokens', JSON.stringify(response?.data?.tokens));
      setUser(response?.data?.user)

      // Show result modal
      displayNotification('success', response?.message);
      navigate('/home');
    } catch (error) {
      console.error('Error submitting quiz:', error);
    }finally{
      setGlobalLoading(false);
    }
  };

  return (
    <div className="container mx-auto my-auto p-6 bg-white shadow-lg rounded-lg w-full sm:w-2/3 max-w-lg">
      <h2 className="text-3xl font-bold text-center mb-6 text-gray-800">Create Account</h2>
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* First Name and Last Name */}
        <div className="grid gap-2 grid-cols-1 ">
          <InputField
            type="text"
            label="First Name"
            name="first_name"
            placeholder=''
            value={formData.first_name}
            onChange={handleChange}
            required
          />
          <InputField
            type="text"
            label="Last Name"
            name="last_name"
            placeholder=''
            value={formData.last_name}
            onChange={handleChange}
            required
          />
        </div>

        {/* Email and Phone Number */}
        <div className="grid grid-cols-1  gap-2">
          <InputField
            type="email"
            label="Email"
            name="email"
            placeholder=''
            value={formData.email}
            onChange={handleChange}
            required
          />
          <InputField
            type="tel"
            label="Phone Number"
            name="phone_number"
            placeholder=''
            value={formData.phone_number}
            onChange={handleChange}
            required
          />
        </div>

        {/* Current Year and Previous Year Performance */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <InputField
            type="select"
            label="Current Year Level"
            name="current_year_level"
            placeholder=''
            value={formData.current_year_level}
            onChange={handleChange}
            required
            options={['1st Year', '2nd Year', '3rd Year', '4th Year', '5th Year']}
          />
          <InputField
            type="select"
            label="Preferred Content"
            name="preferred_content"
            placeholder=''
            value={formData.preferred_content}
            onChange={handleChange}
            required
            options={['Video', 'Article', 'Quiz']}
          />
          
        </div>

        {/* Preferred Content and Study Preference */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {/* <InputField
            type="select"
            label="Previous Year Performance"
            name="previous_year_performance"
            placeholder=''
            value={formData.previous_year_performance}
            onChange={handleChange}
            required
            options={['First Class', '2:1', '2:2', 'Third Class']}
          /> */}
          {/* <InputField
            type="select"
            label="Study Preference"
            name="study_preference"
            placeholder=''
            value={formData.study_preference}
            onChange={handleChange}
            required
            options={['Morning', 'Night']}
          /> */}
        </div>

        {/* Password and Confirm Password with View Toggle */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <div className="relative">
            <InputField
              type={passwordVisible ? 'text' : 'password'} // Conditionally toggle between text and password
              label="Password"
              name="password"
              placeholder=''
              required
              value={formData.password}
              onChange={handleChange}
            />
          </div>

          <div className="relative">
            <InputField
              type={passwordVisible ? 'text' : 'password'} // Conditionally toggle between text and password
              label="Confirm Password"
              name="confirmPassword"
              placeholder=''
              required
              value={formData.confirmPassword}
              onChange={handleChange}
            />
            
          </div>

          <button
              type="button"
              className=""
              onClick={() => setPasswordVisible(!passwordVisible)}
            >
              
              <span className=' text-sm font-normal'>
              {passwordVisible ? 'Hide Password' : 'Show Password'}
              </span>
              
            </button>
        </div>

        {/* Submit Button */}
        <div>
          <button type="submit" className="w-full py-3 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 transition duration-200">
            Register
          </button>
        </div>

        {/* Link to login page */}
        <div className="text-center text-gray-600 text-sm">
          Already have an account?{' '}
          <Link to="/login" className="text-indigo-600">
            Login
          </Link>
        </div>
      </form>
    </div>
  );
};

export default Register;
