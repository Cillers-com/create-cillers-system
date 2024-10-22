import React from 'react'; 
import Demo from './demos/rest/Demo';

interface AuthenticatedProps {
  user_info: Record<string, any>; 
  logout: () => void; 
  csrf: string;
}

const Authenticated: React.FC<AuthenticatedProps> = ({ user_info, logout, csrf }) => {
    return (
        <div>
            <div>
                Authenticated as: {JSON.stringify(user_info)}
            </div>
            <button onClick={logout}>
                Logout
            </button>
            <Demo csrf={csrf} />
        </div>
    )
} 

export default Authenticated;
