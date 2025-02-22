import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Main from './components/Main';
import { loadErrorMessages, loadDevMessages } from "@apollo/client/dev";

const isDev = process.env.NODE_ENV === 'development';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="*" element={<Main />} />
      </Routes>
    </Router>
  )
}

if (isDev) {
  loadDevMessages();
  loadErrorMessages();
}

export default App;
