const carousel = document.querySelector('[data-carousel]');

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
