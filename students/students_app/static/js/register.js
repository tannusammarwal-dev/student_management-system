
/* ==============================
   SHOW / HIDE PASSWORD
============================== */

function togglePassword(inputId, icon) {

    const passwordInput = document.getElementById(inputId);

    if (passwordInput.type === "password") {

        passwordInput.type = "text";

        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");

    } else {

        passwordInput.type = "password";

        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");

    }

}


/* ==============================
   INPUT FOCUS EFFECT
============================== */

document.querySelectorAll(".input-box input").forEach(function(input) {

    input.addEventListener("focus", function() {

        input.parentElement.classList.add("focused");

    });

    input.addEventListener("blur", function() {

        input.parentElement.classList.remove("focused");

    });

});
