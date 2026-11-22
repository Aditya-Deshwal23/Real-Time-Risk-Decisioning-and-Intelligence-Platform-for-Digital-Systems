(function () {
    var choice = "dark";
    try {
        var stored = localStorage.getItem("verdict-theme-preference");
        if (stored === "light" || stored === "dark" || stored === "system") {
            choice = stored;
        }
    } catch (_) {}

    var theme = choice;
    if (choice === "system") {
        theme =
            window.matchMedia &&
            window.matchMedia("(prefers-color-scheme: light)").matches
                ? "light"
                : "dark";
    }
    document.documentElement.setAttribute("data-theme", theme);
})();
