import 'primeflex/primeflex.css';
import React from 'react';
import ReactDOM from 'react-dom/client';
import type { AuthProviderNoUserManagerProps } from 'react-oidc-context';
import { AuthProvider } from 'react-oidc-context';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App.tsx';
import ErrorPage from './ErrorPage.tsx';
import './index.css';
import './styles/layout/layout.scss';

const authProviderProps: AuthProviderNoUserManagerProps = {
  authority: 'https://auth.service.monema.dev',
  client_id: 'upstash-app',
  response_mode: 'fragment',
  redirect_uri: 'http://localhost:5173',
  response_type: 'code',
  scope: 'openid profile email',
  metadataUrl: 'https://auth.service.monema.dev/realms/upstash/.well-known/openid-configuration',
}


const router = createBrowserRouter([
  {
    path: '*',
    element: <App />,
    errorElement: <ErrorPage />,
  }
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AuthProvider {...authProviderProps}>
      <RouterProvider router={router} />
    </AuthProvider>
  </React.StrictMode>,
)
