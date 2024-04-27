import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Main from "./pages/Main";
import AuthCallback from "./pages/AuthCallback";
import { loadErrorMessages, loadDevMessages } from "@apollo/client/dev";
import GameBoard from "./pages/GameBoard"; // Adjust the path based on your file structure

const isDev = process.env.NODE_ENV === "development";

const testSize = 5; // This will create a 5x5 grid
const testCoordinates = [
  { x: 1, y: 1 },
  { x: 2, y: 3 },
  { x: 0, y: 4 },
  // Add as many coordinates as you want to test
];

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/auth/callback" element={<AuthCallback />} />
        <Route path="/" element={<Main />} />
        <Route
          path="/game"
          element={<GameBoard size={testSize} coordinates={testCoordinates} />}
        />
      </Routes>
    </Router>
  );
};

if (isDev) {
  loadDevMessages();
  loadErrorMessages();
}

export default App;
