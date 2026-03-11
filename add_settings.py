"""
Adiciona ao game.html:
1. Suporte a pixel ratio (resolucao interna do canvas)
2. Botao de configuracoes (so mobile) com opcoes de resolucao e sair
"""

with open('public/game.html', 'r', encoding='utf-8') as f:
    c = f.read()

# ── 1. Pixel ratio logo apos W e H ───────────────────────────────────────────
OLD_WH = "const W = canvas.width;\nconst H = canvas.height;"
NEW_WH = (
    "const W = canvas.width;\n"
    "const H = canvas.height;\n"
    "let PIXEL_RATIO = parseFloat(localStorage.getItem('vgPixelRatio') || '1');\n"
    "function setResolution(pr) {\n"
    "  PIXEL_RATIO = pr;\n"
    "  canvas.width  = Math.round(W * pr);\n"
    "  canvas.height = Math.round(H * pr);\n"
    "  localStorage.setItem('vgPixelRatio', pr);\n"
    "}\n"
    "setResolution(PIXEL_RATIO); // aplica resolucao salva"
)
assert OLD_WH in c, "ERRO: bloco W/H nao encontrado"
c = c.replace(OLD_WH, NEW_WH, 1)
print("OK pixel ratio")

# ── 2. Aplica transform no inicio do loop ─────────────────────────────────────
OLD_LOOP_START = "  // Aplica screen shake\n  ctx.save();\n  ctx.translate(shakeX, shakeY);"
NEW_LOOP_START = (
    "  // Pixel ratio (resolucao)\n"
    "  ctx.setTransform(PIXEL_RATIO, 0, 0, PIXEL_RATIO, 0, 0);\n"
    "  // Aplica screen shake\n"
    "  ctx.save();\n"
    "  ctx.translate(shakeX, shakeY);"
)
assert OLD_LOOP_START in c, "ERRO: inicio do loop nao encontrado"
c = c.replace(OLD_LOOP_START, NEW_LOOP_START, 1)
print("OK transform no loop")

# ── 3. Corrige drawChromaticAberration para usar canvas.width/height ──────────
OLD_CHROMA = (
    "  ctx.drawImage(canvas, offset, 0, W, H, 0, 0, W, H);\n"
    "  // Blue channel shift\n"
    "  ctx.drawImage(canvas, -offset, 0, W, H, 0, 0, W, H);"
)
NEW_CHROMA = (
    "  ctx.drawImage(canvas, offset*PIXEL_RATIO, 0, canvas.width, canvas.height, 0, 0, W, H);\n"
    "  // Blue channel shift\n"
    "  ctx.drawImage(canvas, -offset*PIXEL_RATIO, 0, canvas.width, canvas.height, 0, 0, W, H);"
)
assert OLD_CHROMA in c, "ERRO: drawChromaticAberration nao encontrado"
c = c.replace(OLD_CHROMA, NEW_CHROMA, 1)
print("OK chromatic aberration")

# ── 4. Adiciona CSS e HTML do menu de configuracoes (antes do </script></body>) ─
SETTINGS_CSS = """
    /* Botao de configuracoes */
    #tc-settings-btn {
      position: fixed;
      top: 14px; left: 14px;
      width: 44px; height: 44px;
      border-radius: 50%;
      background: rgba(0,0,0,0.45);
      border: 1.5px solid rgba(255,255,255,0.2);
      color: rgba(255,255,255,0.6);
      font-size: 20px;
      display: none;
      align-items: center; justify-content: center;
      pointer-events: all;
      z-index: 9998;
      -webkit-tap-highlight-color: transparent;
      cursor: pointer;
    }
    @media (pointer: coarse) { #tc-settings-btn { display: flex; } }
    /* Overlay de configuracoes */
    #tc-settings-overlay {
      display: none;
      position: fixed; inset: 0;
      background: rgba(0,0,0,0.88);
      z-index: 10001;
      flex-direction: column;
      align-items: center; justify-content: center;
      gap: 18px;
      font-family: 'Georgia', serif;
    }
    #tc-settings-overlay.open { display: flex; }
    .tc-set-title {
      color: #7acc20; font-size: 18px; letter-spacing: 5px;
      text-transform: uppercase; margin-bottom: 6px;
    }
    .tc-set-group { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }
    .tc-set-res {
      padding: 10px 20px; border-radius: 10px;
      border: 1.5px solid rgba(255,255,255,0.25);
      background: rgba(255,255,255,0.07);
      color: rgba(255,255,255,0.75);
      font-family: 'Georgia', serif; font-size: 15px;
      -webkit-tap-highlight-color: transparent; cursor: pointer;
      transition: background 0.15s, border-color 0.15s;
    }
    .tc-set-res.active {
      border-color: #7acc20; color: #7acc20;
      background: rgba(122,204,32,0.12);
    }
    .tc-set-exit {
      margin-top: 10px; padding: 12px 36px; border-radius: 12px;
      border: 1.5px solid rgba(255,80,80,0.5);
      background: rgba(180,30,30,0.18);
      color: rgba(255,130,130,0.9);
      font-family: 'Georgia', serif; font-size: 15px; letter-spacing: 2px;
      -webkit-tap-highlight-color: transparent; cursor: pointer;
    }
    .tc-set-close {
      margin-top: 4px; padding: 10px 28px; border-radius: 10px;
      border: 1.5px solid rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.06);
      color: rgba(255,255,255,0.55);
      font-family: 'Georgia', serif; font-size: 14px;
      -webkit-tap-highlight-color: transparent; cursor: pointer;
    }"""

SETTINGS_JS = """
// ── Menu de configuracoes (mobile) ─────────────────────────────────────────
(function initSettings() {
  const styleEl = document.createElement('style');
  styleEl.textContent = `""" + SETTINGS_CSS + """`;
  document.head.appendChild(styleEl);

  const resOptions = [
    { label: '480p',  pr: 0.5  },
    { label: '720p',  pr: 1.0  },
    { label: '1080p', pr: 2.0  },
    { label: '4K',    pr: 3.0  },
  ];

  const resButtons = resOptions.map(o =>
    `<div class="tc-set-res${Math.abs(PIXEL_RATIO - o.pr) < 0.01 ? ' active' : ''}" data-pr="${o.pr}">${o.label}</div>`
  ).join('');

  const html = `
    <div id="tc-settings-btn">&#9881;</div>
    <div id="tc-settings-overlay">
      <div class="tc-set-title">&#9881; Configuracoes</div>
      <div class="tc-set-group" id="tc-res-group">${resButtons}</div>
      <div class="tc-set-exit" id="tc-exit-btn">&#x23FB; Sair do jogo</div>
      <div class="tc-set-close" id="tc-close-settings">&#x2715; Fechar</div>
    </div>`;
  document.body.insertAdjacentHTML('beforeend', html);

  const overlay = document.getElementById('tc-settings-overlay');

  document.getElementById('tc-settings-btn').addEventListener('touchstart', (e) => {
    e.preventDefault();
    overlay.classList.add('open');
    // Atualiza botao ativo
    document.querySelectorAll('.tc-set-res').forEach(btn => {
      btn.classList.toggle('active', Math.abs(parseFloat(btn.dataset.pr) - PIXEL_RATIO) < 0.01);
    });
  }, { passive: false });

  document.getElementById('tc-res-group').addEventListener('touchstart', (e) => {
    const btn = e.target.closest('.tc-set-res');
    if (!btn) return;
    e.preventDefault();
    const pr = parseFloat(btn.dataset.pr);
    setResolution(pr);
    document.querySelectorAll('.tc-set-res').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }, { passive: false });

  document.getElementById('tc-exit-btn').addEventListener('touchstart', (e) => {
    e.preventDefault();
    if (window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.App) {
      window.Capacitor.Plugins.App.exitApp();
    } else {
      window.close();
    }
  }, { passive: false });

  document.getElementById('tc-close-settings').addEventListener('touchstart', (e) => {
    e.preventDefault();
    overlay.classList.remove('open');
  }, { passive: false });
})();
"""

# Insere antes de </script></body>
OLD_END = "</script>\n</body>"
assert OLD_END in c, "ERRO: fim do script nao encontrado"
c = c.replace(OLD_END, SETTINGS_JS + "</script>\n</body>", 1)
print("OK menu configuracoes")

with open('public/game.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Pronto! Linhas:", c.count('\n'))
