import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "./App";
import api from "../shared/api/api";

vi.mock("../shared/api/api", () => ({
    default: {
        get: vi.fn(),
        post: vi.fn()
    }
}));

describe("App", () => {
    afterEach(() => {
        cleanup();
        localStorage.clear();
        vi.clearAllMocks();
        vi.restoreAllMocks();
    });

    it("pokazuje formularz logowania bez zapisanej sesji", async () => {
        render(<App />);
        expect(await screen.findByRole("heading", { name: "Zaloguj się" })).toBeInTheDocument();
    });

    it("loguje użytkownika i pokazuje wspólny układ aplikacji", async () => {
        api.post.mockResolvedValueOnce({
            data: { access: "access", refresh: "refresh" }
        });
        api.get.mockResolvedValueOnce({
            data: {
                id: 1,
                username: "jan",
                first_name: "Jan",
                last_name: "Kowalski"
            }
        });

        render(<App />);

        fireEvent.change(await screen.findByLabelText("Nazwa użytkownika"), {
            target: { value: "jan" }
        });
        fireEvent.change(screen.getByLabelText("Hasło"), {
            target: { value: "haslo123" }
        });
        fireEvent.click(screen.getByRole("button", { name: "Zaloguj się" }));

        await waitFor(() => expect(screen.getByText("Jan Kowalski")).toBeInTheDocument());
        expect(screen.getByRole("navigation", { name: "Menu główne" })).toBeInTheDocument();
    });

    it("pokazuje odpowiedni komunikat po podaniu błędnego hasła", async () => {
        vi.spyOn(console, "error").mockImplementation(() => {});
        api.post.mockRejectedValueOnce({
            response: {
                status: 400,
                data: { detail: "Nieprawidłowe dane logowania." }
            }
        });

        render(<App />);

        fireEvent.change(await screen.findByLabelText("Nazwa użytkownika"), {
            target: { value: "jan" }
        });
        fireEvent.change(screen.getByLabelText("Hasło"), {
            target: { value: "zle-haslo" }
        });
        fireEvent.click(screen.getByRole("button", { name: "Zaloguj się" }));

        expect(await screen.findByRole("alert")).toHaveTextContent(
            "Nieprawidłowa nazwa użytkownika lub hasło."
        );
    });
});
