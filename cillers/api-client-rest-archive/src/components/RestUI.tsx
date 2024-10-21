import React from 'react';
import SwaggerUI from 'swagger-ui-react';
import SwaggerUIStandalonePreset from 'swagger-ui-dist/swagger-ui-standalone-preset';
import 'swagger-ui-react/swagger-ui.css';

interface RestUIProps {
  url: string;
  csrf: string;
}

const RestUI: React.FC<RestUIProps> = ({ url, csrf }) => {
  const requestInterceptor = (req: any) => {
    if (!req.headers['X-CSRF-Token']) {
      req.headers['X-CSRF-Token'] = csrf;
    }
    return req;
  };

  const defaultQueries = [
    {
      operationId: 'getHello',
      parameters: [],
    },
    {
      operationId: 'getItems',
      parameters: [],
    },
    {
      operationId: 'postItem',
      parameters: [
        {
          name: 'body',
          in: 'body',
          schema: {
            type: 'object',
            properties: {
              name: {
                type: 'string',
              },
            },
          },
        },
      ],
    },
    {
      operationId: 'deleteItem',
      parameters: [
        {
          name: 'ID',
          in: 'path',
          type: 'string',
        },
      ],
    },
  ];

  return (
    <div className="swagger-container">
      <SwaggerUI
        url={url}
        requestInterceptor={requestInterceptor}
        withCredentials={true}
        defaultModelsExpandDepth={-1}
        presets={[SwaggerUIStandalonePreset]}
        plugins={[
          (system: any) => ({
            statePlugins: {
              spec: {
                wrapSelectors: {
                  allowTryItOutFor: () => () => true,
                },
              },
            },
            wrapComponents: {
              operation: (Original: any, { React }: any) => (props: any) => {
                const defaultQuery = defaultQueries.find(
                  (q) => q.operationId === props.operation.get('operationId')
                );
                if (defaultQuery) {
                  props = {
                    ...props,
                    operation: props.operation.set(
                      'parameters',
                      props.operation.get('parameters').map((param: any) => {
                        const defaultParam = defaultQuery.parameters.find(
                          (p) => p.name === param.get('name')
                        );
                        return defaultParam
                          ? param.set('default', defaultParam.schema ? JSON.stringify(defaultParam.schema) : defaultParam.type)
                          : param;
                      })
                    ),
                  };
                }
                return <Original {...props} />;
              },
            },
          }),
        ]}
      />
    </div>
  );
};

export default RestUIComponent;
