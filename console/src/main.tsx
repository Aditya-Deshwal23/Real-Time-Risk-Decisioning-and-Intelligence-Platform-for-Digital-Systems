import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./app/App";
import "./styles/reset.css";
import "./styles/tokens.css";
import "./styles/global.css";
import { ThemeProvider } from "./theme/ThemeProvider";

const rootElement = document.getElementById("root");

if (rootElement === null) {
    throw new Error("Missing console root element");
}

createRoot(rootElement).render(
    <StrictMode>
        <ThemeProvider>
            <App />
        </ThemeProvider>
    </StrictMode>,
);
