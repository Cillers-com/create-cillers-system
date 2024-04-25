import { gql } from '@apollo/client';

export const GET_HELLO = gql`
  query GetHello {
    hello { message }
  }
`;

export const GET_PRODUCTS = gql`
  query GetProducts {
    products { name, id }
  }
`;

export const ADD_PRODUCT = gql`
  mutation AddProduct($name: String!) {
    addProduct(name: $name) { name, id }
  }
`;

export const REMOVE_PRODUCT = gql`
  mutation RemoveProduct($id: String!) {
    removeProduct(id: $id)
  }
`;

export const PRODUCT_ADDED_SUBSCRIPTION = gql`
  subscription OnProductAdded {
    productAdded { name, id }
  }
`;
