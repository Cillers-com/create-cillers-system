import { gql } from '@apollo/client';

export const ITEMS_CREATE = gql`
  mutation ItemsCreate($items: [ItemCreateInput!]!) {
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

export const ITEMS_SUBSCRIPTION = gql`
    subscription Items {
        items {
            existing {
                id
                name
            }
            created {
                id
                name
            }
            updated {
                id
                name
            }
            removed
        }
    }
`;
