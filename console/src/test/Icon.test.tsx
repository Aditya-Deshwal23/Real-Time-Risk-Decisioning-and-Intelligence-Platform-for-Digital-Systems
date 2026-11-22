import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Icon } from "../components/ui/Icon";
import { Info } from "../components/ui/icons";

describe("Icon", () => {
    it("hides decorative icons from assistive technology", () => {
        const { container } = render(<Icon icon={Info} decorative />);
        const svg = container.querySelector("svg");
        expect(svg?.getAttribute("aria-hidden")).toBe("true");
    });

    it("requires and exposes an accessible name for meaningful icons", () => {
        render(<Icon icon={Info} label="Environment information" />);
        expect(
            screen.getByRole("img", { name: "Environment information" }),
        ).toBeTruthy();
    });

    it("rejects unnamed meaningful icons at type-check time", () => {
        // @ts-expect-error meaningful icons require an accessible label
        const unnamed = <Icon icon={Info} />;
        expect(unnamed).toBeTruthy();
    });
});
