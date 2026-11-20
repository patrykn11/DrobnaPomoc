import { useEffect, useState } from "react";
import AuthService from "./api/authApi";
import { AuthContext } from "./context";

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function checkSession() {
            if (!AuthService.hasSession()) {
                setIsLoading(false);
                return;
            }

            try {
                const currentUser = await AuthService.getCurrentUser();
                setUser(currentUser);
            } catch {
                AuthService.clearTokens();
            }

            setIsLoading(false);
        }

        checkSession();
    }, []);

    async function login(username, password) {
        const tokens = await AuthService.loginUser(username, password);
        AuthService.saveTokens(tokens);

        try {
            const currentUser = await AuthService.getCurrentUser();
            setUser(currentUser);
        } catch (error) {
            AuthService.clearTokens();
            throw error;
        }
    }

    async function register(formData) {
        await AuthService.registerUser(formData);
        await login(formData.username, formData.password);
    }

    async function logout() {
        try {
            await AuthService.logoutUser();
        } catch {
            // user wylogowywany bez polaczenia
        }

        AuthService.clearTokens();
        setUser(null);
    }

    return (
        <AuthContext.Provider
            value={{
                user,
                isLoading,
                isAuthenticated: user !== null,
                login,
                register,
                logout
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}
