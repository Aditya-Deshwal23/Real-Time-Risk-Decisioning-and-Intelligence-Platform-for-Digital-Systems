import { cloneElement, isValidElement, type ReactNode } from "react";
import { Icon } from "./Icon";
import { TriangleAlert } from "./icons";

export type FormFieldProps = {
    id: string;
    label: string;
    optional?: boolean;
    hint?: string;
    error?: string;
    children: ReactNode;
};

export function FormField({
    id,
    label,
    optional = false,
    hint,
    error,
    children,
}: FormFieldProps) {
    const hintId = hint ? `${id}-hint` : undefined;
    const errorId = error ? `${id}-error` : undefined;
    const describedBy =
        [hintId, errorId].filter(Boolean).join(" ") || undefined;
    const field = isValidElement<{ id?: string; "aria-describedby"?: string }>(
        children,
    )
        ? cloneElement(
              children,
              describedBy
                  ? {
                        id,
                        "aria-describedby": describedBy,
                    }
                  : { id },
          )
        : children;

    return (
        <div className="ui-form-field">
            <label className="ui-label" htmlFor={id}>
                {label}
                {optional ? (
                    <span className="ui-label-optional"> (optional)</span>
                ) : null}
            </label>
            {field}
            {hint ? (
                <p className="ui-field-hint" id={hintId}>
                    {hint}
                </p>
            ) : null}
            {error ? (
                <p className="ui-field-error" id={errorId} role="alert">
                    <Icon icon={TriangleAlert} decorative />
                    {error}
                </p>
            ) : null}
        </div>
    );
}
