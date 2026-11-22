import { act, cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ThemeProvider, THEME_STORAGE_KEY } from "../theme/ThemeProvider";
import { useTheme } from "../theme/useTheme";

function ThemeProbe() {
    const { choice, theme, setChoice } = useTheme();
    return (
        <div>
            <output data-testid="choice">{choice}</output>
            <output data-testid="theme">{theme}</output>
            <button onClick={() => setChoice("light")}>Light</button>
        </div>
    );
}

let lightQueryMatches = false;
let changeListener: ((event: MediaQueryListEvent) => void) | null = null;

function installMatchMedia(initialMatches: boolean) {
    lightQueryMatches = initialMatches;
    changeListener = null;
    vi.stubGlobal(
        "matchMedia",
        vi.fn(() => ({
            matches: lightQueryMatches,
            media: "(prefers-color-scheme: light)",
            onchange: null,
            addEventListener: (
                _type: string,
                listener: (event: MediaQueryListEvent) => void,
            ) => {
                changeListener = listener;
            },
            removeEventListener: vi.fn(),
            addListener: vi.fn(),
            removeListener: vi.fn(),
            dispatchEvent: vi.fn(),
        })),
    );
}

describe("ThemeProvider", () => {
    beforeEach(() => {
        localStorage.clear();
        document.documentElement.removeAttribute("data-theme");
        installMatchMedia(false);
    });

    afterEach(() => {
        cleanup();
        vi.restoreAllMocks();
        vi.unstubAllGlobals();
    });

    it("uses dark when no choice is stored", () => {
        render(
            <ThemeProvider>
                <ThemeProbe />
            </ThemeProvider>,
        );
        expect(screen.getByTestId("choice").textContent).toBe("dark");
        expect(screen.getByTestId("theme").textContent).toBe("dark");
    });

    it("loads a stored choice", () => {
        localStorage.setItem(THEME_STORAGE_KEY, "light");
        render(
            <ThemeProvider>
                <ThemeProbe />
            </ThemeProvider>,
        );
        expect(screen.getByTestId("choice").textContent).toBe("light");
        expect(screen.getByTestId("theme").textContent).toBe("light");
    });

    it("falls back to dark for an unknown stored value", () => {
        localStorage.setItem(THEME_STORAGE_KEY, "unknown");
        render(
            <ThemeProvider>
                <ThemeProbe />
            </ThemeProvider>,
        );
        expect(screen.getByTestId("choice").textContent).toBe("dark");
    });

    it("uses system preference for the system choice", () => {
        installMatchMedia(true);
        localStorage.setItem(THEME_STORAGE_KEY, "system");
        render(
            <ThemeProvider>
                <ThemeProbe />
            </ThemeProvider>,
        );
        expect(screen.getByTestId("theme").textContent).toBe("light");
    });

    it("falls back to dark when storage access throws", () => {
        vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
            throw new DOMException("blocked");
        });
        render(
            <ThemeProvider>
                <ThemeProbe />
            </ThemeProvider>,
        );
        expect(screen.getByTestId("choice").textContent).toBe("dark");
    });

    it("updates while system preference changes and the page is open", () => {
        localStorage.setItem(THEME_STORAGE_KEY, "system");
        installMatchMedia(false);
        render(
            <ThemeProvider>
                <ThemeProbe />
            </ThemeProvider>,
        );
        act(() => {
            lightQueryMatches = true;
            changeListener?.({
                matches: true,
                media: "(prefers-color-scheme: light)",
            } as MediaQueryListEvent);
        });
        expect(screen.getByTestId("theme").textContent).toBe("light");
    });
});
