import { ApolloClient, InMemoryCache, HttpLink, split } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { WebSocketLink } from '@apollo/client/link/ws';
import { getMainDefinition } from '@apollo/client/utilities';
import config from './config';

const createAutenticatedClient = (csrf: string) => { 

    const httpLink = new HttpLink({
        uri: config.apiBaseUrl,
    });

    const authLink = setContext(async (_, { headers }) => {
        const contextHeaders = { 
            ...headers, 
            "x-curity-csrf": csrf,
        }; 

        return {
            headers: contextHeaders 
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

    return new ApolloClient({
        link: splitLink,
        cache: new InMemoryCache(),
    }); 
};

export default createAutenticatedClient;
