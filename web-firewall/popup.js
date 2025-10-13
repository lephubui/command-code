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
  chrome.tabs.create({ url: chrome.runtime.getURL('telemetry.html') });
});

document.getElementById('about').addEventListener('click', () => {
  chrome.tabs.create({ url: 'https://www.cclabs.dev/product/web-firewall-extention' });
});

init();