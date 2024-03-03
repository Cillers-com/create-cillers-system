import React, { useEffect, useState } from 'react';
import { Outlet } from 'react-router-dom';
import { getUser, signIn } from '../services/authService';

const PrivateRoute: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    getUser().then(user => {
      if (user && !user.expired) {
        setIsAuthenticated(true);
      } else {
        signIn();
      }
    });
  }, []);

  if (isAuthenticated) {
    return <Outlet />;
  } else {
    return (
      <div className="flex justify-center items-center min-h-screen bg-base-300">
        <button className="btn">
          <span className="loading loading-spinner"></span>
          Redirecting to login...
        </button>
      </div>
    );
  }
};

export default PrivateRoute;
