import React, {useState} from 'react';
import {RemoteError} from '../../utilities/remoteError';
import {CallApiProps} from './callApiProps';
import {CallApiState} from './callApiState';

export function CallApiView(props: CallApiProps) {

    const [state, setState] = useState<CallApiState | null>({
        result: '',
        query: 'query Query { dummy }',
        variables: '',  // new field
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
                const data = await props.apiClient.graphqlFetch(state.query, state.variables);
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

    const handleQueryChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
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

    const handleVariablesChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setState(prevState => {
            if (prevState) {
                return {
                    ...prevState,
                    variables: e.target.value
                };
            }
            return null;
        });
    };

    return (
        <div className='container'>
            <h2>Call APIs</h2>
            <p>{getAccessTokenDescription()}</p>
            <textarea
                value={state ? state.query : ''}
                onChange={handleQueryChange}
                className="form-control mb-3"
                placeholder="Enter your GraphQL query"
            />
            <textarea 
                value={state ? state.variables : ''} 
                onChange={handleVariablesChange} 
                className="form-control mb-3" 
                placeholder="Enter your GraphQL variables as JSON">
            </textarea>
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
