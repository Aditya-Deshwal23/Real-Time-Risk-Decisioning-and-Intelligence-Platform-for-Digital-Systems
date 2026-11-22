Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: (query: string) => ({
        matches: false,
        media: query,
        onchange: null,
        addEventListener: () => undefined,
        removeEventListener: () => undefined,
        addListener: () => undefined,
        removeListener: () => undefined,
        dispatchEvent: () => false,
    }),
});

Object.defineProperty(window, "ResizeObserver", {
    writable: true,
    value: class ResizeObserver {
        observe() {}
        unobserve() {}
        disconnect() {}
    },
});

Object.defineProperty(window, "PointerEvent", {
    writable: true,
    value: MouseEvent,
});

HTMLElement.prototype.scrollIntoView = () => undefined;
HTMLElement.prototype.hasPointerCapture = () => false;
HTMLElement.prototype.setPointerCapture = () => undefined;
HTMLElement.prototype.releasePointerCapture = () => undefined;
