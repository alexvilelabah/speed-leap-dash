import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

async function main() {
  const outputDir = path.join(process.cwd(), 'output_screenshots');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();
  
  try {
    await page.goto('http://localhost:8081/');
    await page.waitForTimeout(3000);

  await page.screenshot({ path: path.join(outputDir, '01_main_menu.png') });

  // Simulate space to start
  await page.keyboard.press(' ');
  await page.mouse.click(1920 / 2, 1080 / 2);

  await page.waitForTimeout(2500);
  await page.screenshot({ path: path.join(outputDir, '02_gameplay.png') });
  
  await page.keyboard.press(' ');
  await page.mouse.click(1920 / 2, 1080 / 2);
  await page.waitForTimeout(2000);

  await page.screenshot({ path: path.join(outputDir, '03_mid_gameplay.png') });
  
  await page.waitForTimeout(4000);
  await page.screenshot({ path: path.join(outputDir, '04_end_game_or_leaderboard.png') });

  } catch (error) {
    console.error('An error occurred during screenshot generation:', error);
  } finally {
    console.log('Screenshots captured successfully in output_screenshots/ folder.');
    await browser.close();
  }
}

main().catch(console.error);
