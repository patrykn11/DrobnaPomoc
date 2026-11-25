import { Icon } from "../../../shared/components/Icons";
import "./OrderCTA.css";

export function ContractorOnboardingCTA({ onAction }) {
    return (
        <section className="order-cta">
            <div className="order-cta__body">
                <h2 className="order-cta__title">
                    Chcesz realizować zlecenia w swojej okolicy?
                </h2>
                <p className="order-cta__description">
                    Uzupełnij swój profil wykonawcy (kategorie usług, obszar działania i zdjęcie)
                    oraz przejdź krótką rozmowę weryfikacyjną z konsultantem, aby móc przeglądać
                    dostępne zlecenia i składać oferty cenowe.
                </p>
            </div>

            <div className="order-cta__actions">
                <button
                    type="button"
                    className="order-cta__btn order-cta__btn--primary"
                    onClick={onAction}
                >
                    <Icon name="user" size={20} />
                    <span>Uzupełnij profil wykonawcy</span>
                </button>

                <button
                    type="button"
                    className="order-cta__btn order-cta__btn--phone"
                    onClick={() => {}}
                >
                    <Icon name="phone" size={20} />
                    <span>Zadzwoń do konsultanta</span>
                </button>
            </div>
        </section>
    );
}
