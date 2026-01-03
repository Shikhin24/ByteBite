(function () {

  function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("theme", theme);

    const btn = document.getElementById("themeToggle");
    if (btn) btn.textContent = theme === "light" ? "🌙" : "☀️";
  }

  function syncTheme() {
    const theme = localStorage.getItem("theme") || "dark";
    document.documentElement.dataset.theme = theme;
  }

  // ✅ Runs on normal load
  document.addEventListener("DOMContentLoaded", () => {
    syncTheme();

    const toggleBtn = document.getElementById("themeToggle");
    if (!toggleBtn) return;

    toggleBtn.addEventListener("click", () => {
      const current = document.documentElement.dataset.theme;
      setTheme(current === "dark" ? "light" : "dark");
    });
  });

  // ✅ Runs on back/forward cache restore
  window.addEventListener("pageshow", syncTheme);

})();
