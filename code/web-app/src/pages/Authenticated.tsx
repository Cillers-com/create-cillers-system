import React from "react";
import Products from "./Products";
import GameBoard from "./GameBoard";

interface AuthenticatedProps {
  userInfo: Record<string, any>;
  logout: () => void;
}

const testSize = 5; // This will create a 5x5 grid
const testCoordinates = [
  { x: 1, y: 1 },
  { x: 2, y: 3 },
  { x: 0, y: 4 },
  // Add as many coordinates as you want to test
];

const Authenticated: React.FC<AuthenticatedProps> = ({ userInfo, logout }) => {
  return (
    <>
      <p>Authenticated as: {JSON.stringify(userInfo)}</p>
      <button onClick={logout}>Logout</button>
      <Products />
      <GameBoard size={testSize} coordinates={testCoordinates} />
    </>
  );
};

export default Authenticated;
