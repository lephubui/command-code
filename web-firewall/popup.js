function send(msg) {
  return new Promise((resolve) => chrome.runtime.sendMessage(msg, resolve));
}

async function init() {
  const state = await send({ type: 'getState' });
  document.getElementById('blocked').textContent = state.blockedCount || 0;
  document.getElementById('mode').value = state.mode || 'balanced';
}

document.getElementById('mode').addEventListener('change', async (e) => {
  await send({ type: 'setMode', mode: e.target.value });
  await init();
});

document.getElementById('options').addEventListener('click', () => {
  chrome.runtime.openOptionsPage();
});

document.getElementById('telemetry').addEventListener('click', () => {
  window.open(chrome.runtime.getURL('telemetry.html'), '_blank');
});

document.getElementById('about').addEventListener('click', () => {
  window.open('https://www.cclabs.dev/product/web-firewall', '_blank');
});

init();