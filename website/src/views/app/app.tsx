import React, { useEffect, useState } from 'react';
import { StorageHelper } from '../../utilities/storageHelper';
import { TitleView } from '../title/titleView';
import { AppProps } from './appProps';
import { AppState } from './appState';
import { UnauthenticatedApp } from './UnauthenticatedApp';  // Assuming they're in the same directory
import { AuthenticatedApp } from './AuthenticatedApp';      // Assuming they're in the same directory

export default function App(props: AppProps) {
    const [state, setState] = useState<AppState | null>(null);
    const storage = new StorageHelper(() => multiTabLogout());

    useEffect(() => {
        startup();
        return () => cleanup();
    }, []);

    async function startup() {
        window.addEventListener('storage', storage.onChange);
        await props.viewModel.initialize();

        setState({
            isLoaded: false,
            isLoggedIn: false,
            sessionExpired: false,
        });
    }

    function cleanup() {
        window.removeEventListener('storage', storage.onChange);
    }

    function setIsLoaded() {
        setState((prevState: any) => {
            return {
                ...prevState,
                isLoaded: true,
            };
        });
    }

    function setIsLoggedIn() {
        storage.setLoggedOut(false);
        setState((prevState: any) => {
            return {
                ...prevState,
                isLoggedIn: true,
                sessionExpired: false,
            };
        });
    }

    function setIsLoggedOut() {
        storage.setLoggedOut(true);
        setState((prevState: any) => {
            return {
                ...prevState,
                isLoggedIn: false,
                sessionExpired: true,
            };
        });
    }

    async function multiTabLogout() {
        await props.viewModel.oauthClient!.onLoggedOut();
        setIsLoggedOut();
    }

    return (
        <>
            <TitleView 
                isLoggedIn={state?.isLoggedIn || false}
                oauthClient={props.viewModel.oauthClient}
                onLoggedOut={setIsLoggedOut}
            />
            
            {state && !state.isLoggedIn && 
                <UnauthenticatedApp 
                    viewModel={props.viewModel} 
                    onLoaded={setIsLoaded}
                    onLoggedIn={setIsLoggedIn}
                    onLoggedOut={setIsLoggedOut} />
            }

            {state && state.isLoaded && state.isLoggedIn &&
                <AuthenticatedApp 
                    viewModel={props.viewModel}
                    onLoggedOut={setIsLoggedOut} />
            }
        </>
    );
}
