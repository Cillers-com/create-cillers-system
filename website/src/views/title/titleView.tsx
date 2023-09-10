import React from 'react';
import { SignOutView } from '../signOut/signOutView';
import { OAuthClient } from '../../oauth/oauthClient';

interface TitleViewProps {
    isLoggedIn: boolean;
    oauthClient?: OAuthClient | null;
    onLoggedOut: () => void;
}

export function TitleView({ isLoggedIn, oauthClient, onLoggedOut }: TitleViewProps) {
    return (
        <div className='container spacer'>
            <h1>Single Page App</h1>
            
            {isLoggedIn && oauthClient &&
                <SignOutView 
                    oauthClient={oauthClient}
                    onLoggedOut={onLoggedOut} />
            }
        </div>
    );
}
