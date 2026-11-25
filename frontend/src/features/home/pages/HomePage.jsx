import { useState } from "react";
import { ContractorOnboardingCTA } from "../components/ContractorOnboardingCTA";
import { OrderCTA } from "../components/OrderCTA";
import "./HomePage.css";

const ROLES = [
    {
        id: "client",
        label: "Zleceniodawca",
        subtitle: "Zamawiam dla siebie"
    },
    {
        id: "remote_client",
        label: "Zleceniodawca zdalny",
        subtitle: "Zamawiam dla bliskiej osoby"
    },
    {
        id: "contractor",
        label: "Wykonawca",
        subtitle: "Chcę realizować zlecenia"
    }
];

export function HomePage() {
    const [selectedRole, setSelectedRole] = useState("client");

    return (
        <div className="home-page">
            <header className="home-hero">
                <h1 className="home-hero__title">Witaj w DrobnaPomoc</h1>
                <p className="home-hero__subtitle">
                    Szybka i bezpieczna pomoc w codziennych sprawach domowych.
                </p>

                <div
                    className="role-switcher"
                    role="tablist"
                    aria-label="Wybierz rolę użytkownika"
                >
                    {ROLES.map((role) => {
                        const isSelected = selectedRole === role.id;
                        return (
                            <button
                                key={role.id}
                                type="button"
                                role="tab"
                                aria-selected={isSelected}
                                className={`role-tab ${isSelected ? "role-tab--active" : ""}`}
                                onClick={() => setSelectedRole(role.id)}
                            >
                                <span className="role-tab__title">{role.label}</span>
                                <span className="role-tab__subtitle">{role.subtitle}</span>
                            </button>
                        );
                    })}
                </div>
            </header>

            <section className="home-content">
                {selectedRole === "client" && (
                    <div className="role-view">
                        <OrderCTA
                            variant="client"
                            onAction={() => {}}
                        />
                    </div>
                )}

                {selectedRole === "remote_client" && (
                    <div className="role-view">
                        <OrderCTA
                            variant="remote_client"
                            onAction={() => {}}
                        />
                    </div>
                )}

                {selectedRole === "contractor" && (
                    <div className="role-view">
                        <ContractorOnboardingCTA
                            onAction={() => alert("Formularz profilu wykonawcy - w przygotowaniu")}
                        />
                    </div>
                )}
            </section>
        </div>
    );
}
