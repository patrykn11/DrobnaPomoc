import { useState } from "react";
import { useAuth } from "../useAuth";

export function RegisterForm() {
    const { register } = useAuth();
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [passwordConfirmation, setPasswordConfirmation] = useState("");
    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();
        setError("");

        if (password !== passwordConfirmation) {
            setError("Podane hasła nie są takie same.");
            return;
        }

        setSubmitting(true);

        try {
            await register({
                username: username.trim(),
                email: email.trim(),
                first_name: firstName.trim(),
                last_name: lastName.trim(),
                password
            });
        } catch (requestError) {
            if (requestError.data) {
                const firstError = Object.values(requestError.data)[0];
                const message = Array.isArray(firstError) ? firstError[0] : firstError;
                setError(message || "Sprawdź poprawność podanych danych.");
            } else {
                setError("Nie udało się połączyć z serwerem. Spróbuj ponownie.");
            }
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <div className="name-fields">
                <div>
                    <label htmlFor="firstName">Imię</label>
                    <input
                        id="firstName"
                        autoComplete="given-name"
                        value={firstName}
                        onChange={(event) => setFirstName(event.target.value)}
                        required
                    />
                </div>

                <div>
                    <label htmlFor="lastName">Nazwisko</label>
                    <input
                        id="lastName"
                        autoComplete="family-name"
                        value={lastName}
                        onChange={(event) => setLastName(event.target.value)}
                        required
                    />
                </div>
            </div>

            <label htmlFor="registerUsername">Nazwa użytkownika</label>
            <input
                id="registerUsername"
                autoComplete="username"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                required
            />

            <label htmlFor="email">Adres e-mail</label>
            <input
                id="email"
                type="email"
                autoComplete="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
            />

            <label htmlFor="registerPassword">Hasło</label>
            <input
                id="registerPassword"
                type="password"
                autoComplete="new-password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
            />

            <label htmlFor="passwordConfirmation">Powtórz hasło</label>
            <input
                id="passwordConfirmation"
                type="password"
                autoComplete="new-password"
                value={passwordConfirmation}
                onChange={(event) => setPasswordConfirmation(event.target.value)}
                required
            />

            {error && (
                <div className="form-error" role="alert">
                    {error}
                </div>
            )}

            <button className="auth-submit" type="submit" disabled={submitting}>
                {submitting ? "Tworzenie konta..." : "Utwórz konto"}
            </button>
        </form>
    );
}
