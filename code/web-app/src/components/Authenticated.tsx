import React from 'react'; 
import { ApolloProvider } from '@apollo/client';
import create_api_client from '../utils/apolloClient';
import Items from './Items';

interface AuthenticatedProps {
  userInfo: Record<string, any>; 
  logout: () => void; 
  csrf: string;
}

function on_graphql_error(messages: string[]) { 
    messages.forEach(message => alert(message)); 
} 

const Authenticated: React.FC<AuthenticatedProps> = ({ userInfo, logout, csrf }) => {
    return (
        <ApolloProvider client={create_api_client(csrf, on_graphql_error)}>
            <div>
                Authenticated as: {JSON.stringify(userInfo)}
            </div>
            <button onClick={logout}>
                Logout
            </button>
            <Items />
        </ApolloProvider>
    )
} 

export default Authenticated;

