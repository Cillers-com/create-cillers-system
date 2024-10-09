import { ApiClientInterface } from '../types';

export interface Item {
    id: string;
    name: string;
}

export function create(client: ApiClientInterface) {
    return {
        list(): Promise<Item[]> {
            const on_error = (messages: string[]) => {
                console.error('Error in items list API:', messages);
            };
            return client.get<Item[]>('/api/items', on_error);
        },

        create(items: Omit<Item, 'id'>[]): Promise<Item[]> {
            const on_error = (messages: string[]) => {
                console.error('Error in items create API:', messages);
            };
            return client.post<Item[]>('/api/items', on_error, items);
        },

        remove(id: string): Promise<{ message: string }> {
            const on_error = (messages: string[]) => {
                console.error('Error in items remove API:', messages);
            };
            return client.delete<{ message: string }>(`/api/items/${id}`, on_error);
        }
    };
}
