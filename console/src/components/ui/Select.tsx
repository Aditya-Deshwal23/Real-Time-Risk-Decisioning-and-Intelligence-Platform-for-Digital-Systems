import * as SelectPrimitive from "@radix-ui/react-select";
import { ChevronRight } from "./icons";
import { Icon } from "./Icon";

export type SelectOption = {
    value: string;
    label: string;
    disabled?: boolean;
};

export type SelectProps = {
    value?: string;
    defaultValue?: string;
    onValueChange?: (value: string) => void;
    options: SelectOption[];
    placeholder?: string;
    name?: string;
    disabled?: boolean;
    invalid?: boolean;
    "aria-label"?: string;
};

export function Select({
    value,
    defaultValue,
    onValueChange,
    options,
    placeholder,
    name,
    disabled,
    invalid,
    "aria-label": ariaLabel,
}: SelectProps) {
    return (
        <SelectPrimitive.Root
            value={value}
            defaultValue={defaultValue}
            onValueChange={onValueChange}
            name={name}
            disabled={disabled}
        >
            <SelectPrimitive.Trigger
                className={[
                    "ui-select",
                    invalid ? "ui-select-invalid" : "",
                ].join(" ")}
                aria-label={ariaLabel}
                aria-invalid={invalid || undefined}
            >
                <SelectPrimitive.Value placeholder={placeholder} />
                <SelectPrimitive.Icon>
                    <Icon icon={ChevronRight} decorative />
                </SelectPrimitive.Icon>
            </SelectPrimitive.Trigger>
            <SelectPrimitive.Portal>
                <SelectPrimitive.Content
                    className="ui-select-content"
                    position="popper"
                    sideOffset={4}
                >
                    <SelectPrimitive.Viewport>
                        {options.map((option) => (
                            <SelectPrimitive.Item
                                key={option.value}
                                className="ui-select-item"
                                value={option.value}
                                disabled={option.disabled}
                            >
                                <SelectPrimitive.ItemText>
                                    {option.label}
                                </SelectPrimitive.ItemText>
                            </SelectPrimitive.Item>
                        ))}
                    </SelectPrimitive.Viewport>
                </SelectPrimitive.Content>
            </SelectPrimitive.Portal>
        </SelectPrimitive.Root>
    );
}
