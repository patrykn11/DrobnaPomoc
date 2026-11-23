import { AuthProvider } from "../features/auth/AuthContext";
import { AuthPage } from "../features/auth/pages/AuthPage";
import { useAuth } from "../features/auth/useAuth";
import { AppLayout } from "../layouts/AppLayout";
import "./App.css";

function AppContent() {
    const { isAuthenticated, isLoading } = useAuth();
    if (isLoading) {
        return (
            <div className="app-loader" role="status">
                Ładowanie...
            </div>
        );
    }
    return isAuthenticated ? <AppLayout /> : <AuthPage />;
}

export default function App() {
    return (
        <AuthProvider>
            <AppContent />
        </AuthProvider>
    );
}
