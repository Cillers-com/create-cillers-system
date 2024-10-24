import React, { useState, useEffect } from 'react';
import ApiClientRest from './ApiClientRest';

function on_graphql_error(messages: string[]) {
  messages.forEach(message => alert(message));
}

const Authenticated: React.FC = () => {
  const [spec, setSpec] = useState<object | null>(null);

  useEffect(() => {
    const fetchSpec = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/openapi.json`);
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
      {spec ? (
        <ApiClientRest
          spec={spec}
        />
      ) : (
        <div>Loading API specification...</div>
      )}
    </>
  );
};

export default Authenticated;
