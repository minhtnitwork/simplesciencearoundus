{
  // On the real site, play the Short in a privacy-enhanced player; elsewhere (previews) the card just links to YouTube.
  const embedOK = !/claude|anthropic/.test(location.hostname);
  document.querySelectorAll('a.vid[data-id]').forEach(a => {
    a.addEventListener('click', ev => {
      if (!embedOK) return;
      ev.preventDefault();
      const f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(a.dataset.id) + '?autoplay=1&rel=0';
      f.allow = 'autoplay; encrypted-media; picture-in-picture';
      f.allowFullscreen = true;
      f.title = a.querySelector('.vq')?.textContent || 'Video';
      const box = document.createElement('div');
      box.className = a.className;
      box.setAttribute('style', a.getAttribute('style') || '');
      box.appendChild(f);
      a.replaceWith(box);
    });
  });
}
