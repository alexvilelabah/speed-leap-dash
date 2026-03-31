import { test } from '@playwright/test';
import fs from 'fs';
import path from 'path';

test('capture play store screenshots', async ({ page }) => {
  // Ensure the output directory exists
  const outputDir = path.join(process.cwd(), 'output_screenshots');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Common landscape viewport size for mobile games
  await page.setViewportSize({ width: 1920, height: 1080 });
  
  // Go to the local dev server
  await page.goto('http://localhost:8081/');

  // Wait to ensure everything is loaded (web fonts, assets, canvas)
  await page.waitForTimeout(3000);

  // Take screenshot 1: Main Menu / Early game
  await page.screenshot({ path: path.join(outputDir, '01_main_menu.png') });

  // Try to start the game (Space/Click typical triggers)
  await page.keyboard.press(' ');
  await page.mouse.click(1920 / 2, 1080 / 2);

  // Wait for some action
  await page.waitForTimeout(2500);

  // Take screenshot 2: Gameplay element
  await page.screenshot({ path: path.join(outputDir, '02_gameplay.png') });
  
  // Simulate jump
  await page.keyboard.press(' ');
  await page.mouse.click(1920 / 2, 1080 / 2);
  await page.waitForTimeout(2000);

  // Take screenshot 3: Jumping / Middle of game
  await page.screenshot({ path: path.join(outputDir, '03_mid_gameplay.png') });
  
  // Wait to see if we hit a leaderboard or game over
  await page.waitForTimeout(4000);
  await page.screenshot({ path: path.join(outputDir, '04_end_game_or_leaderboard.png') });

  console.log('Screenshots captured successfully in output_screenshots/ folder.');
});
