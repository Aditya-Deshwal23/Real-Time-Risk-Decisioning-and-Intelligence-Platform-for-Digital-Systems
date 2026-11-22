import type { LucideIcon } from "lucide-react";

type IconSize = 14 | 16 | 20 | 24;

type IconProps = {
    icon: LucideIcon;
    size?: IconSize;
} & (
    { decorative: true; label?: never } | { decorative?: false; label: string }
);

export function Icon({ icon: IconGlyph, size = 16, ...props }: IconProps) {
    const sizeToken =
        size === 14
            ? "var(--icon-size-badge)"
            : size === 20
              ? "var(--icon-size-navigation)"
              : size === 24
                ? "var(--icon-size-empty-state)"
                : "var(--icon-size-control)";

    if (props.decorative) {
        return (
            <IconGlyph
                aria-hidden="true"
                focusable="false"
                size={sizeToken}
                strokeWidth="var(--icon-stroke-width)"
                color="currentColor"
            />
        );
    }

    return (
        <IconGlyph
            role="img"
            aria-label={props.label}
            focusable="false"
            size={sizeToken}
            strokeWidth="var(--icon-stroke-width)"
            color="currentColor"
        />
    );
}
