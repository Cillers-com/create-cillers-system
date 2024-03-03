import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { signInCallback } from '../services/authService';

const SignInCallbackPage: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    signInCallback().then(() => navigate('/')).catch(console.error);
  }, [navigate]);

  return (
    <div className="flex justify-center items-center min-h-screen bg-base-300">
      <button className="btn">
        <span className="loading loading-spinner"></span>
        Loading...
      </button>
    </div>
  );
};

export default SignInCallbackPage;
