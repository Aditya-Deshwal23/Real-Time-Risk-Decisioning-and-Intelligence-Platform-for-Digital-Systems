import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { App } from "../app/App";

describe("App", () => {
    it("renders the product name and skeleton notice", () => {
        render(<App />);

        expect(screen.getByRole("heading", { name: "VERDICT" })).toBeTruthy();
        expect(screen.getByText("console skeleton")).toBeTruthy();
    });
});
