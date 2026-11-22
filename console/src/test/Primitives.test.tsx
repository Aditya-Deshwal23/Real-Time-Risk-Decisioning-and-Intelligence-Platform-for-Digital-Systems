import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import {
    Button,
    Checkbox,
    CodeBlock,
    CopyButton,
    Dialog,
    FormField,
    InlineAlert,
    StatusBadge,
    Switch,
    Table,
    Tabs,
    TextField,
    Tooltip,
} from "../components/ui";

afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
});

describe("Primitives", () => {
    it("renders Button by role and name and supports keyboard activation", async () => {
        const onClick = vi.fn();
        const user = userEvent.setup();
        render(<Button onClick={onClick}>Send decision</Button>);
        const button = screen.getByRole("button", { name: "Send decision" });
        await user.tab();
        expect(button).toBe(document.activeElement);
        await user.keyboard("{Enter}");
        expect(onClick).toHaveBeenCalledOnce();
    });

    it("links form hints and errors to an input", () => {
        render(
            <FormField
                id="credential"
                label="Credential"
                hint="Paste the full credential"
                error="Credential is required"
            >
                <TextField />
            </FormField>,
        );
        const field = screen.getByLabelText("Credential");
        expect(field.getAttribute("aria-describedby")).toContain(
            "credential-hint",
        );
        expect(field.getAttribute("aria-describedby")).toContain(
            "credential-error",
        );
        expect(screen.getByRole("alert").textContent).toContain(
            "Credential is required",
        );
    });

    it("renders Checkbox and Switch with accessible names", async () => {
        const user = userEvent.setup();
        render(
            <div>
                <Checkbox label="Store securely" />
                <Switch label="Enable shortcuts" />
            </div>,
        );
        const checkbox = screen.getByRole("checkbox", {
            name: "Store securely",
        });
        const switchControl = screen.getByRole("switch", {
            name: "Enable shortcuts",
        });
        await user.click(checkbox);
        await user.click(switchControl);
        expect(checkbox.getAttribute("data-state")).toBe("checked");
        expect(switchControl.getAttribute("data-state")).toBe("checked");
    });

    it("uses Radix Tabs with arrow-key operation", async () => {
        const user = userEvent.setup();
        render(
            <Tabs
                defaultValue="summary"
                items={[
                    {
                        value: "summary",
                        label: "Summary",
                        content: "Summary content",
                    },
                    {
                        value: "evidence",
                        label: "Evidence",
                        content: "Evidence content",
                    },
                ]}
            />,
        );
        const summary = screen.getByRole("tab", { name: "Summary" });
        summary.focus();
        await user.keyboard("{ArrowRight}");
        expect(
            screen
                .getByRole("tab", { name: "Evidence" })
                .getAttribute("data-state"),
        ).toBe("active");
    });

    it("Dialog closes with Escape and restores focus", async () => {
        const user = userEvent.setup();
        function DialogHarness() {
            const [open, setOpen] = useState(false);
            return (
                <Dialog
                    open={open}
                    onOpenChange={setOpen}
                    title="Revoke credential"
                    description="This cannot be undone."
                    trigger={<button type="button">Open</button>}
                >
                    Dialog body
                </Dialog>
            );
        }
        render(<DialogHarness />);
        const trigger = screen.getByRole("button", { name: "Open" });
        await user.click(trigger);
        expect(
            screen.getByRole("dialog", { name: "Revoke credential" }),
        ).toBeTruthy();
        await user.keyboard("{Escape}");
        expect(screen.queryByRole("dialog")).toBeNull();
        expect(trigger).toBe(document.activeElement);
    });

    it("Tooltip opens on focus and dismisses with Escape", async () => {
        const user = userEvent.setup();
        render(
            <Tooltip label="Environment details">
                <button type="button">Details</button>
            </Tooltip>,
        );
        const button = screen.getByRole("button", { name: "Details" });
        await user.tab();
        expect(button).toBe(document.activeElement);
        await user.keyboard("{Escape}");
        expect(screen.queryByText("Environment details")).toBeNull();
    });

    it("StatusBadge carries text and never relies on color alone", () => {
        render(<StatusBadge status="decline" label="Decline" />);
        expect(screen.getByText("Decline")).toBeTruthy();
        expect(document.querySelector(".ui-status-decline")).not.toBeNull();
    });

    it("InlineAlert presents status or error semantics", () => {
        render(
            <div>
                <InlineAlert kind="error" title="Save failed" />
                <InlineAlert kind="success" title="Saved" />
            </div>,
        );
        expect(screen.getByRole("alert").textContent).toContain("Save failed");
        expect(screen.getByRole("status").textContent).toContain("Saved");
    });

    it("Table and CodeBlock keep keyboard-focusable text regions", async () => {
        const user = userEvent.setup();
        render(
            <div>
                <Table caption="Decision list">
                    <thead>
                        <tr>
                            <th scope="col">Decision</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>APPROVE</td>
                        </tr>
                    </tbody>
                </Table>
                <CodeBlock code={"<danger>text</danger>"} label="Response">
                    {"<danger>text</danger>"}
                </CodeBlock>
            </div>,
        );
        await user.tab();
        expect(
            screen.getByRole("region", { name: "Decision list table" }),
        ).toBeTruthy();
        expect(screen.getByLabelText("Response text").textContent).toBe(
            "<danger>text</danger>",
        );
    });

    it("CopyButton reports clipboard success", async () => {
        const user = userEvent.setup();
        const onSuccess = vi.fn();
        const writeText = vi.fn().mockResolvedValue(undefined);
        Object.defineProperty(navigator, "clipboard", {
            configurable: true,
            value: { writeText },
        });
        render(<CopyButton value="secret fixture" onSuccess={onSuccess} />);
        await user.click(screen.getByRole("button", { name: "Copy" }));
        expect(writeText).toHaveBeenCalledWith("secret fixture");
        expect(onSuccess).toHaveBeenCalledOnce();
        expect(
            screen.getByRole("button", { name: "Copy completed" }),
        ).toBeTruthy();
    });

    it("CopyButton reports clipboard failure", async () => {
        const user = userEvent.setup();
        const onError = vi.fn();
        Object.defineProperty(navigator, "clipboard", {
            configurable: true,
            value: {
                writeText: vi.fn().mockRejectedValue(new Error("denied")),
            },
        });
        render(<CopyButton value="fixture" onError={onError} />);
        await user.click(screen.getByRole("button", { name: "Copy" }));
        expect(onError).toHaveBeenCalledOnce();
    });
});
