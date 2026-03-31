"""
Adiciona zoom 1.5x para mobile no game.html:
1. Adiciona constantes ZOOM e VW
2. Corrige updateCamera() para usar VW
3. Reestrutura loop() para aplicar zoom só no mundo (não no HUD)
"""

with open('public/game.html', 'r', encoding='utf-8') as f:
    c = f.read()

# ── 1. Adiciona ZOOM e VW após W e H ──────────────────────────────────────────
OLD_WH = "const W = canvas.width;\nconst H = canvas.height;"
NEW_WH = (
    "const W = canvas.width;\n"
    "const H = canvas.height;\n"
    "// Zoom para mobile: elementos 1.5x maiores, câmera mostra menos mundo\n"
    "const ZOOM = (navigator.maxTouchPoints > 0 || window.innerWidth <= 900) ? 1.5 : 1.0;\n"
    "const VW = W / ZOOM; // largura visível do mundo por frame"
)
assert OLD_WH in c, "ERRO: bloco W/H não encontrado"
c = c.replace(OLD_WH, NEW_WH, 1)
print("OK ✓ ZOOM e VW adicionados")

# ── 2. Corrige updateCamera() ─────────────────────────────────────────────────
OLD_CAM = (
    "function updateCamera() {\n"
    "  const target = player.x - W/2 + player.w/2;\n"
    "  camX += (target - camX) * 0.1;\n"
    "  if (camX < 0) camX = 0;\n"
    "  if (camX > WORLD_W - W) camX = WORLD_W - W;\n"
    "}"
)
NEW_CAM = (
    "function updateCamera() {\n"
    "  const target = player.x - VW/2 + player.w/2;\n"
    "  camX += (target - camX) * 0.1;\n"
    "  if (camX < 0) camX = 0;\n"
    "  if (camX > WORLD_W - VW) camX = WORLD_W - VW;\n"
    "}"
)
assert OLD_CAM in c, "ERRO: updateCamera() não encontrado"
c = c.replace(OLD_CAM, NEW_CAM, 1)
print("OK ✓ updateCamera() corrigido para VW")

# ── 3. Reestrutura loop(): zoom só para o mundo, HUD sem zoom ─────────────────
OLD_LOOP = (
    "  ctx.save();\n"
    "  ctx.translate(shakeX, shakeY);\n"
    "\n"
    "  drawBG(); drawPlatforms();\n"
    "  drawTrail(); // Trail atrás do player\n"
    "  drawPlayer();\n"
    "  // for (const p of particles) p.draw(camX); // removido - bolinhas verdes\n"
    "  drawSpeedLines(); // Speed lines\n"
    "  drawDustParticles();\n"
    "  // drawLandingEffects(); // removido\n"
    "  drawPhaseFlash(); // Flash de transição de fase\n"
    "  if (!gameStarted) { drawStartScreen(); } else { drawHUD(); }\n"
    "\n"
    "  ctx.restore(); // Remove shake"
)
NEW_LOOP = (
    "  // ── Mundo (com zoom no mobile) ───────────────────────────\n"
    "  ctx.save();\n"
    "  ctx.translate(shakeX, shakeY);\n"
    "  if (ZOOM !== 1) ctx.scale(ZOOM, ZOOM);\n"
    "\n"
    "  drawBG(); drawPlatforms();\n"
    "  drawTrail(); // Trail atrás do player\n"
    "  drawPlayer();\n"
    "  // for (const p of particles) p.draw(camX); // removido - bolinhas verdes\n"
    "  drawSpeedLines(); // Speed lines\n"
    "  drawDustParticles();\n"
    "  // drawLandingEffects(); // removido\n"
    "\n"
    "  ctx.restore(); // Remove shake + zoom\n"
    "\n"
    "  // ── HUD e overlays (escala normal, sem zoom) ─────────────\n"
    "  drawPhaseFlash(); // Flash de transição de fase\n"
    "  if (!gameStarted) { drawStartScreen(); } else { drawHUD(); }"
)
assert OLD_LOOP in c, "ERRO: bloco loop() não encontrado"
c = c.replace(OLD_LOOP, NEW_LOOP, 1)
print("OK ✓ loop() reestruturado com zoom só no mundo")

with open('public/game.html', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"\nPronto! Linhas: {c.count(chr(10))}")
