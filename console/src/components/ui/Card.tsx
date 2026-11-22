import type { HTMLAttributes, ReactNode } from "react";

export type CardProps = HTMLAttributes<HTMLElement> & {
    title?: string;
    children: ReactNode;
};

export function Card({ title, children, className, ...props }: CardProps) {
    return (
        <article
            {...props}
            className={["ui-card", className ?? ""].filter(Boolean).join(" ")}
        >
            {title ? <h2 className="ui-card-title">{title}</h2> : null}
            {children}
        </article>
    );
}
