const $ = (s) => document.querySelector(s);
function send(msg) { return new Promise((resolve) => chrome.runtime.sendMessage(msg, resolve)); }

function fmtTime(ts) { const d = new Date(ts); return d.toLocaleString(); }

async function load() {
  // Add loading state
  const refreshBtn = $('#refresh');
  const originalText = refreshBtn.textContent;
  refreshBtn.textContent = '🔄 Loading...';
  refreshBtn.disabled = true;
  
  try {
    const res = await send({ type: 'telemetry:get' });
    if (!res?.ok) { 
      alert('Failed to load telemetry: ' + (res?.error || 'Unknown error')); 
      return; 
    }
    const t = res.telemetry;
    
    // Update meta information
    $('#meta').textContent = `Total blocked: ${t.totalBlocked || 0} • Since: ${fmtTime(t.lastReset || Date.now())} • Events stored: ${(t.events || []).length}`;

    // Top domains
    const dtbody = $('#tblDomains tbody'); 
    dtbody.innerHTML = '';
    const domains = Object.entries(t.perDomain || {}).sort((a,b)=>b[1]-a[1]).slice(0,20);
    if (domains.length === 0) {
      dtbody.innerHTML = '<tr><td colspan="2" style="text-align: center; color: #666;">No blocked domains yet</td></tr>';
    } else {
      domains.forEach(([dom, cnt])=>{
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${dom || '<em>(unknown)</em>'}</td><td>${cnt}</td>`;
        dtbody.appendChild(tr);
      });
    }

    // Top rules
    const rtbody = $('#tblRules tbody'); 
    rtbody.innerHTML = '';
    const rules = Object.entries(t.perRule || {}).sort((a,b)=>b[1]-a[1]).slice(0,20);
    if (rules.length === 0) {
      rtbody.innerHTML = '<tr><td colspan="2" style="text-align: center; color: #666;">No active rules yet</td></tr>';
    } else {
      for (const [rid, cnt] of rules) {
        const tr = document.createElement('tr');
        // Get rule description
        const descRes = await send({ type: 'getRuleDescription', ruleId: rid });
        const description = descRes?.description || 'Security rule';
        tr.innerHTML = `<td><code style="cursor: help;" title="${description}">${rid}</code><br><small style="color: #888; font-size: 11px;">${description}</small></td><td>${cnt}</td>`;
        rtbody.appendChild(tr);
      }
    }

    // Recent events
    const ebody = $('#tblEvents tbody'); 
    ebody.innerHTML = '';
    const events = [...(t.events || [])].slice(-100).reverse();
    if (events.length === 0) {
      ebody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #666;">No security events yet</td></tr>';
    } else {
      for (const ev of events) {
        const tr = document.createElement('tr');
        const safeUrl = ev.url.length > 120 ? ev.url.slice(0,120) + '…' : ev.url;
        // Get rule description for tooltip
        const descRes = await send({ type: 'getRuleDescription', ruleId: ev.ruleId });
        const description = descRes?.description || 'Security rule';
        tr.innerHTML = `<td>${fmtTime(ev.ts)}</td><td>${ev.domain}</td><td><code style="cursor: help;" title="${description}">${ev.ruleId}</code></td><td>${ev.action}</td><td title="${ev.url}">${safeUrl}</td>`;
        ebody.appendChild(tr);
      }
    }
  } catch (error) {
    console.error('Error loading telemetry:', error);
    alert('Error loading telemetry data: ' + error.message);
  } finally {
    // Restore button state
    refreshBtn.textContent = originalText;
    refreshBtn.disabled = false;
  }
}

$('#refresh').addEventListener('click', load);
$('#clear').addEventListener('click', async ()=>{ const r = confirm('Clear telemetry?'); if (!r) return; const res = await send({ type: 'telemetry:clear' }); if(res?.ok) load(); });

$('#exportJson').addEventListener('click', async ()=>{
  const res = await send({ type: 'telemetry:get' });
  if (!res?.ok) return alert(res?.error || 'Error');
  const blob = new Blob([JSON.stringify(res.telemetry, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = 'web-firewall-telemetry.json'; a.click(); URL.revokeObjectURL(url);
});

$('#exportCsv').addEventListener('click', async ()=>{
  const res = await send({ type: 'telemetry:get' });
  if (!res?.ok) return alert(res?.error || 'Error');
  const rows = [['ts','time','domain','ruleId','rulesetId','action','url']];
  res.telemetry.events.forEach(ev => rows.push([ev.ts, new Date(ev.ts).toISOString(), ev.domain, ev.ruleId, ev.rulesetId, ev.action, ev.url]));
  const csv = rows.map(r => r.map(v => '"' + String(v).replaceAll('"','""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = 'web-firewall-telemetry.csv'; a.click(); URL.revokeObjectURL(url);
});

load();