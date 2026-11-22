import type { AnchorHTMLAttributes, ReactNode } from "react";

export type LinkProps = AnchorHTMLAttributes<HTMLAnchorElement> & {
    children: ReactNode;
};

export function Link({ children, className, ...props }: LinkProps) {
    return (
        <a
            {...props}
            className={["ui-link", className ?? ""].filter(Boolean).join(" ")}
            rel={props.target === "_blank" ? "noopener noreferrer" : props.rel}
        >
            {children}
        </a>
    );
}
