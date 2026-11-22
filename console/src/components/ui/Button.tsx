import type { ButtonHTMLAttributes } from "react";

export type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: "primary" | "secondary" | "tertiary" | "danger";
    size?: "small" | "medium" | "large";
    loading?: boolean;
    disabledReason?: string;
};

export function Button({
    variant = "secondary",
    size = "medium",
    loading = false,
    disabledReason,
    disabled,
    children,
    className,
    ...props
}: ButtonProps) {
    const unavailable = disabled || loading;
    const classes = [
        "ui-button",
        `ui-button-${variant}`,
        `ui-button-${size}`,
        loading ? "ui-button-loading" : "",
        className ?? "",
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <span className="ui-button-wrap">
            <button
                {...props}
                className={classes}
                aria-busy={loading || undefined}
                aria-disabled={unavailable || undefined}
                disabled={unavailable}
            >
                {loading ? (
                    <span className="ui-spinner" aria-hidden="true" />
                ) : null}
                <span>{children}</span>
            </button>
            {unavailable && disabledReason ? (
                <span className="ui-disabled-reason">{disabledReason}</span>
            ) : null}
        </span>
    );
}
