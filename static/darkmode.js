function applyDarkMode(on) {
  if (on) {
    document.body.classList.add('dark-mode');
  } else {
    document.body.classList.remove('dark-mode');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const dark = localStorage.getItem('darkMode') === 'true';
  applyDarkMode(dark);

  const toggle = document.getElementById('toggle-dark');
  if (toggle) {
    if (toggle.type === 'checkbox') {
      toggle.checked = dark;
      toggle.addEventListener('change', () => {
        const enabled = toggle.checked;
        applyDarkMode(enabled);
        localStorage.setItem('darkMode', enabled);
      });
    } else {
      toggle.addEventListener('click', () => {
        const enabled = !document.body.classList.contains('dark-mode');
        applyDarkMode(enabled);
        localStorage.setItem('darkMode', enabled);
      });
    }
  }
});
