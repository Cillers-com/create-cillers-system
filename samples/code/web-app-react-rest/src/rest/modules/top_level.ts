import { ApiClientInterface } from '../types';

export function create(client: ApiClientInterface) {
    return {
        hello(): Promise<{ message: string }> {
            const on_error = (messages: string[]) => {
                console.error('Error in hello API:', messages);
            };
            return client.get<{ message: string }>('/api/hello', on_error);
        },

        hello_admin(): Promise<{ message: string }> {
            const on_error = (messages: string[]) => {
                console.error('Error in hello admin API:', messages);
            };
            return client.get<{ message: string }>('/api/hello_admin', on_error);
        }
    };
}

export const isTopLevel = true;
