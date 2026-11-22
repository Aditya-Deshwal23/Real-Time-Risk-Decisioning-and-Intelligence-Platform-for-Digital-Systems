import type { ReactNode } from "react";
import { CopyButton } from "./CopyButton";

export type CodeBlockProps = {
    children: ReactNode;
    code: string;
    label?: string;
};

export function CodeBlock({ children, code, label = "Code" }: CodeBlockProps) {
    return (
        <div className="ui-code-block">
            <div className="ui-code-block-toolbar">
                <span>{label}</span>
                <CopyButton value={code} label={`Copy ${label}`} />
            </div>
            <pre
                className="ui-code-block-scroll"
                tabIndex={0}
                aria-label={`${label} text`}
            >
                <code>{children}</code>
            </pre>
        </div>
    );
}
