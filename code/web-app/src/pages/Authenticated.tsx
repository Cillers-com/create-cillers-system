import React from 'react'; 

interface AuthenticatedProps {
  userInfo: Record<string, any>; 
  logout: () => void; 
}

const Authenticated: React.FC<AuthenticatedProps> = ({ userInfo, logout }) => {
    return (
        <>
            Authenticated as: {JSON.stringify(userInfo)}
            <button onClick={logout} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
                Logout
            </button>
        </>
    )
} 

export default Authenticated;

