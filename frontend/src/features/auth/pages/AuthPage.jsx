import { useState } from "react";
import { LoginForm } from "../components/LoginForm";
import { RegisterForm } from "../components/RegisterForm";
import "./AuthPage.css";

export function AuthPage() {
    const [mode, setMode] = useState("login");
    const isLogin = mode === "login";

    return (
        <main className="auth-page">
            <section className="auth-card">
                <div className="auth-tabs">
                    <button
                        type="button"
                        className={isLogin ? "auth-tab auth-tab--active" : "auth-tab"}
                        onClick={() => setMode("login")}
                    >
                        Logowanie
                    </button>

                    <button
                        type="button"
                        className={!isLogin ? "auth-tab auth-tab--active" : "auth-tab"}
                        onClick={() => setMode("register")}
                    >
                        Rejestracja
                    </button>
                </div>

                <h1>{isLogin ? "Zaloguj się" : "Utwórz konto"}</h1>

                {isLogin ? <LoginForm /> : <RegisterForm />}
            </section>
        </main>
    );
}
