document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("themeToggle");

  const current = document.documentElement.dataset.theme || "dark";
  updateIcon(current);

  toggleBtn.addEventListener("click", () => {
    const html = document.documentElement;
    const next = html.dataset.theme === "light" ? "dark" : "light";

    html.dataset.theme = next;
    localStorage.setItem("theme", next);

    animateIcon(toggleBtn);
    updateIcon(next);
  });
});

function updateIcon(theme) {
  const btn = document.getElementById("themeToggle");
  btn.textContent = theme === "light" ? "🌙" : "☀️";
}

function animateIcon(btn) {
  btn.classList.remove("spin");
  void btn.offsetWidth;
  btn.classList.add("spin");
}
