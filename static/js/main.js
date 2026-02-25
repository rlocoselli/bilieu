const carousel = document.querySelector('[data-carousel]');

const cookieBanner = document.querySelector('[data-cookie-banner]');
const cookieAcceptBtn = document.querySelector('[data-cookie-accept]');
const cookieDeclineBtn = document.querySelector('[data-cookie-decline]');
const cookieSettingsButtons = document.querySelectorAll('.cookie-settings-btn');

if (cookieBanner) {
  const cookieKey = 'bilieu_cookie_consent';

  const readCookieConsent = () => {
    const match = document.cookie.match(/(?:^|; )bilieu_cookie_consent=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : null;
  };

  const readConsent = () => {
    try {
      return localStorage.getItem(cookieKey) || readCookieConsent();
    } catch (error) {
      return readCookieConsent();
    }
  };

  const writeConsent = (value) => {
    document.cookie = `bilieu_cookie_consent=${encodeURIComponent(value)}; path=/; max-age=31536000; samesite=lax`;
    try {
      localStorage.setItem(cookieKey, value);
    } catch (error) {}
  };

  const clearConsent = () => {
    document.cookie = 'bilieu_cookie_consent=; path=/; max-age=0; samesite=lax';
    try {
      localStorage.removeItem(cookieKey);
    } catch (error) {}
  };

  const hasDecision = readConsent();

  const showCookieBanner = () => {
    cookieBanner.hidden = false;
  };

  const hideCookieBanner = () => {
    cookieBanner.hidden = true;
    cookieBanner.style.display = 'none';
  };

  if (!hasDecision) {
    cookieBanner.style.display = '';
    showCookieBanner();
  } else {
    hideCookieBanner();
  }

  if (cookieAcceptBtn) {
    cookieAcceptBtn.addEventListener('click', () => {
      writeConsent('accepted');
      hideCookieBanner();
    });
  }

  if (cookieDeclineBtn) {
    cookieDeclineBtn.addEventListener('click', () => {
      writeConsent('declined');
      hideCookieBanner();
    });
  }

  cookieSettingsButtons.forEach((button) => {
    button.addEventListener('click', () => {
      clearConsent();
      showCookieBanner();
    });
  });
}

const header = document.querySelector('.site-header');
const navToggle = document.querySelector('.nav-toggle');

if (header && navToggle) {
  const closeNav = () => {
    header.classList.remove('nav-open');
    navToggle.setAttribute('aria-expanded', 'false');
  };

  navToggle.addEventListener('click', () => {
    const isOpen = header.classList.toggle('nav-open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  header.querySelectorAll('.main-nav a, .lang-switch a').forEach((link) => {
    link.addEventListener('click', closeNav);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 980) {
      closeNav();
    }
  });
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
