{
  // Tap the cover to load the Short in YouTube's privacy-enhanced player.
  document.querySelectorAll('button.vid[data-id]').forEach(b => {
    b.addEventListener('click', () => {
      const f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(b.dataset.id) + '?autoplay=1&rel=0&playsinline=1';
      f.allow = 'autoplay; encrypted-media; picture-in-picture';
      f.allowFullscreen = true;
      f.title = 'Video';
      b.querySelector('img')?.remove();
      b.querySelector('.pl')?.remove();
      b.appendChild(f);
    }, {once: true});
  });
}
