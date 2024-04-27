import React, { useState } from "react";
import { useQuery, useMutation } from "@apollo/client";
import { ADD_GAME, ADD_PLAYER, LIST_PLAYERS } from "../graphql/operations";

const Products: React.FC = () => {
  const [addGame] = useMutation(ADD_GAME);
  const [addPlayer] = useMutation(ADD_PLAYER);

  const [newGameText, setNewGameText] = useState("");

  const loading = false;
  const error = undefined;

  if (loading)
    return (
      <div className="flex justify-center items-center min-h-screen bg-base-300">
        <button className="btn">
          <span className="loading loading-spinner"></span>
          Loading...
        </button>
      </div>
    );
  if (error) return <p>{"Error: " + error}</p>;

  const handleCreateGame = async () => {
    // TODO: get the playername.
    if (!newGameText.trim()) return;
    await addGame({ variables: { name: newGameText, host: "player" } });
    setNewGameText(newGameText);
  };

  const handleAddPlayer = async () => {
    // TODO: get the playername.
    const response = await addPlayer({
      variables: { gameName: newGameText, name: "player" },
    });
    if (response.data && !response.data["addPlayer"]) {
      // TODO: show error.
      return;
    }

    // TODO: re-render list.
  };

  return (
    <div className="min-h-screen flex flex-col">
      <div className="navbar bg-base-300 text-neutral-content">
        <div className="flex-1">
          <a href="/" className="p-2 normal-case text-xl">
            Game:
          </a>
          <input
            type="text"
            placeholder="Game name"
            className="join-item flex-grow input input-bordered input-md input-primary"
            value={newGameText}
            onChange={(e) => setNewGameText(e.target.value)}
          />
          <button
            className="join-item btn btn-square btn-md btn-primary"
            onClick={handleCreateGame}
          >
            Create
          </button>
          <button
            className="join-item btn btn-square btn-md btn-primary"
            onClick={handleAddPlayer}
          >
            Join
          </button>
        </div>
      </div>
    </div>
  );
};

export default Products;
