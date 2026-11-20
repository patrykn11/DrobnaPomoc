import { Icon } from "./Icons";
export function Brand() {
    return (
        <div className="brand" aria-label="DrobnaPomoc">
            <span className="brand__mark">
                <Icon name="home" size={25} />
            </span>
            <span className="brand__name">
                Drobna<span>Pomoc</span>
            </span>
        </div>
    );
}
