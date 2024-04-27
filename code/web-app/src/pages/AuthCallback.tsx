import React, { useEffect } from 'react'; 
import { useNavigate } from 'react-router-dom';
import { getAuthCookies } from '../utils/oauthAgentClient'; 

const AuthCallback: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => { 
    (async () => { 
      await getAuthCookies(window.location.href);
      navigate('/', { replace: true });
    })();
  }, [navigate]); 

  return (
    <>
      Signing in ... 
    </>
  );
}

export default AuthCallback;
