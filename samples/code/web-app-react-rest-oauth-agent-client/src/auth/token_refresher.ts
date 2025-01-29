import { refresh_token as oauth_refresh_token } from './oauth_agent_client';

let refresh_promise: Promise<boolean> | null = null;

export function refresh_token(): Promise<boolean> {
    if (refresh_promise) {
        return refresh_promise;
    }

    refresh_promise = (async () => {
        try {
            const result = await oauth_refresh_token();
            return result;
        } catch (error) {
            console.error('Token refresh failed:', error);
            return false;
        } finally {
            refresh_promise = null;
        }
    })();

    return refresh_promise;
}
