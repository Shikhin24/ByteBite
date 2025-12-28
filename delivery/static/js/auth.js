document.addEventListener("DOMContentLoaded", () => {

  const signinTab = document.getElementById("signinTab");
  const signupTab = document.getElementById("signupTab");
  const signinForm = document.getElementById("signinForm");
  const signupForm = document.getElementById("signupForm");

  signinTab.onclick = () => {
    signinTab.classList.add("active");
    signupTab.classList.remove("active");
    signinForm.classList.add("active");
    signupForm.classList.remove("active");
  };

  signupTab.onclick = () => {
    signupTab.classList.add("active");
    signinTab.classList.remove("active");
    signupForm.classList.add("active");
    signinForm.classList.remove("active");
  };

  signinTab.addEventListener("click", () => {
    signinTab.classList.add("active");
    signupTab.classList.remove("active");

    signinForm.classList.add("active");
    signupForm.classList.remove("active");
  });

  signupTab.addEventListener("click", () => {
    signupTab.classList.add("active");
    signinTab.classList.remove("active");

    signupForm.classList.add("active");
    signinForm.classList.remove("active");
  });

  document.querySelectorAll(".toggle-password").forEach(btn => {
    btn.onclick = () => {
      const input = document.getElementById(btn.dataset.target);
      if (!input) return;
      const hidden = input.type === "password";
      input.type = hidden ? "text" : "password";
      btn.classList.toggle("visible", hidden);
    };
  });

});

