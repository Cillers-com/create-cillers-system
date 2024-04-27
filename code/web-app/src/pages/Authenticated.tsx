import React from "react";
import Games from "./Games";
import GameBoard from "./GameBoard";
import { gameConfig } from "../config/gameConfig";

interface AuthenticatedProps {
  userInfo: Record<string, any>;
  logout: () => void;
}

const Authenticated: React.FC<AuthenticatedProps> = ({ userInfo, logout }) => {
  return (
    <>
      <p>Authenticated as: {JSON.stringify(userInfo)}</p>
      <button onClick={logout}>Logout</button>
      <Games />
      <GameBoard size={gameConfig.size} coordinates={gameConfig.coordinates} />
    </>
  );
};

export default Authenticated;
