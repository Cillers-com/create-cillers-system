import React from 'react'; 

interface AnonymousProps { 
    login: () => Promise<void>;
} 

const Anonymous: React.FC<AnonymousProps> = ({ login }) => {
    return (
        <>
            <p> 
                Not authenticated 
            </p>
            <button onClick={login} >
                Login
            </button>
        </>
    )
} 

export default Anonymous; 
