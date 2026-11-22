import type { InputHTMLAttributes } from "react";

export type TextFieldProps = Omit<
    InputHTMLAttributes<HTMLInputElement>,
    "size"
> & {
    invalid?: boolean;
};

export function TextField({
    invalid = false,
    className,
    "aria-describedby": ariaDescribedBy,
    ...props
}: TextFieldProps) {
    return (
        <input
            {...props}
            className={[
                "ui-text-field",
                invalid ? "ui-text-field-invalid" : "",
                className ?? "",
            ]
                .filter(Boolean)
                .join(" ")}
            aria-invalid={invalid || undefined}
            aria-describedby={ariaDescribedBy}
        />
    );
}
