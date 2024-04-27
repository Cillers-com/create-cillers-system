import { gql } from "@apollo/client";

export const GET_HELLO = gql`
  query GetHello {
    hello {
      message
    }
  }
`;

export const GET_PRODUCTS = gql`
  query GetProducts {
    products {
      name
      id
    }
  }
`;

export const ADD_PRODUCT = gql`
  mutation AddProduct($name: String!) {
    addProduct(name: $name) {
      name
      id
    }
  }
`;

export const REMOVE_PRODUCT = gql`
  mutation RemoveProduct($id: String!) {
    removeProduct(id: $id)
  }
`;

export const PRODUCT_ADDED_SUBSCRIPTION = gql`
  subscription OnProductAdded {
    productAdded {
      name
      id
    }
  }
`;

export const ADD_GAME = gql`
  mutation AddGame($name: String!, $host: String!) {
    addGame(name: $name, host: $host) {
      name
      host
    }
  }
`;

export const ADD_PLAYER = gql`
  mutation AddPlayer($gameName: String!, $name: String!) {
    addPlayer(gameName: $gameName, name: $name)
  }
`;

export const LIST_PLAYERS = gql`
  query ListPlayers($gameName: String!) {
    listPlayers(gameName: $gameName)
  }
`;
