import { ApolloClient, InMemoryCache, HttpLink, split } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { WebSocketLink } from '@apollo/client/link/ws';
import { getMainDefinition } from '@apollo/client/utilities';
import { getAccessToken } from './services/authService';
import config from './config';

const httpLink = new HttpLink({
  uri: config.apiBaseUrl,
});

const authLink = setContext(async (_, { headers }) => {
  const token = await getAccessToken();
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : "",
    }
  };
});

const wsLink = new WebSocketLink({
  uri: config.apiBaseUrl.replace('http', 'ws'),
  options: {
    reconnect: true,
    connectionParams: async () => {
      const token = await getAccessToken();
      return {
        headers: {
          Authorization: token ? `Bearer ${token}` : "",
        },
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
