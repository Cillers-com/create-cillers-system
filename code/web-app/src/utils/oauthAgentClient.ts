import axios, { AxiosRequestConfig, AxiosRequestHeaders, Method } from 'axios';
import { ErrorHandler } from './errorHandler';
import { RemoteError } from './remoteError';

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

export async function getLoginState(pageUrl: string): Promise<any> {
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
    
export async function getUserInfo(csrf: string): Promise<any> {
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

export async function refreshToken(csrf: string): Promise<void> {
  myfetch('POST', 'refresh', null, csrf);
}

export async function logoutFromAgent(csrf: string): Promise<void> {
  myfetch('POST', 'logout', null, csrf);
} 

export async function getAuthRequestUrl(): Promise<any> {
  try {
    const data = await myfetch('POST', 'login/start', null);    
    return data.authorizationRequestUrl; 
  } catch (error) {
    console.error('Error:', error); 
    throw error;
  }
}

export type UserInfo = Record<string, any>; 

