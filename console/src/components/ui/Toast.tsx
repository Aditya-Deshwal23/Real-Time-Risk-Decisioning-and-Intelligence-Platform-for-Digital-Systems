import * as ToastPrimitive from "@radix-ui/react-toast";
import type { ReactNode } from "react";
import { Icon } from "./Icon";
import { CircleCheck, CircleX, Info } from "./icons";

export type ToastProps = {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    kind: "success" | "info" | "error";
    title: string;
    description?: string;
    action?: ReactNode;
};

export function Toast({
    open,
    onOpenChange,
    kind,
    title,
    description,
    action,
}: ToastProps) {
    const icon =
        kind === "success" ? CircleCheck : kind === "error" ? CircleX : Info;
    return (
        <ToastPrimitive.Provider swipeDirection="right">
            <ToastPrimitive.Root
                className={`ui-toast ui-toast-${kind}`}
                open={open}
                onOpenChange={onOpenChange}
                duration={kind === "error" ? 0 : kind === "info" ? 8000 : 5000}
                role={kind === "error" ? "alert" : "status"}
            >
                <Icon icon={icon} decorative />
                <div className="ui-toast-copy">
                    <ToastPrimitive.Title className="ui-toast-title">
                        {title}
                    </ToastPrimitive.Title>
                    {description ? (
                        <ToastPrimitive.Description className="ui-toast-description">
                            {description}
                        </ToastPrimitive.Description>
                    ) : null}
                </div>
                {action ? (
                    <ToastPrimitive.Action asChild altText="Open action">
                        {action}
                    </ToastPrimitive.Action>
                ) : null}
                <ToastPrimitive.Close
                    className="ui-toast-close"
                    aria-label="Dismiss notification"
                >
                    Close
                </ToastPrimitive.Close>
            </ToastPrimitive.Root>
            <ToastPrimitive.Viewport className="ui-toast-viewport" />
        </ToastPrimitive.Provider>
    );
}
