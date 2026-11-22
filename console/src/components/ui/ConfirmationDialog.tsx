import * as AlertDialogPrimitive from "@radix-ui/react-alert-dialog";
import type { ReactNode } from "react";
import { Button } from "./Button";

export type ConfirmationDialogProps = {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    title: string;
    description: string;
    confirmLabel: string;
    cancelLabel?: string;
    onConfirm: () => void;
    confirmDisabled?: boolean;
    children?: ReactNode;
};

export function ConfirmationDialog({
    open,
    onOpenChange,
    title,
    description,
    confirmLabel,
    cancelLabel = "Cancel",
    onConfirm,
    confirmDisabled,
    children,
}: ConfirmationDialogProps) {
    return (
        <AlertDialogPrimitive.Root open={open} onOpenChange={onOpenChange}>
            <AlertDialogPrimitive.Portal>
                <AlertDialogPrimitive.Overlay className="ui-dialog-overlay" />
                <AlertDialogPrimitive.Content className="ui-dialog ui-dialog-400">
                    <AlertDialogPrimitive.Title className="ui-dialog-title">
                        {title}
                    </AlertDialogPrimitive.Title>
                    <AlertDialogPrimitive.Description className="ui-dialog-description">
                        {description}
                    </AlertDialogPrimitive.Description>
                    {children}
                    <div className="ui-dialog-footer">
                        <AlertDialogPrimitive.Cancel asChild>
                            <Button variant="secondary">{cancelLabel}</Button>
                        </AlertDialogPrimitive.Cancel>
                        <AlertDialogPrimitive.Action asChild>
                            <Button
                                variant="danger"
                                disabled={confirmDisabled}
                                onClick={onConfirm}
                            >
                                {confirmLabel}
                            </Button>
                        </AlertDialogPrimitive.Action>
                    </div>
                </AlertDialogPrimitive.Content>
            </AlertDialogPrimitive.Portal>
        </AlertDialogPrimitive.Root>
    );
}
