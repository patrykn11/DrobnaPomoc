import { useState } from "react";
import { useAuth } from "../features/auth/useAuth";
import { Brand } from "../shared/components/Brand";
import { Icon } from "../shared/components/Icons";
import "./AppLayout.css";

const menuItems = [
    { icon: "home", label: "Strona główna", active: true },
    { icon: "list", label: "Moje zlecenia" },
    { icon: "plus", label: "Złóż zlecenie" }
];

function initials(user) {
    const firstLetter = user?.first_name?.[0] || "";
    const lastLetter = user?.last_name?.[0] || "";
    const nameInitials = `${firstLetter}${lastLetter}`.toUpperCase();

    return nameInitials || user?.username?.slice(0, 2).toUpperCase() || "U";
}

function displayName(user) {
    const fullName = [user?.first_name, user?.last_name].filter(Boolean).join(" ");

    return fullName || user?.username;
}

export function AppLayout() {
    const { user, logout } = useAuth();
    const [sidebarOpen, setSidebarOpen] = useState(false);

    return (
        <div className="app-shell">
            <header className="topbar">
                <button
                    className="mobile-menu"
                    type="button"
                    onClick={() => setSidebarOpen(true)}
                    aria-label="Otwórz menu"
                >
                    <Icon name="menu" />
                </button>

                <Brand />

                <div className="topbar__actions">
                    <div className="helpline">
                        <Icon name="phone" />
                        <span>
                            Konsultant: <strong>[numer infolinii]</strong>
                        </span>
                    </div>

                    <div className="user-summary">
                        <span className="avatar">{initials(user)}</span>
                        <strong>{displayName(user)}</strong>
                    </div>

                    <button className="logout-button" type="button" onClick={logout}>
                        Wyloguj
                    </button>
                </div>
            </header>

            <div className="app-shell__body">
                {sidebarOpen && (
                    <button
                        className="sidebar-backdrop"
                        aria-label="Zamknij menu"
                        onClick={() => setSidebarOpen(false)}
                    />
                )}

                <aside className={`sidebar ${sidebarOpen ? "sidebar--open" : ""}`}>
                    <div className="sidebar__mobile-heading">
                        <Brand />
                        <button
                            type="button"
                            onClick={() => setSidebarOpen(false)}
                            aria-label="Zamknij menu"
                        >
                            <Icon name="close" />
                        </button>
                    </div>

                    <nav aria-label="Menu główne">
                        {menuItems.map((item) => (
                            <button
                                key={item.label}
                                type="button"
                                className={`nav-item ${item.active ? "nav-item--active" : ""}`}
                                aria-current={item.active ? "page" : undefined}
                            >
                                <Icon name={item.icon} />
                                <span>{item.label}</span>
                            </button>
                        ))}
                    </nav>

                    <button className="sidebar__logout" type="button" onClick={logout}>
                        Wyloguj
                    </button>
                </aside>

                <main className="page-canvas" aria-label="Strona główna" />
            </div>
        </div>
    );
}
