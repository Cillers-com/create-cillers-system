import { useState, useEffect, useCallback } from 'react'; 
import { 
    get_login_state, 
    get_user_info, 
    logout, 
    login,
    get_auth_request_url, 
    UserInfo,
    LoginState
} from './oauthAgentClient'

export { logout, login }; 

let isLoginStateChecked = false;

const useAuth = () => {
    const [getLoginStateComplete, setGetLoginStateComplete] = useState<boolean>(false);
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
    const [csrf, setCsrf] = useState<string | null | undefined>(null);
    const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
    const [isLoggingOut, setIsLoggingOut] = useState<boolean>(false);

    const handleLogout = useCallback(async () => {
        if (isLoggedIn) {
            setIsLoggingOut(true);
            setIsLoggedIn(false);
            setCsrf(null);
            setUserInfo(null);
            setIsLoggingOut(false);
            isLoginStateChecked = true; 
        }
    }, [isLoggedIn]);

    // Check login state on pageload. 
    useEffect(() => { 
        (async () => {
            if (isLoginStateChecked) {
                return;
            }
            const loginState: LoginState = await get_login_state();
            setGetLoginStateComplete(true);
            if (loginState.isLoggedIn) {
                setIsLoggedIn(true);
                setCsrf(loginState.csrf);
                const userInfo = await get_user_info(); 
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

