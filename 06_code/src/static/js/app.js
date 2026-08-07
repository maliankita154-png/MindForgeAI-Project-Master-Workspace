document.querySelector('.menu-toggle')?.addEventListener('click', (event) => {
  const nav = document.querySelector('.site-nav');
  const expanded = event.currentTarget.getAttribute('aria-expanded') === 'true';
  event.currentTarget.setAttribute('aria-expanded', String(!expanded));
  nav.style.display = expanded ? '' : 'flex';
});
