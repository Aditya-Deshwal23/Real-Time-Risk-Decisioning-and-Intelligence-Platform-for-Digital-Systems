import type { Preview } from "@storybook/react-vite";
import "../src/styles/reset.css";
import "../src/styles/tokens.css";
import "../src/styles/global.css";

const preview: Preview = {
    parameters: {
        layout: "padded",
        controls: { expanded: true },
    },
    globalTypes: {
        theme: {
            name: "Theme",
            description: "VERDICT theme",
            defaultValue: "dark",
            toolbar: {
                icon: "circlehollow",
                items: [
                    { value: "dark", title: "Dark" },
                    { value: "light", title: "Light" },
                ],
            },
        },
    },
    decorators: [
        (Story, context) => {
            document.documentElement.setAttribute(
                "data-theme",
                context.globals.theme === "light" ? "light" : "dark",
            );
            return Story();
        },
    ],
};

export default preview;
