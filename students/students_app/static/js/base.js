  const menuBtn = document.getElementById('menuBtn');
  const closeBtn = document.getElementById('closeBtn');
  const sidebar = document.getElementById('sidebar');

  menuBtn.addEventListener('click', () => sidebar.classList.add('open'));
  closeBtn.addEventListener('click', () => sidebar.classList.remove('open'));

  // Close when a nav link is clicked, or when Esc is pressed
  sidebar.querySelectorAll('.nav-link').forEach(link =>
    link.addEventListener('click', () => sidebar.classList.remove('open'))
  );
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') sidebar.classList.remove('open');
  });