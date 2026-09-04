const unitButtons = document.querySelectorAll('.unit-toggle');
const controlResult = document.querySelector('.control-result');

unitButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const isFahrenheit = button.dataset.unit === 'f';
    unitButtons.forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
    controlResult.textContent = isFahrenheit
      ? 'Nighttime trend: +0.68°F per decade'
      : 'Nighttime trend: +0.38°C per decade';
  });
});
