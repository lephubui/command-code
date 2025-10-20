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
  try {
    // Get current mode before clearing
    const currentState = await chrome.runtime.sendMessage({ type: 'getState' });
    const previousMode = currentState?.mode || 'balanced';
    
    // Clear the custom rules in UI
    $('#rules').value = '[]';
    
    // Clear custom rules in background
    const clearResult = await chrome.runtime.sendMessage({ type: 'setCustomRules', rules: [] });
    
    if (!clearResult?.ok) {
      throw new Error(clearResult?.error || 'Failed to clear custom rules');
    }
    
    // Wait a moment for the clear to complete
    await new Promise(resolve => setTimeout(resolve, 200));
    
    // Verify the mode is still correct
    const finalState = await chrome.runtime.sendMessage({ type: 'getState' });
    const finalMode = finalState?.mode;
    
    if (finalMode === 'off' && previousMode !== 'off') {
      // Mode was unexpectedly disabled, restore it
      await chrome.runtime.sendMessage({ type: 'setMode', mode: previousMode });
      $('#status').textContent = `Rules cleared and mode restored to ${previousMode}.`;
    } else {
      $('#status').textContent = `Rules cleared successfully. Mode: ${finalMode}.`;
    }
    
    $('#status').className = 'success';
    
    setTimeout(() => {
      $('#status').textContent = '';
      $('#status').className = '';
    }, 3000);
    
  } catch (error) {
    console.error('Error in clear operation:', error);
    $('#status').textContent = 'Error: ' + error.message;
    $('#status').className = 'error';
    setTimeout(() => {
      $('#status').textContent = '';
      $('#status').className = '';
    }, 3000);
  }
});

load();