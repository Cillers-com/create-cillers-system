import { ApolloClient, InMemoryCache, HttpLink, split } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { WebSocketLink } from '@apollo/client/link/ws';
import { getMainDefinition } from '@apollo/client/utilities';
import config from './config';

const httpLink = new HttpLink({
    uri: config.apiBaseUrl,
});

const authLink = setContext(async (_, { headers }) => {
    const csrf = localStorage.getItem('csrf') || ''; // Retrieve CSRF token dynamically
    return {
        headers: { 
            ...headers, 
            'X-CSRF-Token': csrf,
        }
    };
});

const wsLink = new WebSocketLink({
    uri: config.apiBaseUrl.replace('http', 'ws'),
    options: {
        reconnect: true,
        connectionParams: async () => {
            return {
                headers: {}
            };
        },
    },
});

const splitLink = split(
    ({ query }) => {
        const definition = getMainDefinition(query);
        return (
            definition.kind === 'OperationDefinition' &&
            definition.operation === 'subscription'
        );
    },
    wsLink,
    authLink.concat(httpLink),
);

const client = new ApolloClient({
    link: splitLink,
    cache: new InMemoryCache(),
});

export default client;
