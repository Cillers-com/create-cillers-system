import { useState, useEffect } from 'react'; 
import axios, { AxiosRequestConfig, AxiosRequestHeaders, Method } from 'axios';
import { ErrorHandler } from './utilities/errorHandler';
import { RemoteError } from './utilities/remoteError';

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

type UserInfo = Record<string, any>; 

interface AuthState {
    getLoginStateComplete: boolean;
    isLoggedIn: boolean;
    csrf: string | null;
    userInfo: UserInfo | null;
    isLoggingOut: boolean;
}

export const login = async () => {
  window.location.href = await getAuthRequestUrl(); 
} 

export const logout = () => { 
  localStorage.setItem("logout", "" + Date.now()); 
  window.dispatchEvent(new CustomEvent('logout')); 
} 

const useAuth = () => {
    const [getLoginStateComplete, setGetLoginStateComplete] = useState<boolean>(false);
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
    const [csrf, setCsrf] = useState<string | null>(null);
    const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
    const [isLoggingOut, setIsLoggingOut] = useState<boolean>(false);

    const handleLogout = async () => {
        if (isLoggedIn) {
            if (!csrf) { 
                throw new Error("No CSRF"); 
            } 
            setIsLoggingOut(true);
            await Ologout(csrf);
            setIsLoggedIn(false);
            setCsrf(null);
            setUserInfo(null);
            setIsLoggingOut(false);
        }
    };

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

    useEffect(() => {
        const handleStorageEvent = async (event: StorageEvent) => {
            if (event.key === "logout") {
                handleLogout();
            }
        };

        window.addEventListener('logout', handleLogout);
        window.addEventListener('storage', handleStorageEvent);

        return () => {
            window.removeEventListener('logout', handleLogout);
            window.removeEventListener('storage', handleStorageEvent);
        };
    }, [isLoggedIn, csrf]);

    return { getLoginStateComplete, isLoggedIn, csrf, userInfo, isLoggingOut };
};

export default useAuth; 
