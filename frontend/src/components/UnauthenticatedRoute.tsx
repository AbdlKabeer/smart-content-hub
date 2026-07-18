import React from 'react';
import { useAuth } from '../context/authContext'; // Import the useAuth hook
import { Navigate } from 'react-router-dom';

interface UnauthenticatedRouteProps {
  element: JSX.Element;
}

const UnauthenticatedRoute: React.FC<UnauthenticatedRouteProps> = ({ element }) => {
  const { user } = useAuth(); // Get user from context

  // If user is authenticated, redirect to home page
  console.log(user)
  if (user) {
    return <Navigate to="/home" />;
  }

  // If user is not authenticated, render the login page
  return element;
};

export default UnauthenticatedRoute;
