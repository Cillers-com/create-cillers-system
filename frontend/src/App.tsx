import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import SignInCallbackPage from './pages/SignInCallbackPage';
import PrivateRoute from './pages/PrivateRoute';
import { loadErrorMessages, loadDevMessages } from "@apollo/client/dev";

const isDev = process.env.NODE_ENV === 'development';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/auth/callback" element={<SignInCallbackPage />} />
        <Route path="/" element={<PrivateRoute />}>
          <Route index element={<HomePage />} />
        </Route>
      </Routes>
    </Router>
  );
}

if (isDev) {
  loadDevMessages();
  loadErrorMessages();
}

export default App;
