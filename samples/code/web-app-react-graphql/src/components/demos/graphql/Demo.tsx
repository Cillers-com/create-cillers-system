import React, { useMemo } from 'react'
import { ApolloProvider } from '@apollo/client'
import create_api_client from '../../../graphql/client';
import Items from './Items'

function on_graphql_error(messages: string[]) { 
    messages.forEach(message => alert(message)); 
} 

const Demo: React.FC = () => {
  const client = useMemo(() => create_api_client(on_graphql_error), []);

  return (
    <ApolloProvider client={client}>
        <Items />
    </ApolloProvider>
  )
}

export default Demo 
