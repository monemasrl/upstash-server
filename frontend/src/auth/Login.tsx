import { Button } from "primereact/button";
import { useAuth } from "react-oidc-context";
import { Navigate } from "react-router-dom";

function Login() {
    const auth = useAuth();

    if (auth.isAuthenticated) {
        return <Navigate to="/" />;
    }
    return (
        <div>
            <Button label="Sign In with GitHub" icon="pi pi-github" className="w-full p-button-secondary" onClick={() => void auth.signinPopup()} />
        </div>
    );
}

export default Login;