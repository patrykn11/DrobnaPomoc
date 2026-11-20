import { useState } from "react";
import { useAuth } from "../useAuth";

export function LoginForm() {
    const { login } = useAuth();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();
        setError("");
        setSubmitting(true);

        try {
            await login(username.trim(), password);
        } catch (requestError) {
            if (requestError.status === 400) {
                setError("Nieprawidłowa nazwa użytkownika lub hasło.");
            } else {
                setError("Nie udało się połączyć z serwerem. Spróbuj ponownie.");
            }
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="loginUsername">Nazwa użytkownika</label>
            <input
                id="loginUsername"
                autoComplete="username"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                required
            />

            <label htmlFor="loginPassword">Hasło</label>
            <input
                id="loginPassword"
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
            />

            {error && (
                <div className="form-error" role="alert">
                    {error}
                </div>
            )}

            <button className="auth-submit" type="submit" disabled={submitting}>
                {submitting ? "Logowanie..." : "Zaloguj się"}
            </button>
        </form>
    );
}
