import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/authContext';
import Layout from './Layout';

interface PrivateRouteProps {
  element: JSX.Element;
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ element }) => {
  const { authToken } = useAuth();

  if (!authToken) {
    return <Navigate to="/login" />;
  }

  return <Layout>
    <div className=' max-w-5xl mx-auto'>
    {element}
    </div>
    </Layout>;; 
};

export default PrivateRoute;
