import React from 'react'; 
import { ApolloProvider } from '@apollo/client';
import createAuthenticatedClient from '../apolloClient';
import Products from './Products';

interface AuthenticatedProps {
  userInfo: Record<string, any>; 
  logout: () => void; 
  csrf: string;
}

const Authenticated: React.FC<AuthenticatedProps> = ({ userInfo, logout, csrf }) => {
    return (
        <ApolloProvider client={createAuthenticatedClient(csrf)}>
            <p>
                Authenticated as: {JSON.stringify(userInfo)}
            </p>
            <button onClick={logout}>
                Logout
            </button>
            <Products />
        </ApolloProvider>
    )
} 

export default Authenticated;

