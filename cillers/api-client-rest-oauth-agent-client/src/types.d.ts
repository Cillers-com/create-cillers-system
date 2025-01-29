declare module 'swagger-ui-dist/swagger-ui-standalone-preset';

interface DefaultQueryParameter {
  name: string;
  in: string;
  schema?: {
    type: string;
    properties: {
      name: {
        type: string;
      };
    };
  };
  type?: string;
}

interface DefaultQuery {
  operationId: string;
  parameters: DefaultQueryParameter[];
}

interface ApiClientRestProps {
  spec: object;
  csrf: string;
}
