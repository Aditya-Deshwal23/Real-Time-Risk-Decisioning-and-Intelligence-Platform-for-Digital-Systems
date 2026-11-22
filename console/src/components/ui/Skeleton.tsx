export type SkeletonProps = {
    width?: "full" | "long" | "medium" | "short";
    height?: "text" | "row" | "panel";
};

export function Skeleton({ width = "full", height = "text" }: SkeletonProps) {
    return (
        <span
            className={`ui-skeleton ui-skeleton-${width} ui-skeleton-${height}`}
            aria-hidden="true"
        />
    );
}
