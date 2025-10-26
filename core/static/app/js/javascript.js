document.addEventListener("DOMContentLoaded", function(event) {
    console.log("JavaScript cargado correctamente");

    const showNavbar = (toggleId, navId, bodyId, headerId) => {
        console.log("Ejecutando showNavbar...");
        const toggle = document.getElementById(toggleId),
            nav = document.getElementById(navId),
            bodypd = document.getElementById(bodyId),
            headerpd = document.getElementById(headerId);

        if (toggle && nav && bodypd && headerpd) {
            toggle.addEventListener('click', () => {
                console.log("Navbar toggle clickeado");
                nav.classList.toggle('show');
                toggle.classList.toggle('bx-x');
                bodypd.classList.toggle('body-pd');
                headerpd.classList.toggle('body-pd');
            });
        } else {
            console.log("Algunos elementos no existen en el DOM");
        }
    };

    showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header');

    const linkColor = document.querySelectorAll('.nav_link');

    function colorLink() {
        if (linkColor) {
            console.log("Cambiando color de enlace");
            linkColor.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        }
    }

    linkColor.forEach(l => l.addEventListener('click', colorLink));

    console.log("Script ejecutado correctamente");
});
