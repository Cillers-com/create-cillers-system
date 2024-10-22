import { gql } from '@apollo/client';

export const ITEMS = gql`
  query ItemsGet {
    items { name, id }
  }
`;

export const ITEMS_CREATE = gql`
  mutation ItemCreate($items: [ItemCreateInput!]!) {
    itemsCreate(items: $items) {
        name 
        id
    }
  }
`;

export const ITEMS_REMOVE = gql`
  mutation ItemsRemove($ids: [String!]!) {
    itemsRemove(ids: $ids) 
  }
`;

export const ITEMS_CREATED = gql`
  subscription OnItemCreated {
    itemsCreated { name, id }
  }
`;
