import type { ReactNode } from "react";
import { Icon } from "./Icon";
import { CircleCheck, CircleX, Info, TriangleAlert } from "./icons";

export type InlineAlertProps = {
    kind: "success" | "info" | "warning" | "error";
    title: string;
    children?: ReactNode;
};

export function InlineAlert({ kind, title, children }: InlineAlertProps) {
    const icon =
        kind === "success"
            ? CircleCheck
            : kind === "error"
              ? CircleX
              : kind === "warning"
                ? TriangleAlert
                : Info;
    return (
        <div
            className={`ui-inline-alert ui-inline-alert-${kind}`}
            role={kind === "error" ? "alert" : "status"}
        >
            <Icon icon={icon} decorative />
            <div>
                <strong>{title}</strong>
                {children}
            </div>
        </div>
    );
}
