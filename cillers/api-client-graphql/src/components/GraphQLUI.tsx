import React from 'react'
import { createGraphiQLFetcher } from '@graphiql/toolkit';
import GraphiQL from "graphiql";

const url = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8080/api';

const createFetcher = () => createGraphiQLFetcher({
  url,
  fetch: async (input, init = {}) => {
    return fetch(input, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...init.headers,
      },
    });
  },
});

const helloQuery = `query Hello {
  hello {
    message
  }
}
`;

const itemsCreateMutation = `mutation ItemsCreate {
  itemsCreate(items: [{name: "B"}]) {
    name
		id
  }
}
`;

const itemsQuery = ` query Items {
  items {
		name
		id
	}
}
`;

const itemsRemoveMutation = `mutation ItemsRemove {
  itemsRemove(ids: [""])
}
`;

const tabs = [
  {
    query: helloQuery
  },
  {
    query: itemsQuery
  },
  {
    query: itemsCreateMutation
  },
  {
    query: itemsRemoveMutation
  }
]

const GraphQLUI: React.FC = () => {
  const fetcher = React.useMemo(() => createFetcher(), []);

  return (
    <div style={{ height: '90vh', width: '100%' }}>
      <GraphiQL
        fetcher={fetcher}
        defaultTabs={tabs}
      />
    </div>
  );
}

export default GraphQLUI

