import React, { useEffect } from 'react'; 
import { useNavigate } from 'react-router-dom';
import { exchange_code_for_cookies } from '../utils/oauthAgentClient'; 

const AuthCallback: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => { 
    (async () => { 
      await exchange_code_for_cookies(window.location.href);
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
