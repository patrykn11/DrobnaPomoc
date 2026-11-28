import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { HomePage } from "./HomePage";

describe("HomePage", () => {
    afterEach(() => {
        cleanup();
    });

    it("renders centered header and role switcher group", () => {
        render(<HomePage />);

        expect(screen.getByRole("heading", { name: "Witaj w DrobnaPomoc" })).toBeInTheDocument();
        expect(
            screen.getByText("Szybka i bezpieczna pomoc w codziennych sprawach domowych.")
        ).toBeInTheDocument();
        expect(screen.getByRole("group", { name: "Wybierz rolę użytkownika" })).toBeInTheDocument();
    });

    it("renders client view by default", () => {
        render(<HomePage />);

        const clientButton = screen.getByRole("button", {
            name: /Zleceniodawca.*Zamawiam dla siebie/i
        });
        expect(clientButton).toHaveAttribute("aria-pressed", "true");

        expect(
            screen.getByRole("heading", { name: "Potrzebujesz pomocy w domowych pracach?" })
        ).toBeInTheDocument();
        expect(screen.getByRole("button", { name: "Złóż nowe zlecenie" })).toBeInTheDocument();
    });

    it("switches to remote client view on button click", () => {
        render(<HomePage />);

        const clientButton = screen.getByRole("button", {
            name: /Zleceniodawca.*Zamawiam dla siebie/i
        });
        const remoteClientButton = screen.getByRole("button", {
            name: /Zleceniodawca zdalny/i
        });

        fireEvent.click(remoteClientButton);

        expect(remoteClientButton).toHaveAttribute("aria-pressed", "true");
        expect(clientButton).toHaveAttribute("aria-pressed", "false");

        expect(
            screen.getByRole("heading", { name: "Zorganizuj pomoc dla bliskiej osoby" })
        ).toBeInTheDocument();
        expect(screen.getByRole("button", { name: "Złóż zlecenie dla bliskiego" })).toBeInTheDocument();
    });

    it("switches to contractor view on button click", () => {
        render(<HomePage />);

        const contractorButton = screen.getByRole("button", { name: /Wykonawca/i });
        fireEvent.click(contractorButton);

        expect(contractorButton).toHaveAttribute("aria-pressed", "true");
        expect(
            screen.getByRole("heading", { name: "Chcesz realizować zlecenia w swojej okolicy?" })
        ).toBeInTheDocument();
        expect(
            screen.getByRole("button", { name: "Uzupełnij profil wykonawcy" })
        ).toBeInTheDocument();
    });

    it("renders consultant phone call button", () => {
        render(<HomePage />);

        expect(screen.getByRole("button", { name: "Zadzwoń do konsultanta" })).toBeInTheDocument();
    });
});
