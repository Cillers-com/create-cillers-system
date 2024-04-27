type AppConfig = {
  apiBaseUrl: string;
  oauthAgentBaseUrl: string;
  oidcAuthority: string;
  oidcClientId: string;
  oidcScopes: string;
};

function loadConfig(): AppConfig {
  const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
  const oauthAgentBaseUrl = process.env.REACT_APP_OAUTH_AGENT_BASE_URL; 
  const oidcAuthority = process.env.REACT_APP_OIDC_AUTHORITY;
  const oidcClientId = process.env.REACT_APP_OIDC_CLIENT_ID;
  const oidcScopes = process.env.REACT_APP_OIDC_SCOPES || 'openid profile email';

  if (!apiBaseUrl) throw new Error("REACT_APP_API_BASE_URL has not been set.");
  if (!oauthAgentBaseUrl) throw new Error("REACT_APP_OAUTH_BASE_URL has not been set");
  if (!oidcAuthority) throw new Error("REACT_APP_OIDC_AUTHORITY has not been set.");
  if (!oidcClientId) throw new Error("REACT_APP_OIDC_CLIENT_ID has not been set.");

  return { apiBaseUrl, oauthAgentBaseUrl, oidcAuthority, oidcClientId, oidcScopes };
}

const config = loadConfig();

export default config;
