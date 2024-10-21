import config from '../config'

export interface LoginState { 
    isLoggedIn: boolean,
    isHandled: boolean,
    csrf: string
} 

export type UserInfo = Record<string, any>; 

let csrf: string | null = null; 

const base_URL = `${config.oauth_agent_base_url}`;
async function fetch_from_agent(method: string, path: string, body?: string): Promise<Response> {
    const URL = `${base_URL}/${path}`;
    const headers = new Headers({
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    });
    if (csrf) {
        headers.append('x-curity-csrf', csrf);
    }
    const options: RequestInit = {
        method: method,
        headers: headers,
        credentials: 'include',
        body: body,
    };
    return fetch(URL, options); 
}

async function fetch_data_from_agent_with_token_refresh(method: string, path: string, body?: string) : Promise<any> { 
    const response: Response = await fetch_from_agent(method, path, body);
    assert_response_status(response, [200, 401]); 
    const data = await response.json(); 
    if (response.status === 200) { 
        return data;
    }
    assert(data.code === "token_expired", `Unexpected code: ${data.code}`); 
    const tokenRefreshed = await refresh_token(); 
    if (!tokenRefreshed) {
        return null; 
    }
    const response2 = await fetch_from_agent(method, path, body); 
    assert_response_status(response2, [200]); 
    return response2.json(); 
}

export async function get_login_state(): Promise<LoginState> {
    const response = await fetch_from_agent('POST', 'login/end');
    assert_response_status(response, 200);
    const data = await response.json();
    csrf = data.csrf;
    return data;
}

export async function exchange_code_for_cookies(pageUrl: string): Promise<LoginState> { 
    const request = JSON.stringify({ pageUrl });
    const response = await fetch_from_agent('POST', 'login/end', request);
    assert_response_status(response, 200);
    const data = await response.json(); 
    assert(data.handled, `handled is expected to be true ${JSON.stringify(data)}`); 
    assert(data.csrf, `csrf is expected to be non-null ${JSON.stringify(data)}`); 
    csrf = data.csrf; 
    return data;  
}

export async function get_user_info(): Promise<UserInfo | null> {
    return await fetch_data_from_agent_with_token_refresh('GET', 'userInfo');
}

export async function refresh_token(): Promise<boolean> {
    const response: Response = await fetch_from_agent('POST', 'refresh');
    assert_response_status(response, [204, 401]); 
    if (response.status === 401) { 
        await login(); 
        return false;
    } 
    return true; 
}


export async function login() {
    window.location.href = await get_auth_request_url(); 
} 

export async function logout(): Promise<void> {
    const response = await fetch_from_agent('POST', 'logout');
    assert_response_status(response, [200, 401]);
    csrf = null; 
    signalLoggedOut(); 
} 

function signalLoggedOut(): void { 
    localStorage.setItem("logout", "" + Date.now()); 
    window.dispatchEvent(new CustomEvent('logout')); 
}

export async function get_auth_request_url(): Promise<string> {
    const response = await fetch_from_agent('POST', 'login/start');
    assert_response_status(response, 200); 
    const data = await response.json(); 
    assert(data.authorizationRequestUrl, "Unexpected empty authorizationRequestUrl."); 
    return data.authorizationRequestUrl; 
}

function assert(condition: boolean, message: string): void { 
    if (!condition) { 
        throw new Error(`Assertion failed: ${message}`); 
    }
} 

function assert_response_status(response: Response, accepted_statuses: number | number[]): void {
    if (typeof accepted_statuses === 'number') { 
        assert(accepted_statuses === response.status, `Unexpected response status: ${response.status}`); 
    } else { 
        assert(accepted_statuses.includes(response.status), `Unexpected response status: ${response.status}`); 
    }
} 

