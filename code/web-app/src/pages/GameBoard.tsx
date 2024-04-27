import React, { useState, useEffect } from "react";
import styles from "./GameBoard.module.css";

type Coordinate = { x: number; y: number };
type GameBoardProps = {
  size: number;
  coordinates: Coordinate[];
};

const GameBoard: React.FC<GameBoardProps> = ({ size, coordinates }) => {
  const [grid, setGrid] = useState<boolean[][]>([]);
  const [currentBlock, setCurrentBlock] = useState<Coordinate | null>(null);
  const [userSelections, setUserSelections] = useState<Coordinate[]>([]);
  const [showResults, setShowResults] = useState<boolean>(false);

  useEffect(() => {
    // Initialize the grid based on the size prop
    const initialGrid = Array.from({ length: size }, () =>
      new Array<boolean>(size).fill(false)
    );
    setGrid(initialGrid);
    showBlocks(coordinates);
  }, [size, coordinates]);

  const showBlocks = async (blocks: Coordinate[]) => {
    for (let block of blocks) {
      setCurrentBlock(block);
      await new Promise((resolve) => setTimeout(resolve, 1000)); // show each block for 1 second
      setCurrentBlock(null);
    }
    setTimeout(() => {
      setShowResults(true);
      sendResults();
    }, 10000); // After showing all blocks, wait 10 seconds to collect answers
  };

  const handleBlockClick = (x: number, y: number) => {
    if (!showResults) {
      const updatedSelections = [...userSelections, { x, y }];
      setUserSelections(updatedSelections);
    }
  };

  const sendResults = () => {
    // Placeholder for sending results to a server
    console.log("Sending results to server:", userSelections);
    // TODO: Replace with actual API call
  };

  return (
    <div className={styles["game-board"]}>
      {grid.map((row, rowIndex) => (
        <div key={rowIndex} className={styles["row"]}>
          {row.map((_, colIndex) => (
            <div
              key={`${rowIndex}-${colIndex}`}
              className={`${styles["cell"]} ${
                currentBlock &&
                currentBlock.x === rowIndex &&
                currentBlock.y === colIndex
                  ? styles["active"]
                  : ""
              }`}
              onClick={() => handleBlockClick(rowIndex, colIndex)}
            >
              {showResults && (
                <>
                  {coordinates.some(
                    (coord) => coord.x === rowIndex && coord.y === colIndex
                  ) && <span className={styles["correct"]}>✓</span>}
                  {userSelections.some(
                    (sel) => sel.x === rowIndex && sel.y === colIndex
                  ) && <span className={styles["user-selected"]}></span>}
                </>
              )}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default GameBoard;
