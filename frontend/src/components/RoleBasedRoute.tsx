import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/authContext';
import Layout from './Layout';

interface RoleBasedRouteProps {
  element: JSX.Element;
  requiredRole: string;
}

const RoleBasedRoute: React.FC<RoleBasedRouteProps> = ({ element, requiredRole }) => {
  const { user } = useAuth();

  if (!user || user.role !== requiredRole) {
    return <Navigate to="/unauthorized" />;
  }

  return <Layout>{element}</Layout>;; 
};

export default RoleBasedRoute;
