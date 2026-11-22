import type { ReactNode } from "react";

export type TableProps = {
    caption: string;
    children: ReactNode;
};

export function Table({ caption, children }: TableProps) {
    return (
        <div
            className="ui-table-scroll"
            role="region"
            tabIndex={0}
            aria-label={`${caption} table`}
        >
            <table className="ui-table">
                <caption className="ui-visually-hidden">{caption}</caption>
                {children}
            </table>
        </div>
    );
}
