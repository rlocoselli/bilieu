const carousel = document.querySelector('[data-carousel]');

for (const oldConsentKey of ['bilieu_cookie_consent', 'bilieu_cookie_consent_v2']) {
  document.cookie = `${oldConsentKey}=; path=/; max-age=0; samesite=lax`;
  try {
    localStorage.removeItem(oldConsentKey);
  } catch (error) {}
}

const cookieSettingsButtons = document.querySelectorAll('.cookie-settings-btn');

const openPrivacySettings = () => {
  if (!document.querySelector('main[data-ad-client]')) {
    const url = new URL('/', window.location.origin);
    url.searchParams.set('lang', document.documentElement.lang || 'fr');
    url.searchParams.set('privacy-settings', '1');
    window.location.assign(url);
    return;
  }

  window.googlefc = window.googlefc || {};
  window.googlefc.callbackQueue = window.googlefc.callbackQueue || [];
  window.googlefc.callbackQueue.push({
    CONSENT_API_READY: () => window.googlefc.showRevocationMessage(),
  });
};

cookieSettingsButtons.forEach((button) => {
  button.addEventListener('click', openPrivacySettings);
});

if (new URLSearchParams(window.location.search).get('privacy-settings') === '1') {
  openPrivacySettings();
}

const header = document.querySelector('.site-header');
const navToggle = document.querySelector('.nav-toggle');
const tabsGroups = document.querySelectorAll('[data-tabs]');

tabsGroups.forEach((group) => {
  const tabButtons = Array.from(group.querySelectorAll('[data-tab-btn]'));
  const tabPanels = Array.from(group.querySelectorAll('[data-tab-panel]'));

  if (!tabButtons.length || !tabPanels.length) return;

  const setActiveTab = (nextIndex) => {
    tabButtons.forEach((button, index) => {
      const isActive = index === nextIndex;
      button.classList.toggle('active', isActive);
      button.setAttribute('aria-selected', String(isActive));
      if (isActive) {
        button.focus();
      }
    });

    tabPanels.forEach((panel, index) => {
      panel.hidden = index !== nextIndex;
    });
  };

  tabButtons.forEach((button, index) => {
    button.addEventListener('click', () => setActiveTab(index));

    button.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowRight') {
        event.preventDefault();
        setActiveTab((index + 1) % tabButtons.length);
      }

      if (event.key === 'ArrowLeft') {
        event.preventDefault();
        setActiveTab((index - 1 + tabButtons.length) % tabButtons.length);
      }

      if (event.key === 'Home') {
        event.preventDefault();
        setActiveTab(0);
      }

      if (event.key === 'End') {
        event.preventDefault();
        setActiveTab(tabButtons.length - 1);
      }
    });
  });
});

if (header && navToggle) {
  const toggleHeaderSolid = () => {
    header.classList.add('header-solid');
  };

  const updateHeaderOffset = () => {
    if (header.classList.contains('nav-open')) return;
    document.documentElement.style.setProperty('--header-offset', `${header.offsetHeight}px`);
  };

  const closeNav = () => {
    header.classList.remove('nav-open');
    navToggle.setAttribute('aria-expanded', 'false');
  };

  navToggle.addEventListener('click', () => {
    const isOpen = header.classList.toggle('nav-open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
    if (!isOpen) {
      updateHeaderOffset();
    }
  });

  header.querySelectorAll('.main-nav a, .lang-switch a').forEach((link) => {
    link.addEventListener('click', closeNav);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 980) {
      closeNav();
    }
    updateHeaderOffset();
  });

  window.addEventListener('scroll', toggleHeaderSolid, { passive: true });
  toggleHeaderSolid();
  updateHeaderOffset();
}

if (carousel) {
  const slides = Array.from(carousel.querySelectorAll('.carousel-slide'));
  const dots = Array.from(carousel.querySelectorAll('.dot'));
  const prev = carousel.querySelector('.prev');
  const next = carousel.querySelector('.next');

  let index = 0;

  const setSlide = (newIndex) => {
    if (!slides.length) return;
    slides[index].classList.remove('active');
    if (dots[index]) dots[index].classList.remove('active');
    index = (newIndex + slides.length) % slides.length;
    slides[index].classList.add('active');
    if (dots[index]) dots[index].classList.add('active');
  };

  if (prev) prev.addEventListener('click', () => setSlide(index - 1));
  if (next) next.addEventListener('click', () => setSlide(index + 1));

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => setSlide(i));
  });

  if (slides.length > 1) {
    setInterval(() => setSlide(index + 1), 5000);
  }
}

const loadVideo = (button) => {
    const videoId = button.getAttribute('data-video-id');
    const placeholder = button.closest('[data-video-placeholder]');

    if (!videoId || !placeholder) return;

    const frameWrap = document.createElement('div');
    frameWrap.className = 'video-embed-wrap';

    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?rel=0&modestbranding=1&autoplay=1&mute=1&playsinline=1`;
    iframe.title = 'YouTube video';
    iframe.loading = 'lazy';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    iframe.setAttribute('allowfullscreen', '');

    frameWrap.appendChild(iframe);
    placeholder.replaceWith(frameWrap);
};

document.querySelectorAll('[data-load-video]').forEach((button) => {
  button.addEventListener('click', () => loadVideo(button));
});

document.querySelectorAll('[data-auto-video]').forEach((placeholder) => {
  const button = placeholder.querySelector('[data-load-video]');
  if (button) loadVideo(button);
});
