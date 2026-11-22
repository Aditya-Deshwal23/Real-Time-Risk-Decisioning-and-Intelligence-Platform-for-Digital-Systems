import type { Meta, StoryObj } from "@storybook/react-vite";
import { Button } from "./Button";
import { IconButton } from "./IconButton";
import { Search } from "./icons";
import { Link } from "./Link";
import { TextField } from "./TextField";
import { Select } from "./Select";
import { Checkbox } from "./Checkbox";
import { Switch } from "./Switch";
import { FormField } from "./FormField";
import { Badge } from "./Badge";
import { StatusBadge } from "./StatusBadge";
import { Card } from "./Card";
import { Panel } from "./Panel";
import { Tabs } from "./Tabs";
import { Dialog } from "./Dialog";
import { ConfirmationDialog } from "./ConfirmationDialog";
import { InlineAlert } from "./InlineAlert";
import { Toast } from "./Toast";
import { Tooltip } from "./Tooltip";
import { Skeleton } from "./Skeleton";
import { Spinner } from "./Spinner";
import { EmptyState } from "./EmptyState";
import { CopyButton } from "./CopyButton";
import { CodeBlock } from "./CodeBlock";
import { PageHeader } from "./PageHeader";
import { Table } from "./Table";

const meta: Meta = {
    title: "Primitives",
};

export default meta;
type Story = StoryObj;

export const ButtonStates: Story = {
    render: () => (
        <div
            style={{ display: "flex", gap: "var(--space-3)", flexWrap: "wrap" }}
        >
            <Button variant="primary">Primary</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="tertiary">Tertiary</Button>
            <Button variant="danger">Danger</Button>
            <Button disabled disabledReason="Unavailable">
                Disabled
            </Button>
            <Button loading>Loading</Button>
        </div>
    ),
};

export const IconButtonState: Story = {
    render: () => <IconButton icon={Search} label="Search" />,
};

export const LinkState: Story = {
    render: () => <Link href="#example">Open decision</Link>,
};

export const TextFieldStates: Story = {
    render: () => (
        <div
            style={{
                display: "grid",
                gap: "var(--space-3)",
                maxWidth: "40rem",
            }}
        >
            <FormField
                id="name"
                label="Environment name"
                hint="Shown in audit records"
            >
                <TextField id="name" placeholder="Production" />
            </FormField>
            <FormField
                id="invalid"
                label="Credential"
                error="Enter a credential"
            >
                <TextField id="invalid" invalid />
            </FormField>
            <TextField
                aria-label="Read-only identifier"
                value="vk_live_..."
                readOnly
            />
        </div>
    ),
};

export const SelectState: Story = {
    render: () => (
        <Select
            aria-label="Environment"
            placeholder="Choose an environment"
            options={[
                { value: "sandbox", label: "Sandbox" },
                { value: "live", label: "Live" },
            ]}
        />
    ),
};

export const ChoiceStates: Story = {
    render: () => (
        <div style={{ display: "grid", gap: "var(--space-3)" }}>
            <Checkbox label="Stored securely" />
            <Checkbox label="Disabled" disabled />
            <Switch label="System shortcuts" />
            <Switch label="Disabled switch" disabled />
        </div>
    ),
};

export const BadgeStates: Story = {
    render: () => (
        <div
            style={{ display: "flex", gap: "var(--space-2)", flexWrap: "wrap" }}
        >
            <Badge>Mode</Badge>
            <Badge outline>Demo data</Badge>
            <StatusBadge status="approve" label="Approve" />
            <StatusBadge status="review" label="Review" />
            <StatusBadge status="decline" label="Decline" />
            <StatusBadge
                status="degraded"
                label="Degraded"
                detail="Stale features"
            />
            <StatusBadge status="info" label="Info" />
            <StatusBadge status="neutral" label="Unknown" />
        </div>
    ),
};

export const CardAndPanel: Story = {
    render: () => (
        <div
            style={{
                display: "grid",
                gap: "var(--space-4)",
                maxWidth: "40rem",
            }}
        >
            <Card title="Decision posture">Card content</Card>
            <Panel title="Evidence">Panel content</Panel>
        </div>
    ),
};

export const TabsState: Story = {
    render: () => (
        <Tabs
            defaultValue="summary"
            items={[
                {
                    value: "summary",
                    label: "Summary",
                    content: "Summary content",
                },
                {
                    value: "evidence",
                    label: "Evidence",
                    count: 3,
                    content: "Evidence content",
                },
            ]}
        />
    ),
};

export const DialogStates: Story = {
    render: () => (
        <Dialog
            open
            onOpenChange={() => undefined}
            title="Revoke credential"
            description="This action cannot be undone."
            footer={<Button variant="danger">Revoke credential</Button>}
        >
            Confirm the credential revocation.
        </Dialog>
    ),
};

export const ConfirmationDialogState: Story = {
    render: () => (
        <ConfirmationDialog
            open
            onOpenChange={() => undefined}
            title="Activate policy"
            description="Activation changes live decisions."
            confirmLabel="Activate policy"
            onConfirm={() => undefined}
        />
    ),
};

export const AlertStates: Story = {
    render: () => (
        <div style={{ display: "grid", gap: "var(--space-3)" }}>
            <InlineAlert kind="success" title="Decision sent" />
            <InlineAlert kind="info" title="Demo data">
                This environment uses synthetic values.
            </InlineAlert>
            <InlineAlert kind="warning" title="Stale features" />
            <InlineAlert kind="error" title="Decisions did not load">
                Try again.
            </InlineAlert>
        </div>
    ),
};

export const ToastStates: Story = {
    render: () => (
        <Toast
            open
            onOpenChange={() => undefined}
            kind="success"
            title="Credential copied"
        />
    ),
};

export const TooltipState: Story = {
    render: () => (
        <Tooltip label="This explains the control">
            <button
                type="button"
                className="ui-button ui-button-secondary ui-button-medium"
            >
                Focus me
            </button>
        </Tooltip>
    ),
};

export const LoadingStates: Story = {
    render: () => (
        <div style={{ display: "grid", gap: "var(--space-3)" }}>
            <Skeleton height="panel" />
            <Spinner label="Loading decisions" />
        </div>
    ),
};

export const EmptyStateStory: Story = {
    render: () => (
        <EmptyState
            title="No decisions yet"
            description="Send a test decision from the Developer Portal."
            action={<Button variant="primary">Open Developer Portal</Button>}
        />
    ),
};

export const CopyState: Story = {
    render: () => <CopyButton value="vk_live_example" />,
};

export const CodeState: Story = {
    render: () => (
        <CodeBlock code={'{"decision":"APPROVE"}'} label="Response">
            {'{"decision":"APPROVE"}'}
        </CodeBlock>
    ),
};

export const PageHeaderState: Story = {
    render: () => (
        <PageHeader
            title="Decisions"
            breadcrumbs={<Link href="#decisions">Overview</Link>}
            actions={<Button variant="primary">Send decision</Button>}
        />
    ),
};

export const TableState: Story = {
    render: () => (
        <Table caption="Example decisions">
            <thead>
                <tr>
                    <th scope="col">Time</th>
                    <th scope="col">Decision</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>2026-11-22 12:00:00 UTC</td>
                    <td>
                        <StatusBadge status="approve" label="Approve" />
                    </td>
                </tr>
            </tbody>
        </Table>
    ),
};
