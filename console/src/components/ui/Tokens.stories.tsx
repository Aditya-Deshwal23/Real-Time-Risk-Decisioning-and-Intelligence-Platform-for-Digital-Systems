import type { Meta, StoryObj } from "@storybook/react-vite";
import { useEffect, useState } from "react";

const meta: Meta = {
    title: "Foundation/Tokens",
};

export default meta;

const tokenNames = [
    "--color-bg-canvas",
    "--color-bg-surface",
    "--color-bg-raised",
    "--color-bg-sunken",
    "--color-bg-hover",
    "--color-bg-selected",
    "--color-border-subtle",
    "--color-border-default",
    "--color-border-strong",
    "--color-text-primary",
    "--color-text-secondary",
    "--color-text-tertiary",
    "--color-text-disabled",
    "--color-link",
    "--color-accent",
    "--color-accent-hover",
    "--color-accent-active",
    "--color-on-accent",
    "--color-accent-subtle",
    "--color-focus-ring",
    "--color-status-approve-text",
    "--color-status-approve-bg",
    "--color-status-review-text",
    "--color-status-review-bg",
    "--color-status-decline-text",
    "--color-status-decline-bg",
    "--color-status-degraded-text",
    "--color-status-degraded-bg",
    "--color-status-info-text",
    "--color-status-info-bg",
    "--color-status-neutral-text",
    "--color-status-neutral-bg",
];

function TokenReference() {
    const [, setTheme] = useState(
        document.documentElement.getAttribute("data-theme") ?? "dark",
    );

    useEffect(() => {
        const observer = new MutationObserver(() => {
            setTheme(
                document.documentElement.getAttribute("data-theme") ?? "dark",
            );
        });
        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ["data-theme"],
        });
        return () => {
            observer.disconnect();
        };
    }, []);

    return (
        <table className="ui-table">
            <caption>Semantic token reference for the selected theme</caption>
            <thead>
                <tr>
                    <th scope="col">Token</th>
                    <th scope="col">Resolved value</th>
                    <th scope="col">Preview</th>
                </tr>
            </thead>
            <tbody>
                {tokenNames.map((name) => (
                    <tr key={name}>
                        <td>
                            <code>{name}</code>
                        </td>
                        <td>
                            {getComputedStyle(
                                document.documentElement,
                            ).getPropertyValue(name)}
                        </td>
                        <td
                            style={{ background: `var(${name})` }}
                            aria-label={`Preview ${name}`}
                        />
                    </tr>
                ))}
            </tbody>
        </table>
    );
}

export const TokenReferencePage: StoryObj = {
    render: () => <TokenReference />,
};
