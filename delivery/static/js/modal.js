document.addEventListener("DOMContentLoaded", () => {
  const modals = document.querySelectorAll(".modal-overlay");

  function closeAllModals() {
    modals.forEach(modal => modal.classList.remove("active"));
    document.body.classList.remove("modal-open");
  }

  // 🔹 Close on backdrop click
  modals.forEach(modal => {
    modal.addEventListener("click", e => {
      if (e.target === modal) {
        closeAllModals();
      }
    });
  });

  // 🔹 Close on ESC key
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") {
      closeAllModals();
    }
  });

  // 🔹 Expose helpers globally
  window.openModal = (id) => {
    closeAllModals();
    const modal = document.getElementById(id);
    if (modal) {
      modal.classList.add("active");
      document.body.classList.add("modal-open");
    }
  };

  window.closeModals = closeAllModals;
});
