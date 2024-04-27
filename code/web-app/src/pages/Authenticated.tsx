import React from 'react'; 
import Products from './Products';

interface AuthenticatedProps {
  userInfo: Record<string, any>; 
  logout: () => void; 
}

const Authenticated: React.FC<AuthenticatedProps> = ({ userInfo, logout }) => {
    return (
        <>
            <p>
                Authenticated as: {JSON.stringify(userInfo)}
            </p>
            <button onClick={logout}>
                Logout
            </button>
            <Products />
        </>
    )
} 

export default Authenticated;

