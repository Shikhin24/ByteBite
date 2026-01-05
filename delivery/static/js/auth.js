document.addEventListener("DOMContentLoaded", () => {
  const signinTab = document.getElementById("signinTab");
  const signupTab = document.getElementById("signupTab");
  const signinForm = document.getElementById("signinForm");
  const signupForm = document.getElementById("signupForm");

  function activate(tab) {
    const isSignin = tab === "signin";

    signinTab.classList.toggle("active", isSignin);
    signupTab.classList.toggle("active", !isSignin);
    signinForm.classList.toggle("active", isSignin);
    signupForm.classList.toggle("active", !isSignin);
  }

  signinTab.addEventListener("click", () => activate("signin"));
  signupTab.addEventListener("click", () => activate("signup"));

  document.querySelectorAll(".toggle-password").forEach(btn => {
    btn.addEventListener("click", () => {
      const input = document.getElementById(btn.dataset.target);
      if (!input) return;

      const show = input.type === "password";
      input.type = show ? "text" : "password";
      btn.classList.toggle("visible", show);
    });
  });
});
