import React, { useMemo } from 'react'
import { ApolloProvider } from '@apollo/client'
import create_api_client from '../../../graphql/client';
import Items from './Items'

interface DemoProps {
    csrf: string
}

function on_graphql_error(messages: string[]) { 
    messages.forEach(message => alert(message)); 
} 

const Demo: React.FC<DemoProps> = ({csrf}) => {
  const client = useMemo(() => create_api_client(csrf, on_graphql_error), [csrf]);

  return (
    <ApolloProvider client={client}>
        <Items />
    </ApolloProvider>
  )
}

export default Demo 
