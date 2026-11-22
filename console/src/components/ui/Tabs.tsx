import * as TabsPrimitive from "@radix-ui/react-tabs";
import type { ReactNode } from "react";

export type TabItem = {
    value: string;
    label: string;
    count?: number;
    content: ReactNode;
};

export type TabsProps = {
    items: TabItem[];
    value?: string;
    defaultValue?: string;
    onValueChange?: (value: string) => void;
};

export function Tabs({ items, value, defaultValue, onValueChange }: TabsProps) {
    return (
        <TabsPrimitive.Root
            className="ui-tabs"
            value={value}
            defaultValue={defaultValue ?? items[0]?.value}
            onValueChange={onValueChange}
        >
            <TabsPrimitive.List className="ui-tabs-list" aria-label="View">
                {items.map((item) => (
                    <TabsPrimitive.Trigger
                        key={item.value}
                        className="ui-tab"
                        value={item.value}
                    >
                        {item.label}
                        {item.count !== undefined ? (
                            <span className="ui-tab-count">{item.count}</span>
                        ) : null}
                    </TabsPrimitive.Trigger>
                ))}
            </TabsPrimitive.List>
            {items.map((item) => (
                <TabsPrimitive.Content
                    key={item.value}
                    className="ui-tab-panel"
                    value={item.value}
                >
                    {item.content}
                </TabsPrimitive.Content>
            ))}
        </TabsPrimitive.Root>
    );
}
