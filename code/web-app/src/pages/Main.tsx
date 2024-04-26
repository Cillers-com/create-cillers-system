import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import useAuth, { login, logout } from '../useAuth'

const App: React.FC = () => {
    const { getLoginStateComplete, isLoggedIn, userInfo, isLoggingOut } = useAuth();

  const component: React.ReactElement = (() => { 
    if (isLoggingOut) { 
      return (<>Logging out ...</>)
    } else if (!getLoginStateComplete) { 
      return (<>Waiting for login state info...</>)
    } else if (!isLoggedIn){ 
      return (
        <>
          Not authenticated 
          <button onClick={login} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
            Login
          </button>
        </>
      )
    } else if (!userInfo) { 
      return (<>Waiting for user info ...</>)
    } else {  
      return (
        <>
          Authenticated as: {JSON.stringify(userInfo)}
          <button onClick={logout} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
            Logout
          </button>
        </>
      )
    }   
  })(); 

  return component; 
}

export default App;
