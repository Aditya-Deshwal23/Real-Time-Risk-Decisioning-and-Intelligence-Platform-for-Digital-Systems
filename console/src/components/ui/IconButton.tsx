import type { ButtonHTMLAttributes } from "react";
import type { LucideIcon } from "lucide-react";

export type IconButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
    icon: LucideIcon;
    label: string;
    size?: "small" | "medium" | "large";
};

export function IconButton({
    icon: IconGlyph,
    label,
    size = "medium",
    className,
    ...props
}: IconButtonProps) {
    return (
        <button
            {...props}
            type={props.type ?? "button"}
            className={[
                "ui-icon-button",
                `ui-icon-button-${size}`,
                className ?? "",
            ]
                .filter(Boolean)
                .join(" ")}
            aria-label={label}
            title={label}
        >
            <IconGlyph
                aria-hidden="true"
                focusable="false"
                size="var(--icon-size-control)"
                strokeWidth="var(--icon-stroke-width)"
            />
        </button>
    );
}
