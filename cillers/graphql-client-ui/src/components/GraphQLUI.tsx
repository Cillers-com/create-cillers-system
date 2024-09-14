import React from 'react'
import { createGraphiQLFetcher } from '@graphiql/toolkit';
import GraphiQL from "graphiql";

const url = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8080/api';

const createFetcher = (csrf: string) => createGraphiQLFetcher({
  url,
  fetch: async (input, init = {}) => {
    return fetch(input, {
      ...init,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        "x-curity-csrf": csrf,
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

const helloAdminQuery = `query HelloAdmin {
  helloAdmin {
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
    query: helloAdminQuery
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

const GraphQLUI: React.FC<{ csrf: string }> = ({ csrf }) => {
  const fetcher = React.useMemo(() => createFetcher(csrf), [csrf]);

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

