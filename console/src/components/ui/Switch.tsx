import * as SwitchPrimitive from "@radix-ui/react-switch";

export type SwitchProps = {
    checked?: boolean;
    defaultChecked?: boolean;
    onCheckedChange?: (checked: boolean) => void;
    disabled?: boolean;
    name?: string;
    label: string;
};

export function Switch({
    checked,
    defaultChecked,
    onCheckedChange,
    disabled,
    name,
    label,
}: SwitchProps) {
    return (
        <label className="ui-choice">
            <SwitchPrimitive.Root
                className="ui-switch"
                checked={checked}
                defaultChecked={defaultChecked}
                onCheckedChange={onCheckedChange}
                disabled={disabled}
                name={name}
            >
                <SwitchPrimitive.Thumb className="ui-switch-thumb" />
            </SwitchPrimitive.Root>
            <span>{label}</span>
        </label>
    );
}
