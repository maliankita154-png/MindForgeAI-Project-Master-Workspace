const form = document.querySelector('#scenario-form');
if (form) {
  form.querySelectorAll('input[type="range"]').forEach((input) => {
    input.addEventListener('input', () => { input.previousElementSibling.value = `${input.value}%`; });
  });
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('button'); button.textContent = 'Simulating…'; button.disabled = true;
    try {
      const body = Object.fromEntries(new FormData(form));
      const response = await fetch('/api/twin/simulate', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
      const result = await response.json();
      document.querySelector('#result-availability').textContent = `${result.availability}%`;
      document.querySelector('#result-demand').textContent = result.demand;
      document.querySelector('#result-resilience').textContent = result.resilience;
      document.querySelector('#result-heading').textContent = result.resilience >= 75 ? 'Resilient pathway' : 'Intervention needed';
      document.querySelector('#result-recommendation').textContent = result.recommendation;
    } catch (_) { document.querySelector('#result-recommendation').textContent = 'Unable to simulate this scenario. Please try again.'; }
    finally { button.textContent = 'Simulate future →'; button.disabled = false; }
  });
}
