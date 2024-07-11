import React from 'react';
import { ApolloProvider } from '@apollo/client';
import create_api_client from '../utils/apolloClient';
import Items from './Items';

function on_graphql_error(messages: string[]) { 
    messages.forEach(message => alert(message)); 
} 

const Main: React.FC = () => {
    return (
        <ApolloProvider client={create_api_client(on_graphql_error)}>
            <Items />
        </ApolloProvider>
    )
}

export default Main;
