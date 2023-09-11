import React, {useState} from 'react';
import {RemoteError} from '../../utilities/remoteError';
import {CallApiProps} from './callApiProps';
import {CallApiState} from './callApiState';

export function CallApiView(props: CallApiProps) {

    const [state, setState] = useState<CallApiState | null>({
        result: '',
        query: '{ __schema { types { name } } }',
        error: null,
    });

    function isButtonDisabled(): boolean {
        return false;
    }

    function getAccessTokenDescription(): string {
        return "The SPA makes all API calls using SameSite cookies, with no tokens in the browser";
    }

    async function execute() {
        if (state && state.query) {
            try {
                const data = await props.apiClient.graphqlFetch(state.query);
                console.log(data);
                if (data.data) {
                    setState((state: any) => {
                        return {
                            ...state,
                            result: data.data,
                            error: null,
                        };
                    });
                }
            } catch (e) {
                const remoteError = e as RemoteError;
                if (remoteError) {
                    if (remoteError.isSessionExpiredError()) {
                        props.onLoggedOut();
                    } else {
                        setState((state: any) => {
                            return {
                                ...state,
                                result: '',
                                error: remoteError.toDisplayFormat(),
                            };
                        });
                    }
                }
            }
        }
    }

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setState(prevState => {
            if (prevState) {
                return {
                    ...prevState,
                    query: e.target.value
                };
            }
            return null;
        });
    };

    return (
        <div className='container'>
            <h2>Call APIs</h2>
            <p>{getAccessTokenDescription()}</p>
            <input
                type="text"
                value={state ? state.query : ''}
                onChange={handleInputChange}
                className="form-control mb-3"
                placeholder="Enter your GraphQL query"
            />
            <button
                id='getApiData'
                className='btn btn-primary operationButton'
                onClick={execute}
                disabled={isButtonDisabled()}>
                    Get Data
            </button>
            {state && state.result &&
            <div>
                <pre className='alert alert-success' id='getDataResult'>{JSON.stringify(state.result, null, 2)}</pre>
            </div>}
            {state && state.error &&
            <div>
                <p className='alert alert-danger' id='getDataErrorResult'>{state.error}</p>
            </div>}
            <hr/>
        </div>
    )
}
