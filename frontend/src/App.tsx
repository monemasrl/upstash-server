import 'primeflex/primeflex.css'; // flex
import 'primeicons/primeicons.css';
import 'primereact/resources/themes/saga-blue/theme.css';

import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Login from './auth/Login';
import Test from './main/test';
import PrivateRoute from './routes/PrivateRoute';

function App() {

  return (
    <Routes>
      <Route
        path="*"
        element={
          <PrivateRoute>
            <React.StrictMode>
              <Routes>
                <Route path="/" element={<Test />} />
                <Route path="/documentation" element={<Test />} />
              </Routes>
            </React.StrictMode>
          </PrivateRoute>
        }
      />
      <Route
        path="login"
        element={
            <Login />
        }
      />
    </Routes>
  )
}

export default App
