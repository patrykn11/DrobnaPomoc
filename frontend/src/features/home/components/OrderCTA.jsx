import { Icon } from "../../../shared/components/Icons";
import "./OrderCTA.css";

export function OrderCTA({ variant = "client", onAction }) {
    const isRemote = variant === "remote_client";

    return (
        <section className="order-cta">
            <div className="order-cta__body">
                <h2 className="order-cta__title">
                    {isRemote
                        ? "Zorganizuj pomoc dla bliskiej osoby"
                        : "Potrzebujesz pomocy w domowych pracach?"}
                </h2>
                <p className="order-cta__description">
                    {isRemote
                        ? "Wprowadź dane osoby, która potrzebuje pomocy, i przekaż jej jednorazowy kod wizyty."
                        : "Opisz zadanie i wybierz termin. Zweryfikowani wykonawcy z Twojej okolicy prześlą swoje oferty."}
                </p>
            </div>

            <div className="order-cta__actions">
                <button
                    type="button"
                    className="order-cta__btn order-cta__btn--primary"
                    onClick={onAction}
                >
                    <Icon name="plus" size={20} />
                    <span>
                        {isRemote
                            ? "Złóż zlecenie dla bliskiego"
                            : "Złóż nowe zlecenie"}
                    </span>
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
