import React, { useState, useEffect } from 'react';
import ApiClientRest from './ApiClientRest';

interface AuthenticatedProps {
  userInfo: Record<string, any>;
  logout: () => void;
  csrf: string;
}

function on_graphql_error(messages: string[]) {
  messages.forEach(message => alert(message));
}

const Authenticated: React.FC<AuthenticatedProps> = ({ userInfo, logout, csrf }) => {
  const [spec, setSpec] = useState<object | null>(null);

  useEffect(() => {
    const fetchSpec = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/openapi.json`, {
          credentials: 'include'
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setSpec(data);
      } catch (error) {
        console.error('Error fetching OpenAPI spec:', error);
        on_graphql_error(['Failed to fetch OpenAPI specification']);
      }
    };

    fetchSpec();
  }, []);

  return (
    <>
      <div>
        Authenticated as: {JSON.stringify(userInfo)}
      </div>
      <button onClick={logout}>
        Logout
      </button>
      {spec ? (
        <ApiClientRest
          spec={spec}
          csrf={csrf}
        />
      ) : (
        <div>Loading API specification...</div>
      )}
    </>
  );
};

export default Authenticated;
