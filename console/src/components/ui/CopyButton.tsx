import { useState } from "react";
import { Button } from "./Button";

export type CopyButtonProps = {
    value: string;
    label?: string;
    onSuccess?: () => void;
    onError?: (error: unknown) => void;
};

export function CopyButton({
    value,
    label = "Copy",
    onSuccess,
    onError,
}: CopyButtonProps) {
    const [copied, setCopied] = useState(false);

    async function copy() {
        try {
            await navigator.clipboard.writeText(value);
            setCopied(true);
            onSuccess?.();
        } catch (error) {
            setCopied(false);
            onError?.(error);
        }
    }

    return (
        <Button
            variant="tertiary"
            size="small"
            type="button"
            onClick={() => {
                void copy();
            }}
            aria-label={copied ? `${label} completed` : label}
        >
            {copied ? "Copied" : label}
        </Button>
    );
}
