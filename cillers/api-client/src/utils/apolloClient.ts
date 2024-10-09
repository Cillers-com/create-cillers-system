import { 
    ApolloClient, 
    ApolloLink,
    InMemoryCache, 
    HttpLink, 
    split, 
    Observable,
    NormalizedCacheObject,
    DocumentNode
} from '@apollo/client';
import { onError } from '@apollo/client/link/error';
import { setContext } from '@apollo/client/link/context';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';
import { getMainDefinition } from '@apollo/client/utilities';
import config from '../config';
import { refresh_token } from './oauthAgentClient'; 

function replace_http_with_ws (url: string) : string {
    console.log(url.replace('http', 'ws'));
    if (url.startsWith('https')) {
        return url.replace('https', 'wss');
    }
    return url.replace('http', 'ws');
}

function create_http_link(): HttpLink {
    return new HttpLink({
        uri: config.api_base_url,
    });
}

function create_ws_link (csrf: string): GraphQLWsLink {
    return new GraphQLWsLink(createClient({
        url: replace_http_with_ws(config.api_base_url),
        retryAttempts: Infinity,
        shouldRetry: () => true,
        lazy: true, 
        on: {
            closed: async (event: any) => {
                console.log("Subscription websocket closed: ", event); 
                if (event.code === 4403 && event.reason === "token_expired") { 
                    const token_refreshed = await refresh_token();
                    return token_refreshed;
                }
            }, 
            error: async (event: any) => {
                console.log("Error:", event);  
            } 
        }
    }));
};

function create_csrf_link (csrf: string): ApolloLink {
    return setContext(async (_, { headers }) => {
        return {
            headers: {
                ...headers, 
                "x-curity-csrf": csrf,
            } 
        };
    });
} 

interface ServerError { 
    statusCode: number
} 

function create_error_link (csrf: string, on_error: Function) : ApolloLink { 
    return onError(({ graphQLErrors, networkError, operation, forward }) => {
        if (networkError) {
            if (networkError.name === "ServerError" && (networkError as ServerError).statusCode === 401) {
                return new Observable(observer => { 
                    refresh_token().then((token_refreshed: boolean) => {
                        if (token_refreshed) { 
                            const subscriber = { 
                                next: observer.next.bind(observer), 
                                error: observer.error.bind(observer),
                                complete: observer.complete.bind(observer)
                            }
                            forward(operation).subscribe(subscriber);
                        }
                    }).catch(error => {
                        console.log("ERROR:", error); 
                        observer.error(error);
                    });
                });
            }
        }
        if (graphQLErrors) {
            const messages = graphQLErrors.map(error => error.message); 
            on_error(messages); 
        } 
    });
} 

function is_subscription_query({ query }: { query: DocumentNode }) {
    const definition = getMainDefinition(query);
    return (
        definition.kind === 'OperationDefinition' &&
            definition.operation === 'subscription'
    );
} 

function create_api_client (csrf: string, on_error: Function) : ApolloClient<NormalizedCacheObject> { 
    const ws_link = create_ws_link(csrf);
    const http_link = create_http_link();
    const csrf_link = create_csrf_link(csrf); 
    const error_link = create_error_link(csrf, on_error); 
    const http_chain = error_link.concat(csrf_link.concat(http_link)) 

    const split_link = split(is_subscription_query, ws_link, http_chain);

    return new ApolloClient({
        link: split_link,
        cache: new InMemoryCache(),
        defaultOptions: {
            watchQuery: {
                errorPolicy: 'all'
            },
            query: {
                errorPolicy: 'all'
            },
            mutate: {
                errorPolicy: 'all'
            }
        }
    }); 
};

export default create_api_client;
