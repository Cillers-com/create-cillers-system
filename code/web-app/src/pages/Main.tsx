import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios, { AxiosRequestConfig, AxiosRequestHeaders, Method } from 'axios';
import { ErrorHandler } from '../utilities/errorHandler';
import { RemoteError } from '../utilities/remoteError';

async function myfetch(method: string, path: string, body: any, csrf?: string): Promise<any> {
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
  const headers = options.headers as AxiosRequestHeaders

  if (body) {
    options.data = body;
  }

  if (csrf) {
    headers['x-curity-csrf'] = csrf;
  }

  try {
    const response = await axios.request(options);
    return response.data;
  } catch (e) {
    console.error(e);  
    throw ErrorHandler.handleFetchError('OAuth Agent', e);
  }
}

async function getLoginState(pageUrl: string): Promise<any> {
  try {
    const request = pageUrl ? JSON.stringify({ pageUrl }) : null; 
    return await myfetch('POST', 'login/end', request);
  } catch (e) {
    const remoteError = e as RemoteError;
    if (remoteError.isSessionExpiredError()) {
      return {
        handled: false,
        isLoggedIn: false
      };
    }
    throw e;
  }
}
    
async function getUserInfo(csrf: string): Promise<any> {
  try {
    return await myfetch('GET', 'userInfo', null, csrf);
  } catch (remoteError) {
    console.log('Remote error', remoteError); 
    if (!(remoteError instanceof RemoteError)) {
      throw remoteError;
    }
    if (!remoteError.isAccessTokenExpiredError()) {
      throw remoteError;
    }
    await refreshToken(csrf);
    try {
      return await myfetch('GET', 'userInfo', null, csrf);
    } catch (e) {
      throw ErrorHandler.handleFetchError('OAuth Agent', e);
    }
  }
}

async function refreshToken(csrf: string): Promise<void> {
  myfetch('POST', 'refresh', null, csrf);
}

async function Ologout(csrf: string): Promise<void> {
  myfetch('POST', 'logout', null, csrf);
} 

async function getAuthRequestUrl(): Promise<any> {
  try {
    const data = await myfetch('POST', 'login/start', null);    
    return data.authorizationRequestUrl; 
  } catch (error) {
    console.error('Error:', error); 
    throw error;
  }
}

async function signalLogoutToOtherTabs() { 
  localStorage.setItem("logout", "" + Date.now()); 
} 

type UserInfo = Record<string, any>; 

const App: React.FC = () => {
  const [getLoginStateComplete, setGetLoginStateComplete] = useState<boolean>(false); 
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false); 
  const [csrf, setCsrf] = useState<string | null>(null); 
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null); 
  const [isLoggingOut, setIsLoggingOut] = useState<boolean>(false); 
  
  // Check login state on pageload. 
  useEffect(() => { 
    (async () => {
      const loginState = await getLoginState(window.location.href);
      setGetLoginStateComplete(true);
      if (loginState.isLoggedIn) {
        if (!loginState.csrf) { 
          throw new Error("No CSRF in loginState"); 
        }
        setIsLoggedIn(true);
        setCsrf(loginState.csrf);
        const userInfo = await getUserInfo(loginState.csrf); 
        setUserInfo(userInfo); 
      }
    })(); 
  }, []); 

  // Logout if other tab is logged out. 
  useEffect(() => {
    const handleEventLogoutFromOtherTab = (event: StorageEvent) => {
      if (event.key === "logout") {
        resetStateOnLogout();
      }
    };
    window.addEventListener('storage', handleEventLogoutFromOtherTab);
    return () => {
      window.removeEventListener('storage', handleEventLogoutFromOtherTab);
    };
  }, []);

  const login = async () => {
    window.location.href = await getAuthRequestUrl(); 
  } 

  const logout = async () => {
    if (!isLoggedIn) { 
      throw new Error("Not logged in"); 
    } 
    if (!csrf) { 
      throw new Error("No CSRF"); 
    } 
    setIsLoggingOut(true);
    await Ologout(csrf); 
    setIsLoggingOut(false);
    resetStateOnLogout();
    signalLogoutToOtherTabs(); 
  } 
  
  const resetStateOnLogout = () => { 
    setIsLoggedIn(false);
    setCsrf(null); 
    setUserInfo(null);
  }

  const component: React.ReactElement = (() => { 
    if (isLoggingOut) { 
      return (<>Logging out ...</>)
    } else if (!getLoginStateComplete) { 
      return (<>Waiting for login state info...</>)
    } else if (!isLoggedIn){ 
      return (
        <>
          Not authenticated 
          <button onClick={login} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
            Login
          </button>
        </>
      )
    } else if (!userInfo) { 
      return (<>Waiting for user info ...</>)
    } else {  
      return (
        <>
          Authenticated as: {JSON.stringify(userInfo)}
          <button onClick={logout} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
            Logout
          </button>
        </>
      )
    }   
  })(); 

  return (<>{component}</>); 
}

export default App;

