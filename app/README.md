# Apollo On The Couch

A framework for building GraphQL APIs with the Apollo GraphQL server backed by Couchbase. The main purpose of this 
framework is to make it simple to build super scalable and reliable APIs quickly and cost-effectively. 

## Getting Started

### Prerequisites 
* [A Couchbase Capella account or your own Couchbase server.](https://www.couchbase.com/downloads) 
* [Node.js](https://nodejs.org/en/download)
* [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or similar

### Create Your `Apollo On The Couch` Server Project
```bash
npx create-apollo-couchbase-server@latest my-server
```

#### Configure the Couchbase Environment Variables in the .env file


##### Capella database
```bash
PORT=4000
LOCAL=true

COUCHBASE_USER=username
COUCHBASE_PASSWORD=password
COUCHBASE_ENDPOINT=couchbases://cb.yourendpoint.cloud.couchbase.com
COUCHBASE_DEFAULT_BUCKET=_default
COUCHBASE_DEFAULT_SCOPE=_default
COUCHBASE_IS_CLOUD_INSTANCE=true
```

##### Localhost database
```bash
PORT=4000
LOCAL=true

COUCHBASE_USER=username
COUCHBASE_PASSWORD=password
COUCHBASE_ENDPOINT=couchbase://localhost
COUCHBASE_DEFAULT_BUCKET=_default
COUCHBASE_DEFAULT_SCOPE=_default
COUCHBASE_IS_CLOUD_INSTANCE=false
```


### Generate an ```apollo-couchbase``` resource 
In `apollo-couchbase`, the GraphQL schema and resolvers are structured in what's called `resources`. These resources will typically be very similar to REST resources, with CrUD operations.  

You can use a scaffolding script, `generate-resource`, to generate a new resource. This script will generate resources with scaffold resolvers and schema files that you can edit to fit your purposes.  

You also have the flexibility to create your own resources that can contain any type of API resolvers and schema. 

To create a resource using the scaffolding script, follow these steps:

#### Run the generate-resource script:
```bash
npm run generate-resource <resourceNameInPlural>
```

#### Edit the ./src/graphql/resources/`<resourceNameInPlural>`/schema.graphql file. Fill in the properties you want to expose on the resource.
E.g.
```graphql
type AccountContent {
    name: String!
    phone: String
}

input AccountContentInput {
  name: String!
  phone: String
}

input AccountContentPatchInput {
  name: String
  phone: String
}

input AccountsListFiltersInput {
  name: String
}
```
Notice that there is no exclamation mark in the `AccountContentPatchInput` input, since you probably don't want to require any field to be included when patching records. 

#### Run the generate-graphql-types script:
```bash
npm run generate-graphql-types
```

### Start the server
```bash
npm run dev
```
