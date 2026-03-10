with open(r'C:\Users\stree\Desktop\jogopulo\public\game.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Add Supabase CDN + leaderboard CSS + overlay HTML ──────────────
css_and_overlay = '''
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js"></script>
<style>
#game-wrap { position: relative; display: inline-block; }
#lb-overlay {
  display: none;
  position: absolute;
  top: 0; left: 0; width: 900px; height: 500px;
  background: linear-gradient(160deg, rgba(8,4,18,0.96) 0%, rgba(14,8,4,0.97) 100%);
  font-family: 'Georgia', serif;
  color: #ffe0a0;
  z-index: 10;
  overflow-y: auto;
}
#lb-overlay .lb-inner {
  padding: 28px 40px 20px;
  display: flex;
  gap: 32px;
  height: 100%;
  box-sizing: border-box;
}
/* ── LEFT: submit panel ── */
#lb-overlay .lb-left {
  flex: 0 0 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-right: 1px solid rgba(255,200,60,0.18);
  padding-right: 32px;
}
#lb-overlay .lb-title {
  font-size: 22px;
  letter-spacing: 5px;
  color: #ffe040;
  text-align: center;
  margin-bottom: 4px;
  text-shadow: 0 0 18px rgba(255,220,0,0.5);
}
#lb-overlay .lb-score-big {
  font-size: 62px;
  font-weight: bold;
  letter-spacing: 2px;
  color: #ffe040;
  text-shadow: 0 0 30px rgba(255,200,0,0.7);
  line-height: 1.1;
}
#lb-overlay .lb-score-label {
  font-size: 11px;
  letter-spacing: 4px;
  color: rgba(255,200,120,0.55);
  margin-bottom: 20px;
}
#lb-overlay .lb-rating {
  font-size: 15px;
  letter-spacing: 4px;
  margin-bottom: 6px;
}
#lb-overlay .lb-stars {
  font-size: 20px;
  letter-spacing: 4px;
  margin-bottom: 22px;
}
#lb-overlay .lb-sep {
  width: 80%;
  border: none;
  border-top: 1px solid rgba(255,200,60,0.20);
  margin: 0 auto 18px;
}
#lb-overlay .lb-ask {
  font-size: 12px;
  letter-spacing: 3px;
  color: rgba(255,210,150,0.75);
  margin-bottom: 10px;
  text-align: center;
}
#lb-overlay #lb-name {
  width: 220px;
  background: rgba(255,200,60,0.07);
  border: 1px solid rgba(255,200,60,0.35);
  border-radius: 4px;
  color: #ffe0a0;
  font-family: 'Georgia', serif;
  font-size: 15px;
  letter-spacing: 3px;
  padding: 8px 14px;
  text-align: center;
  outline: none;
  margin-bottom: 10px;
  transition: border-color .2s;
}
#lb-overlay #lb-name:focus { border-color: rgba(255,200,60,0.7); }
#lb-overlay #lb-name::placeholder { color: rgba(255,200,100,0.3); letter-spacing: 2px; }
#lb-overlay #lb-submit {
  width: 220px;
  padding: 9px;
  background: rgba(255,200,60,0.12);
  border: 1px solid rgba(255,200,60,0.45);
  border-radius: 4px;
  color: #ffe040;
  font-family: 'Georgia', serif;
  font-size: 13px;
  letter-spacing: 4px;
  cursor: pointer;
  transition: background .2s, border-color .2s;
  margin-bottom: 8px;
}
#lb-overlay #lb-submit:hover:not(:disabled) {
  background: rgba(255,200,60,0.22);
  border-color: rgba(255,220,80,0.8);
}
#lb-overlay #lb-submit:disabled { opacity: 0.45; cursor: default; }
#lb-overlay #lb-msg {
  font-size: 11px;
  letter-spacing: 2px;
  min-height: 16px;
  color: rgba(120,220,80,0.9);
  text-align: center;
}
#lb-overlay .lb-restart {
  margin-top: 16px;
  font-size: 10px;
  letter-spacing: 3px;
  color: rgba(255,180,60,0.45);
  cursor: pointer;
  text-align: center;
}
#lb-overlay .lb-restart:hover { color: rgba(255,200,80,0.75); }
/* ── RIGHT: ranking table ── */
#lb-overlay .lb-right {
  flex: 1;
  display: flex;
  flex-direction: column;
}
#lb-overlay .lb-rank-title {
  font-size: 13px;
  letter-spacing: 5px;
  color: rgba(255,200,60,0.8);
  margin-bottom: 14px;
  text-align: center;
  text-transform: uppercase;
}
#lb-overlay .lb-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
#lb-overlay .lb-table th {
  font-size: 9px;
  letter-spacing: 3px;
  color: rgba(255,180,60,0.45);
  text-align: left;
  padding: 0 8px 8px;
  border-bottom: 1px solid rgba(255,200,60,0.12);
  text-transform: uppercase;
}
#lb-overlay .lb-table th:last-child { text-align: right; }
#lb-overlay .lb-table td {
  padding: 7px 8px;
  border-bottom: 1px solid rgba(255,200,60,0.06);
  color: rgba(255,220,160,0.85);
  letter-spacing: 1px;
}
#lb-overlay .lb-table td:last-child { text-align: right; }
#lb-overlay .lb-table tr:first-child td { color: #ffe040; font-weight: bold; }
#lb-overlay .lb-table tr:nth-child(2) td { color: #e0d0a0; }
#lb-overlay .lb-table tr:nth-child(3) td { color: #c8b888; }
#lb-overlay .lb-pos { color: rgba(255,180,60,0.5); font-size: 11px; }
#lb-overlay .lb-pos-1 { color: #ffe040; }
#lb-overlay .lb-pos-2 { color: #c0c0c0; }
#lb-overlay .lb-pos-3 { color: #cd7f32; }
#lb-overlay .lb-medal { font-size: 15px; }
#lb-overlay .lb-loading {
  text-align: center;
  color: rgba(255,180,60,0.4);
  font-size: 11px;
  letter-spacing: 3px;
  margin-top: 30px;
}
#lb-overlay .lb-my-row td { color: #7aff40 !important; }
</style>
</head>'''

# ── 2. Wrap canvas + add overlay HTML ───────────────────────────────────
canvas_line = '<canvas id="gameCanvas" width="900" height="500"></canvas>'
canvas_wrapped = '''<div id="game-wrap">
<canvas id="gameCanvas" width="900" height="500"></canvas>
<div id="lb-overlay">
  <div class="lb-inner">
    <div class="lb-left">
      <div class="lb-title">✦ PARABÉNS ✦</div>
      <div class="lb-score-big" id="lb-score-num">0</div>
      <div class="lb-score-label">PULOS TOTAIS</div>
      <div class="lb-stars" id="lb-stars-disp">★★★★★</div>
      <div class="lb-rating" id="lb-rating-disp">LENDÁRIO</div>
      <hr class="lb-sep">
      <div class="lb-ask">INSIRA SEU NOME</div>
      <input id="lb-name" type="text" maxlength="20" placeholder="seu nome aqui" autocomplete="off" spellcheck="false">
      <button id="lb-submit">✦ ENVIAR RECORDE ✦</button>
      <div id="lb-msg"></div>
      <div class="lb-restart" id="lb-restart-btn">↺ jogar novamente</div>
    </div>
    <div class="lb-right">
      <div class="lb-rank-title">🏆 TOP 10 — MENOS PULOS</div>
      <div id="lb-table-wrap"><div class="lb-loading">carregando...</div></div>
    </div>
  </div>
</div>
</div>'''

content = content.replace(canvas_line, canvas_wrapped)

# ── 3. Add Supabase CDN + CSS before </head> ──────────────────────────
content = content.replace('</head>', css_and_overlay)

# ── 4. Add Supabase JS logic before </script> at the very end ──────────
supabase_js = '''
// ═══════════════════════════════════════════════════════════════
//  SUPABASE LEADERBOARD
// ═══════════════════════════════════════════════════════════════
const SB_URL = 'https://axvxrjpiusgfaentcoik.supabase.co';
const SB_KEY = 'sb_publishable_XIwUjTwB9TdhuZKF6GhabQ_RGoVjnH-';
let sbClient = null;
try { sbClient = window.supabase.createClient(SB_URL, SB_KEY); } catch(e) {}

async function sbSubmit(username, jumps) {
  if (!sbClient) return false;
  const { error } = await sbClient.from('leaderboard').insert({ username: username.trim(), jumps });
  return !error;
}

async function sbLoadTop10() {
  if (!sbClient) return [];
  const { data } = await sbClient
    .from('leaderboard')
    .select('username, jumps')
    .order('jumps', { ascending: true })
    .limit(10);
  return data || [];
}

function renderLbTable(rows, myName, myJumps) {
  const wrap = document.getElementById('lb-table-wrap');
  if (!wrap) return;
  if (!rows.length) { wrap.innerHTML = '<div class="lb-loading">nenhum recorde ainda — seja o primeiro!</div>'; return; }
  const medals = ['🥇','🥈','🥉'];
  const ratingLabel = j =>
    j <= 500 ? 'LENDÁRIO' : j <= 800 ? 'MESTRE' : j <= 1200 ? 'HABILIDOSO' : j <= 2000 ? 'APRENDIZ' : 'SOBREVIVENTE';
  let rows_html = rows.map((r, i) => {
    const isMe = r.username === myName && r.jumps === myJumps;
    const medal = i < 3 ? `<span class="lb-medal">${medals[i]}</span>` : `<span class="lb-pos">#${i+1}</span>`;
    return `<tr class="${isMe ? 'lb-my-row' : ''}">
      <td>${medal}</td>
      <td>${r.username}</td>
      <td>${ratingLabel(r.jumps)}</td>
      <td><b>${r.jumps}</b> pulos</td>
    </tr>`;
  }).join('');
  wrap.innerHTML = `<table class="lb-table">
    <thead><tr><th>#</th><th>jogador</th><th>rank</th><th style="text-align:right">pulos</th></tr></thead>
    <tbody>${rows_html}</tbody>
  </table>`;
}

async function showLeaderboardOverlay(jumps) {
  const rating =
    jumps <= 500  ? ['LENDÁRIO',  '#ffe040'] :
    jumps <= 800  ? ['MESTRE',    '#00e8c8'] :
    jumps <= 1200 ? ['HABILIDOSO','#88aaff'] :
    jumps <= 2000 ? ['APRENDIZ',  '#ffb030'] :
                    ['SOBREVIVENTE','#cc4444'];
  const stars =
    jumps <= 500  ? '★★★★★' :
    jumps <= 800  ? '★★★★☆' :
    jumps <= 1200 ? '★★★☆☆' :
    jumps <= 2000 ? '★★☆☆☆' : '★☆☆☆☆';

  document.getElementById('lb-score-num').textContent = jumps;
  document.getElementById('lb-score-num').style.color = rating[1];
  document.getElementById('lb-stars-disp').textContent = stars;
  document.getElementById('lb-stars-disp').style.color = rating[1];
  document.getElementById('lb-rating-disp').textContent = rating[0];
  document.getElementById('lb-rating-disp').style.color = rating[1];
  document.getElementById('lb-msg').textContent = '';
  document.getElementById('lb-submit').disabled = false;
  document.getElementById('lb-name').value = localStorage.getItem('vgUsername') || '';
  document.getElementById('lb-overlay').style.display = 'block';

  // Load top 10 in background
  sbLoadTop10().then(rows => renderLbTable(rows, null, null));

  // Submit button
  const btn = document.getElementById('lb-submit');
  const oldBtn = btn.cloneNode(true);
  btn.parentNode.replaceChild(oldBtn, btn);
  document.getElementById('lb-submit').addEventListener('click', async () => {
    const nameInput = document.getElementById('lb-name');
    const name = nameInput.value.trim();
    if (!name) { document.getElementById('lb-msg').textContent = '⚠ digite seu nome!'; return; }
    document.getElementById('lb-submit').disabled = true;
    document.getElementById('lb-msg').textContent = 'enviando...';
    localStorage.setItem('vgUsername', name);
    const ok = await sbSubmit(name, jumps);
    if (ok) {
      document.getElementById('lb-msg').textContent = '✓ recorde enviado!';
      const rows = await sbLoadTop10();
      renderLbTable(rows, name, jumps);
    } else {
      document.getElementById('lb-msg').textContent = '✗ erro ao enviar — tente novamente';
      document.getElementById('lb-submit').disabled = false;
    }
  });

  // Restart button
  document.getElementById('lb-restart-btn').onclick = () => {
    document.getElementById('lb-overlay').style.display = 'none';
    restartGame();
  };
}

// ── Prevent key/click restart while overlay is open ────────────
function isLbOpen() {
  const el = document.getElementById('lb-overlay');
  return el && el.style.display !== 'none';
}
</script>
</body>
</html>'''

# ── 5. Replace </script></body></html> at the very end with supabase_js ──
# Find the last </script> just before </body></html>
last_script = content.rfind('</script>\n</body>\n</html>')
if last_script == -1:
    last_script = content.rfind('</script>')
    content = content[:last_script] + supabase_js
else:
    content = content[:last_script] + supabase_js

# ── 6. Patch keydown/click to skip restart when overlay is open ─────────
content = content.replace(
    'document.addEventListener(\'keydown\', e => {\n  if (gameFinished) { restartGame(); return; }',
    'document.addEventListener(\'keydown\', e => {\n  if (gameFinished && !isLbOpen()) { restartGame(); return; }'
)
content = content.replace(
    'canvas.addEventListener(\'click\', () => {\n  if (gameFinished) { restartGame(); return; }',
    'canvas.addEventListener(\'click\', () => {\n  if (gameFinished && !isLbOpen()) { restartGame(); return; }'
)

# ── 7. Patch gameFinished = true block to trigger overlay ───────────────
content = content.replace(
    '      gameFinished = true;\n      const best = parseInt(localStorage.getItem(\'vgBest\') || \'999999\');\n      if (jumpCount < best) localStorage.setItem(\'vgBest\', jumpCount);',
    '      gameFinished = true;\n      const best = parseInt(localStorage.getItem(\'vgBest\') || \'999999\');\n      if (jumpCount < best) localStorage.setItem(\'vgBest\', jumpCount);\n      setTimeout(() => showLeaderboardOverlay(jumpCount), 1200);'
)

with open(r'C:\Users\stree\Desktop\jogopulo\public\game.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done! Lines:', content.count('\n'))
# Verify patches
checks = [
    ('Supabase CDN', 'supabase.min.js'),
    ('lb-overlay div', 'lb-overlay'),
    ('sbSubmit function', 'async function sbSubmit'),
    ('showLeaderboardOverlay', 'showLeaderboardOverlay'),
    ('setTimeout trigger', 'setTimeout(() => showLeaderboardOverlay'),
    ('isLbOpen guard keydown', 'isLbOpen') ,
]
for name, pattern in checks:
    print(f'  {"OK" if pattern in content else "MISS"} — {name}')
