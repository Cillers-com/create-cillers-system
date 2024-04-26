import React from 'react'; 

interface AnonymousProps { 
    login: () => Promise<void>;
} 

const Anonymous: React.FC<AnonymousProps> = ({ login }) => {
    return (
        <>
            Not authenticated 
            <button onClick={login} >
                Login
            </button>
        </>
    )
} 

export default Anonymous; 
