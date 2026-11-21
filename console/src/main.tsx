import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./app/App";
import "./styles/reset.css";

const rootElement = document.getElementById("root");

if (rootElement === null) {
    throw new Error("Missing console root element");
}

createRoot(rootElement).render(
    <StrictMode>
        <App />
    </StrictMode>,
);
