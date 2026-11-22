import type { ReactNode } from "react";

export type BadgeProps = {
    children: ReactNode;
    outline?: boolean;
};

export function Badge({ children, outline = false }: BadgeProps) {
    return (
        <span className={outline ? "ui-badge ui-badge-outline" : "ui-badge"}>
            {children}
        </span>
    );
}
