import React from 'react'; 
//import { ApolloProvider } from '@apollo/client';
//import create_api_client from '../utils/apolloClient';
import GraphQLUI from './GraphQLUI';

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
        <>
            <div>
                Authenticated as: {JSON.stringify(userInfo)}
            </div>
            <button onClick={logout}>
                Logout
            </button>
            <GraphQLUI csrf={csrf}/>
        </>
    )
} 

export default Authenticated;

