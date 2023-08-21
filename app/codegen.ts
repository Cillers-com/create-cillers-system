import type { CodegenConfig } from '@graphql-codegen/cli';

const config: CodegenConfig = {
  overwrite: true,
  schema: [
    "src/graphql/**/*.graphql", 
    "node_modules/apollo-couchbase/src/graphql/**/*.graphql"
  ],
  generates: {
    "src/graphql/generated-types.ts": {
      plugins: ["typescript", "typescript-resolvers"],
      config: {
        useIndexSignature: true
      },
    }, 
  }
};

export default config;