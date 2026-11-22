import type { HTMLAttributes, ReactNode } from "react";

export type PanelProps = HTMLAttributes<HTMLElement> & {
    title?: string;
    children: ReactNode;
};

export function Panel({ title, children, className, ...props }: PanelProps) {
    return (
        <section
            {...props}
            className={["ui-panel", className ?? ""].filter(Boolean).join(" ")}
        >
            {title ? <h2 className="ui-panel-title">{title}</h2> : null}
            {children}
        </section>
    );
}
