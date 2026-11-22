import {
    createContext,
    useCallback,
    useEffect,
    useMemo,
    useState,
    type ReactNode,
} from "react";

export type ThemeChoice = "light" | "dark" | "system";
export type ResolvedTheme = "light" | "dark";

export const THEME_STORAGE_KEY = "verdict-theme-preference";

interface ThemeContextValue {
    choice: ThemeChoice;
    theme: ResolvedTheme;
    setChoice: (choice: ThemeChoice) => void;
}

export const ThemeContext = createContext<ThemeContextValue | null>(null);

function readChoice(): ThemeChoice {
    try {
        const stored = window.localStorage.getItem(THEME_STORAGE_KEY);
        if (stored === "light" || stored === "dark" || stored === "system") {
            return stored;
        }
    } catch {
        // Storage may be blocked; the documented fallback is dark.
    }
    return "dark";
}

function resolveTheme(choice: ThemeChoice): ResolvedTheme {
    if (choice === "system") {
        return window.matchMedia?.("(prefers-color-scheme: light)").matches
            ? "light"
            : "dark";
    }
    return choice;
}

export function ThemeProvider({ children }: { children: ReactNode }) {
    const [choice, setChoiceState] = useState<ThemeChoice>(readChoice);
    const [systemTheme, setSystemTheme] = useState<ResolvedTheme>(() =>
        window.matchMedia?.("(prefers-color-scheme: light)").matches
            ? "light"
            : "dark",
    );

    useEffect(() => {
        const media = window.matchMedia?.("(prefers-color-scheme: light)");
        if (!media) {
            return;
        }
        const handleChange = () => {
            setSystemTheme(media.matches ? "light" : "dark");
        };
        media.addEventListener("change", handleChange);
        return () => media.removeEventListener("change", handleChange);
    }, []);

    const theme = choice === "system" ? systemTheme : resolveTheme(choice);

    useEffect(() => {
        document.documentElement.setAttribute("data-theme", theme);
        document.documentElement.style.colorScheme = theme;
    }, [theme]);

    const setChoice = useCallback((nextChoice: ThemeChoice) => {
        setChoiceState(nextChoice);
        try {
            window.localStorage.setItem(THEME_STORAGE_KEY, nextChoice);
        } catch {
            // Storage may be blocked; the in-memory choice still applies.
        }
    }, []);

    const value = useMemo(
        () => ({ choice, theme, setChoice }),
        [choice, setChoice, theme],
    );

    return (
        <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
    );
}
