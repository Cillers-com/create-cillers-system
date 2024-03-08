import { User, UserManager } from 'oidc-client-ts';
import config from '../config';

const settings = {
  authority: config.oidcAuthority,
  client_id: config.oidcClientId,
  redirect_uri: `${window.location.origin}/auth/callback`,
  post_logout_redirect_uri: window.location.origin,
  response_type: 'code',
  scope: config.oidcScopes
};

const userManager = new UserManager(settings);

export const signIn = (): Promise<void> => {
  return userManager.signinRedirect();
};

export const signOut = (): Promise<void> => {
  return userManager.signoutRedirect();
};

export const getUser = async () => {
  return userManager.getUser();
};

export const signInCallback = (): Promise<User> => {
  return userManager.signinRedirectCallback();
};

export const getAccessToken = async (): Promise<string | null> => {
  const user = await userManager.getUser();
  return user?.access_token ? user.access_token : null;
};
