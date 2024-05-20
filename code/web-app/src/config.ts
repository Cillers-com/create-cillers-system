type AppConfig = {
  api_base_url: string;
  oauth_agent_base_url: string;
};

function loadConfig(): AppConfig {
  const api_base_url = process.env.REACT_APP_API_BASE_URL;
  const oauth_agent_base_url = process.env.REACT_APP_OAUTH_AGENT_BASE_URL; 

  if (!api_base_url) throw new Error("REACT_APP_API_BASE_URL has not been set.");
  if (!oauth_agent_base_url) throw new Error("REACT_APP_OAUTH_BASE_URL has not been set");

  return { 
      api_base_url, 
      oauth_agent_base_url, 
  };
}

const config = loadConfig();

export default config;
