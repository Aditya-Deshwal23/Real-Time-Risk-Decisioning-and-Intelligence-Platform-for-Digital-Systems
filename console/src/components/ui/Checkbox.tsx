import * as CheckboxPrimitive from "@radix-ui/react-checkbox";
import { Icon } from "./Icon";
import { CircleCheck } from "./icons";

export type CheckboxProps = {
    checked?: boolean;
    defaultChecked?: boolean;
    onCheckedChange?: (checked: boolean | "indeterminate") => void;
    disabled?: boolean;
    name?: string;
    required?: boolean;
    label: string;
};

export function Checkbox({
    checked,
    defaultChecked,
    onCheckedChange,
    disabled,
    name,
    required,
    label,
}: CheckboxProps) {
    return (
        <label className="ui-choice">
            <CheckboxPrimitive.Root
                className="ui-checkbox"
                checked={checked}
                defaultChecked={defaultChecked}
                onCheckedChange={onCheckedChange}
                disabled={disabled}
                name={name}
                required={required}
            >
                <CheckboxPrimitive.Indicator className="ui-checkbox-indicator">
                    <Icon icon={CircleCheck} decorative />
                </CheckboxPrimitive.Indicator>
            </CheckboxPrimitive.Root>
            <span>{label}</span>
        </label>
    );
}
