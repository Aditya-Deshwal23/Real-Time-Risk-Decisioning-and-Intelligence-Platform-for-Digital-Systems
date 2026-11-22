import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import type { ReactNode } from "react";

export type TooltipProps = {
    label: string;
    children: ReactNode;
};

export function Tooltip({ label, children }: TooltipProps) {
    return (
        <TooltipPrimitive.Provider delayDuration={400}>
            <TooltipPrimitive.Root>
                <TooltipPrimitive.Trigger asChild>
                    {children}
                </TooltipPrimitive.Trigger>
                <TooltipPrimitive.Portal>
                    <TooltipPrimitive.Content
                        className="ui-tooltip"
                        sideOffset={4}
                    >
                        {label}
                        <TooltipPrimitive.Arrow className="ui-tooltip-arrow" />
                    </TooltipPrimitive.Content>
                </TooltipPrimitive.Portal>
            </TooltipPrimitive.Root>
        </TooltipPrimitive.Provider>
    );
}
