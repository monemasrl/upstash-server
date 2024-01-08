import React, { useEffect } from 'react'
import { useAuth } from 'react-oidc-context'
import { Navigate } from 'react-router-dom'

interface IPrivateRouteProps {
  children: React.ReactNode
}

const PrivateRoute = (props: IPrivateRouteProps): JSX.Element => {
  const auth = useAuth();
  useEffect(() => {
    console.log("PrivateRoute: useEffect: auth.events.addAccessTokenExpiring")
    // return auth.events.addAccessTokenExpiring(() => {
    //     auth.signinSilent();
    // })
  }, [auth.events, auth.signinSilent]);
  switch (auth.activeNavigator) {
    case 'signinRedirect':
        return <div>Redirecting...</div>;
    case 'signinSilent':
        return <div>Redirecting...</div>;
    case 'signoutRedirect':
        return <div>Redirecting...</div>;
    case 'signoutPopup':
        return <div>Redirecting...</div>;
    default:
        break;
  }
  if (auth.isLoading) {
    return <div>Loading...</div>;
  }

  if (auth.error) {
      return <div>Ooops... {auth.error.message}</div>;
  }

  return <>{auth.isAuthenticated ? props.children : <Navigate to="/login" />}</>
}

export default PrivateRoute
