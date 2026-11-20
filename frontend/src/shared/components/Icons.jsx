export function Icon({ name, size = 22 }) {
    const paths = {
        home: (
            <>
                <path d="M3 10.8 12 3l9 7.8" />
                <path d="M5.5 9.5V21h13V9.5" />
                <path d="M9 21v-6h6v6" />
            </>
        ),
        list: (
            <>
                <rect x="5" y="3" width="14" height="18" rx="2" />
                <path d="M9 8h6M9 12h6M9 16h4" />
            </>
        ),
        plus: (
            <>
                <circle cx="12" cy="12" r="9" />
                <path d="M12 8v8M8 12h8" />
            </>
        ),
        phone: (
            <path d="M7.2 3.5 4.8 5.9c-.7.7-.5 2.1.1 3.5 1.7 4.1 5.6 8 9.7 9.7 1.4.6 2.8.8 3.5.1l2.4-2.4-4.1-3-2.2 2.2c-2.6-1.2-5-3.6-6.2-6.2l2.2-2.2-3-4.1Z" />
        ),
        menu: <path d="M4 7h16M4 12h16M4 17h16" />,
        close: <path d="m6 6 12 12M18 6 6 18" />
    };

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
        >
            {paths[name]}
        </svg>
    );
}
