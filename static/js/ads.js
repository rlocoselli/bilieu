(() => {
  const client = document.querySelector('main[data-ad-client]')?.dataset.adClient;
  if (!/^ca-pub-\d+$/.test(client)) return;
  const placements = [...document.querySelectorAll('.ad-placement[data-ad-slot]')];
  let started = false;

  function loadAds() {
    if (started || !navigator.onLine || document.documentElement.dataset.adConsent !== 'accepted') return;
    started = true;
    const script = document.createElement('script');
    script.async = true;
    script.crossOrigin = 'anonymous';
    script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${encodeURIComponent(client)}`;
    script.onload = () => {
      for (const placement of placements) {
        if (!/^\d+$/.test(placement.dataset.adSlot)) continue;
        placement.hidden = false;
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      }
    };
    document.head.append(script);
  }

  loadAds();
  window.addEventListener('bilieu:consent', loadAds);
  window.addEventListener('online', loadAds);
})();
