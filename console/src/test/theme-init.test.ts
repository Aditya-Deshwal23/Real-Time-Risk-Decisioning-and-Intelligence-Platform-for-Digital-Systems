import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

describe("theme initialisation", () => {
    it("uses a separate same-origin script without an inline script", () => {
        const html = readFileSync(
            new URL("../../index.html", import.meta.url),
            "utf8",
        );
        expect(html).toContain('src="/theme-init.js"');
        expect(html).not.toMatch(/<script(?![^>]*src=)[^>]*>/);
    });
});
