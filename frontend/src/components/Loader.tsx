// src/components/Loader.tsx

import React from 'react';

interface LoaderProps {
  text?: string;
}

const Loader: React.FC<LoaderProps> = ({ text }) => {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-xs w-full text-center">
        <div className="flex justify-center items-center mb-4">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
        </div>
        <p className="text-lg text-gray-700 dark:text-white">{text || 'Loading...'}</p>
      </div>
    </div>
  );
};

export default Loader;
