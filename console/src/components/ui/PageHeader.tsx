import type { ReactNode } from "react";

export type PageHeaderProps = {
    title: string;
    breadcrumbs?: ReactNode;
    actions?: ReactNode;
};

export function PageHeader({ title, breadcrumbs, actions }: PageHeaderProps) {
    return (
        <header className="ui-page-header">
            {breadcrumbs}
            <div className="ui-page-header-row">
                <h1 tabIndex={-1}>{title}</h1>
                {actions ? (
                    <div className="ui-page-header-actions">{actions}</div>
                ) : null}
            </div>
        </header>
    );
}
