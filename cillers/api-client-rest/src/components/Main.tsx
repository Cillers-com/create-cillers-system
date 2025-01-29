import React, { useState, useEffect } from 'react';
import ApiClientRest from './ApiClientRest';


const Main: React.FC = () => {
  const [spec, setSpec] = useState<object | null>(null);

  useEffect(() => {
    const fetchSpec = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/openapi.json`, {});
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setSpec(data);
      } catch (error) {
        console.error('Error fetching OpenAPI spec:', error);
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
}

export default Main;
