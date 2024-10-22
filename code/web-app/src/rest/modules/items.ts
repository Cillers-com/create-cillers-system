import { ApiClientInterface } from '../types';

export interface Item {
    id: string;
    data: ItemData;
}

export interface ItemData {
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

        create(item: Omit<Item, 'id'>): Promise<Item> {
            const on_error = (messages: string[]) => {
                console.error('Error in items create API:', messages);
            };
            return client.post<Item>('/api/items', on_error, item);
        },

        remove(id: string): Promise<null> {
            const on_error = (messages: string[]) => {
                console.error('Error in items remove API:', messages);
            };
            return client.delete(`/api/items/${id}`, on_error);
        }
    };
}
