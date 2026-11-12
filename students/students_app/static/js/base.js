
document.addEventListener('DOMContentLoaded', function () {

    // Mobile Sidebar
    const menuBtn = document.getElementById('menuBtn');
    const closeBtn = document.getElementById('closeBtn');
    const sidebar = document.getElementById('sidebar');

    if (menuBtn && sidebar) {
        menuBtn.addEventListener('click', () => {
            sidebar.classList.add('open');
        });
    }

    if (closeBtn && sidebar) {
        closeBtn.addEventListener('click', () => {
            sidebar.classList.remove('open');
        });
    }

    if (sidebar) {
        sidebar.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                sidebar.classList.remove('open');
            });
        });
    }

    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && sidebar) {
            sidebar.classList.remove('open');
        }
    });


    // Success Message Auto Hide
    const messages = document.querySelectorAll('.auto-dismiss');

    messages.forEach(message => {

        if (message.classList.contains('alert-success')) {

            setTimeout(() => {
                message.classList.add('hide-message');

                setTimeout(() => {
                    message.remove();
                }, 500);

            }, 3000);

        }

    });

});
