import { Icon } from "./Icon";
import { CircleCheck, CircleX, Info, TriangleAlert } from "./icons";

export type StatusKind =
    "approve" | "review" | "decline" | "degraded" | "info" | "neutral";

export type StatusBadgeProps = {
    status: StatusKind;
    label: string;
    detail?: string;
    size?: "small" | "detail";
};

const icons = {
    approve: CircleCheck,
    review: TriangleAlert,
    decline: CircleX,
    degraded: TriangleAlert,
    info: Info,
    neutral: Info,
};

export function StatusBadge({
    status,
    label,
    detail,
    size = "small",
}: StatusBadgeProps) {
    return (
        <span
            className={`ui-status-badge ui-status-${status} ui-status-${size}`}
            title={detail}
        >
            <Icon icon={icons[status]} decorative />
            <span>{label}</span>
        </span>
    );
}
