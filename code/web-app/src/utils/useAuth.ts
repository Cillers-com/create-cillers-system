import { useState, useEffect, useCallback } from 'react'; 
import { 
    getLoginState, 
    getUserInfo, 
    logoutFromAgent, 
    getAuthRequestUrl, 
    UserInfo 
} from './oauthAgentClient'

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

    const handleLogout = useCallback(async () => {
        if (isLoggedIn) {
            if (!csrf) { 
                throw new Error("No CSRF"); 
            } 
            setIsLoggingOut(true);
            await logoutFromAgent(csrf);
            setIsLoggedIn(false);
            setCsrf(null);
            localStorage.setItem('csrf', "");
            setUserInfo(null);
            setIsLoggingOut(false);
        }
    }, [isLoggedIn, csrf]);

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
                localStorage.setItem('csrf', loginState.csrf);
                const userInfo = await getUserInfo(loginState.csrf); 
                setUserInfo(userInfo); 
            }
        })(); 
    }, []); 

    // Set up logout listeners. 
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
    }, [handleLogout]);

    return { getLoginStateComplete, isLoggedIn, csrf, userInfo, isLoggingOut };
};

export default useAuth; 
