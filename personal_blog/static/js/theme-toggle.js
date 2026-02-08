(function () {
  const toggle = document.getElementById('theme-toggle');
  if (!toggle) return;

  const applyTheme = (mode) => {
    if (mode === 'dark') {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  };

  const stored = window.localStorage.getItem('theme');
  if (stored === 'dark') {
    applyTheme('dark');
    toggle.checked = true;
  }

  toggle.addEventListener('change', () => {
    const mode = toggle.checked ? 'dark' : 'light';
    applyTheme(mode);
    window.localStorage.setItem('theme', mode);
  });
})();
