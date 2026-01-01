(function () {
  function applyTheme() {
    const theme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", theme);
    updateIcon(theme);
  }

  function updateIcon(theme) {
    const btn = document.getElementById("themeToggle");
    if (!btn) return;
    btn.textContent = theme === "light" ? "🌙" : "☀️";
  }

  function animateIcon(btn) {
    btn.classList.remove("spin");
    void btn.offsetWidth;
    btn.classList.add("spin");
  }

  // ✅ Normal page load
  document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("themeToggle");
    applyTheme();

    toggleBtn.addEventListener("click", () => {
      const next =
        document.documentElement.getAttribute("data-theme") === "light"
          ? "dark"
          : "light";

      localStorage.setItem("theme", next);
      document.documentElement.setAttribute("data-theme", next);
      animateIcon(toggleBtn);
      updateIcon(next);
    });
  });

window.addEventListener("pageshow", () => {
  const html = document.documentElement;

  const theme = localStorage.getItem("theme") || "dark";
  html.setAttribute("data-theme", theme);

  // 🔥 FORCE REPAINT (THIS IS THE KEY)
  html.style.display = "none";
  html.offsetHeight; // force reflow
  html.style.display = "";
});

})();
