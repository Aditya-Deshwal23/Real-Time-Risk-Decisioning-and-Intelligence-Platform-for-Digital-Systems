import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { App } from "../app/App";
import { ThemeProvider } from "../theme/ThemeProvider";

describe("App", () => {
    it("renders the product name and skeleton notice", () => {
        render(
            <ThemeProvider>
                <App />
            </ThemeProvider>,
        );

        expect(screen.getByRole("heading", { name: "VERDICT" })).toBeTruthy();
        expect(screen.getByText("console skeleton")).toBeTruthy();
    });
});
