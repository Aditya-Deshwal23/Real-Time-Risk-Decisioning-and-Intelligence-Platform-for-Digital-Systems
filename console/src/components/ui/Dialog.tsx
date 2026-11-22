import * as DialogPrimitive from "@radix-ui/react-dialog";
import type { ReactNode } from "react";
import { IconButton } from "./IconButton";
import { X } from "lucide-react";

export type DialogProps = {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    title: string;
    description?: string;
    children: ReactNode;
    footer?: ReactNode;
    width?: "400" | "560" | "720";
};

export function Dialog({
    open,
    onOpenChange,
    title,
    description,
    children,
    footer,
    width = "560",
}: DialogProps) {
    return (
        <DialogPrimitive.Root open={open} onOpenChange={onOpenChange}>
            <DialogPrimitive.Portal>
                <DialogPrimitive.Overlay className="ui-dialog-overlay" />
                <DialogPrimitive.Content
                    className={`ui-dialog ui-dialog-${width}`}
                    aria-describedby={
                        description ? "verdict-dialog-description" : undefined
                    }
                >
                    <div className="ui-dialog-header">
                        <DialogPrimitive.Title className="ui-dialog-title">
                            {title}
                        </DialogPrimitive.Title>
                        <DialogPrimitive.Close asChild>
                            <IconButton
                                icon={X}
                                label="Close dialog"
                                size="small"
                            />
                        </DialogPrimitive.Close>
                    </div>
                    {description ? (
                        <DialogPrimitive.Description
                            id="verdict-dialog-description"
                            className="ui-dialog-description"
                        >
                            {description}
                        </DialogPrimitive.Description>
                    ) : null}
                    <div className="ui-dialog-body">{children}</div>
                    {footer ? (
                        <div className="ui-dialog-footer">{footer}</div>
                    ) : null}
                </DialogPrimitive.Content>
            </DialogPrimitive.Portal>
        </DialogPrimitive.Root>
    );
}
