(() => {
  const client = document.querySelector('main[data-ad-client]')?.dataset.adClient;
  if (!/^ca-pub-\d+$/.test(client)) return;

  for (const placement of document.querySelectorAll('.ad-placement[data-ad-slot]')) {
    if (!/^\d+$/.test(placement.dataset.adSlot)) continue;
    placement.hidden = false;
    (window.adsbygoogle = window.adsbygoogle || []).push({});
  }
})();
