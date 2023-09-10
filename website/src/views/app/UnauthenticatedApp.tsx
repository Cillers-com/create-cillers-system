import React from 'react';
import {PageLoadView} from '../pageLoad/pageLoadView';
import {StartAuthenticationView} from '../startAuthentication/startAuthenticationView';

interface UnauthenticatedAppProps {
    viewModel: any;
    onLoaded: () => void;
    onLoggedIn: () => void;
    onLoggedOut: () => void;
}

export const UnauthenticatedApp: React.FC<UnauthenticatedAppProps> = (props) => {
    const { viewModel, onLoaded, onLoggedIn, onLoggedOut } = props;

    return (
        <>
            <PageLoadView 
                oauthClient={viewModel.oauthClient!}
                onLoaded={onLoaded}
                onLoggedIn={onLoggedIn}
                onLoggedOut={onLoggedOut} />

            <StartAuthenticationView 
                oauthClient={viewModel.oauthClient!} />
        </>
    );
};
