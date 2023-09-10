import React from 'react';
import {UserInfoView} from '../userInfo/userInfoView';
import {ClaimsView} from '../claims/claimsView';
import {CallApiView} from '../callApi/callApiView';

interface AuthenticatedAppProps {
    viewModel: any;
    onLoggedOut: () => void;
}

export const AuthenticatedApp: React.FC<AuthenticatedAppProps> = (props) => {
    const { viewModel, onLoggedOut } = props;

    return (
        <>
            <UserInfoView 
                oauthClient={viewModel.oauthClient!}
                onLoggedOut={onLoggedOut} />

            <ClaimsView 
                oauthClient={viewModel.oauthClient!}
                onLoggedOut={onLoggedOut} />

            <CallApiView 
                apiClient={viewModel.apiClient!}
                onLoggedOut={onLoggedOut} />

        </>
    );
};
