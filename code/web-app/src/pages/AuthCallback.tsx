import React, { useEffect } from 'react'; 
import { useNavigate } from 'react-router-dom';
import axios, { AxiosRequestConfig, Method } from 'axios';
import { RemoteError } from '../utilities/remoteError';

async function myfetch(method: string, path: string, body: any): Promise<any> {
  const url = `http://localhost:8080/oauth-agent/${path}`;
  const options: AxiosRequestConfig = {
    url,
    method: method as Method,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
    },
    withCredentials: true,
  };

  if (body) {
    options.data = body;
  }

  try {
    const response = await axios.request(options);
    return response.data;
  } catch (e) {
    console.error(e);
    throw new Error('Failed to fetch data from OAuth Agent');
  }
}

async function getAuthCookies(pageUrl: string) { 
  const request = JSON.stringify({ pageUrl });
  const response = await myfetch('POST', 'login/end', request);
  if (!response.handled) { 
    throw new Error("response.handled is expected to be true in callback"); 
  } 
  return response;  
} 

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
