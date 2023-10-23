document.addEventListener("DOMContentLoaded", function () {
    const mensaje = document.getElementById("mensaje");

    setTimeout(function () {
        mensaje.style.opacity = 0;
        setTimeout(function () {
            mensaje.style.opacity = 1;
        }, 1000);
        mensaje.classList.remove("oculto");
    }, 1000);

    setTimeout(function () {
        mensaje.style.opacity = 0;
        setTimeout(function () {
            mensaje.style.display = "none";
        }, 2000);
    }, 6000);
});