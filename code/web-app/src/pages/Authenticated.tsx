import React from "react";
import Games from "./Games";

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
    </>
  );
};

export default Authenticated;
