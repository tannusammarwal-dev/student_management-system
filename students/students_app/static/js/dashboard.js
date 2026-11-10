
document.addEventListener("DOMContentLoaded", function () {

    const messages = document.querySelectorAll(".auto-dismiss");

    messages.forEach(function (message) {

        setTimeout(function () {
            message.classList.add("hide-message");

            setTimeout(function () {
                message.remove();
            }, 400);

        }, 3000);

    });

});
