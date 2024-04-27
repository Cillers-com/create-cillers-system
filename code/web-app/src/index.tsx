import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { ApolloProvider } from '@apollo/client';
import client from './apolloClient';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

/* Cannot use StrictMode because of oauthAgent timing issues when components are rerendered twice in dev mode. 
 * Cookies and csrf tokens can become set in the wrong order. 
*/
root.render(
    <>
        <ApolloProvider client={client}>
            <App />
        </ApolloProvider>
    </>
);

reportWebVitals();
