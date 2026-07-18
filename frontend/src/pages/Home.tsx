import React from 'react';
import { useAuth } from '../context/authContext';
import AdminDashboard from './admin/AdminDashboard';
import StudentDashboard from '../components/StudentDashboard';

const Home: React.FC = () => {
  const { user } = useAuth();
  return (
    <>
   {user?.role == 'admin' ?<AdminDashboard /> : <StudentDashboard />}
    </>
  );
};

export default Home;
