import React from "react";
import Games from "./Games";
import { gameConfig } from "../config/gameConfig";
import GameBoard from "./GameBoard";

interface AuthenticatedProps {
  userInfo: Record<string, any>;
  logout: () => void;
}

const Authenticated: React.FC<AuthenticatedProps> = ({ userInfo, logout }) => {
  return (
    <>
      <p>Authenticated as: {JSON.stringify(userInfo)}</p>
      <button onClick={logout}>Logout</button>
      <Games userInfo={userInfo} />
      <GameBoard size={gameConfig.size} coordinates={gameConfig.coordinates} />
    </>
  );
};

export default Authenticated;
