const $ = (s) => document.querySelector(s);

async function load() {
  const { customRules } = await chrome.storage.local.get({ customRules: [] });
  $('#rules').value = JSON.stringify(customRules, null, 2);
}

$('#save').addEventListener('click', async () => {
  try {
    const parsed = JSON.parse($('#rules').value || '[]');
    if (!Array.isArray(parsed)) throw new Error('Rules must be an array');
    await chrome.runtime.sendMessage({ type: 'setCustomRules', rules: parsed });
    $('#status').textContent = 'Saved & applied.';
    setTimeout(() => $('#status').textContent = '', 1500);
  } catch (e) {
    $('#status').textContent = 'Error: ' + e.message;
  }
});

$('#clear').addEventListener('click', async () => {
  $('#rules').value = '[]';
  await chrome.runtime.sendMessage({ type: 'setCustomRules', rules: [] });
  $('#status').textContent = 'Cleared.';
  setTimeout(() => $('#status').textContent = '', 1500);
});

load();