with open('public/game.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Remove ZOOM e VW
OLD_WH = (
    "const W = canvas.width;\n"
    "const H = canvas.height;\n"
    "// Zoom para mobile: elementos 1.5x maiores, camara mostra menos mundo\n"
    "const ZOOM = (navigator.maxTouchPoints > 0 || window.innerWidth <= 900) ? 1.5 : 1.0;\n"
    "const VW = W / ZOOM; // largura visivel do mundo por frame"
)
NEW_WH = "const W = canvas.width;\nconst H = canvas.height;"
assert OLD_WH in c, "ERRO: bloco ZOOM nao encontrado"
c = c.replace(OLD_WH, NEW_WH, 1)
print("OK revertido ZOOM/VW")

# 2. Reverte updateCamera()
OLD_CAM = (
    "function updateCamera() {\n"
    "  const target = player.x - VW/2 + player.w/2;\n"
    "  camX += (target - camX) * 0.1;\n"
    "  if (camX < 0) camX = 0;\n"
    "  if (camX > WORLD_W - VW) camX = WORLD_W - VW;\n"
    "}"
)
NEW_CAM = (
    "function updateCamera() {\n"
    "  const target = player.x - W/2 + player.w/2;\n"
    "  camX += (target - camX) * 0.1;\n"
    "  if (camX < 0) camX = 0;\n"
    "  if (camX > WORLD_W - W) camX = WORLD_W - W;\n"
    "}"
)
assert OLD_CAM in c, "ERRO: updateCamera() com VW nao encontrado"
c = c.replace(OLD_CAM, NEW_CAM, 1)
print("OK revertido updateCamera()")

# 3. Reverte loop()
OLD_LOOP = (
    "  // -- Mundo (com zoom no mobile) -------------------------------------------\n"
    "  ctx.save();\n"
    "  ctx.translate(shakeX, shakeY);\n"
    "  if (ZOOM !== 1) ctx.scale(ZOOM, ZOOM);\n"
    "\n"
    "  drawBG(); drawPlatforms();\n"
    "  drawTrail(); // Trail atras do player\n"
    "  drawPlayer();\n"
    "  // for (const p of particles) p.draw(camX); // removido - bolinhas verdes\n"
    "  drawSpeedLines(); // Speed lines\n"
    "  drawDustParticles();\n"
    "  // drawLandingEffects(); // removido\n"
    "\n"
    "  ctx.restore(); // Remove shake + zoom\n"
    "\n"
    "  // -- HUD e overlays (escala normal, sem zoom) ----------------------------------------\n"
    "  drawPhaseFlash(); // Flash de transicao de fase\n"
    "  if (!gameStarted) { drawStartScreen(); } else { drawHUD(); }"
)
NEW_LOOP = (
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
assert OLD_LOOP in c, "ERRO: bloco loop() modificado nao encontrado"
c = c.replace(OLD_LOOP, NEW_LOOP, 1)
print("OK revertido loop()")

with open('public/game.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Pronto! Linhas:", c.count('\n'))
