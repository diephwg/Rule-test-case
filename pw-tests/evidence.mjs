import { chromium } from '@playwright/test';
import { ARGS } from './lib.mjs';
import fs from 'node:fs';

await new Promise(r => setTimeout(r, 60000));

const browser = await chromium.launch({ args: ARGS });
const context = await browser.newContext({ storageState: 'auth.json', viewport: { width: 1440, height: 1000 } });
const page = await context.newPage();
const api = [];
page.on('response', async (r) => {
  if (!r.url().includes('api-caapp') || r.request().method() === 'OPTIONS') return;
  let body = null; try { body = await r.json(); } catch {}
  api.push({ url: r.url(), status: r.status(), body });
});
const sleep = (ms) => page.waitForTimeout(ms);
fs.mkdirSync('evidence2', { recursive: true });
const out = {};
const T_TOTAL = 'Key customer metrics breakdown by CA — Total';
const T_PERIOD = 'Key customer metrics breakdown by CA — In selected period';
const T_TOP = 'Top 50 Customers Board';
const section = (title) => page.locator('div').filter({ hasText: title }).filter({ has: page.locator('.ant-table') }).last();

async function act(fn, settle = 4500) {
  for (let i = 0; i < 4; i++) {
    api.length = 0;
    await fn();
    await sleep(settle);
    if (!api.some(a => a.status === 429)) return true;
    console.log('429 cooling'); await sleep(50000);
  }
  return false;
}
async function regions(key) {
  // filter + funnel region
  const top = await section(T_TOP).boundingBox();
  const filt = await page.getByText('KỲ XEM', { exact: true }).first().boundingBox();
  const y0 = Math.max(0, filt.y - 30), y1 = top.y - 6;
  await page.screenshot({ path: `evidence2/${key}__funnel.png`, fullPage: true, clip: { x: 250, y: y0 + await page.evaluate(() => window.scrollY), width: 1180, height: y1 - y0 } }).catch(async () => {});
  await section(T_TOP).screenshot({ path: `evidence2/${key}__top.png` });
  await section(T_TOTAL).screenshot({ path: `evidence2/${key}__total.png` });
  await section(T_PERIOD).screenshot({ path: `evidence2/${key}__period.png` });
}
async function funnelShot(key) {
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  await page.evaluate(() => window.scrollTo(0, 0));
  const top = await section(T_TOP).boundingBox();
  await page.screenshot({ path: `evidence2/${key}__funnel.png`, clip: { x: 250, y: 90, width: 1180, height: Math.min(top.y + await page.evaluate(() => window.scrollY) - 90, 800) } });
}
async function snap(key) {
  await page.evaluate(() => window.scrollTo(0, 0));
  const pick = (k) => api.filter(a => a.url.includes(k)).slice(-1)[0]?.body ?? null;
  out[key] = { inputs: await page.locator('input').evaluateAll(e => e.slice(0, 2).map(x => x.value)), overview: pick('/overview') };
  await funnelShot(key);
  await section(T_TOP).screenshot({ path: `evidence2/${key}__top.png` });
  await section(T_TOTAL).screenshot({ path: `evidence2/${key}__total.png` });
  await section(T_PERIOD).screenshot({ path: `evidence2/${key}__period.png` });
  console.log('snap', key, JSON.stringify(out[key].inputs), JSON.stringify(out[key].overview?.metrics));
}
async function preset(label) { await act(() => page.getByText(label, { exact: true }).first().click()); }
async function custom(from, to) {
  for (let t = 0; t < 3; t++) {
    await act(() => page.getByText('Tháng này', { exact: true }).first().click(), 3500);
    const ok = await act(async () => {
      await page.locator('input').nth(0).click();
      await page.keyboard.press('Control+A'); await page.keyboard.type(from, { delay: 60 }); await page.keyboard.press('Enter');
      await sleep(400);
      await page.keyboard.press('Control+A'); await page.keyboard.type(to, { delay: 60 }); await page.keyboard.press('Enter');
    }, 5500);
    const v = await page.locator('input').evaluateAll(e => e.slice(0, 2).map(x => x.value));
    if (ok && v[0] === from && v[1] === to) return true;
  }
  return false;
}
const storeSel = () => page.locator('.ant-select').filter({ hasText: /Store|Boss|Hermès/ }).last();
async function pickStore(name) {
  await act(async () => {
    await storeSel().click(); await sleep(400);
    await page.locator('.ant-select-item-option').filter({ hasText: name }).first().click(); await sleep(300);
    await page.keyboard.press('Escape');
  });
}

await page.goto('https://ca-app.sts.vn/dashboard');
await page.getByText('Customer', { exact: true }).first().click();
await sleep(9000);
await snap('E01_thang_nay_all');
await preset('Tháng trước'); await snap('E02_thang_truoc');
await preset('Tuần này'); await snap('E03_tuan_nay');
await preset('Năm nay'); await snap('E04_nam_nay');
await custom('01/03/2026', '31/03/2026'); await snap('E05_custom_thang3_2026');
await custom('01/10/2026', '31/10/2026'); await snap('E06_custom_den_31_10_tuong_lai');
await custom('30/09/2026', '30/09/2026'); await snap('E07_custom_1_ngay_30_09');
await custom('01/01/2020', '31/01/2020'); await snap('E08_ky_rong_2020');
await custom('01/03/2025', '01/03/2026'); await snap('E10_custom_366_ngay');
await preset('Tháng này');

// store scenarios in Oct then Sep
await pickStore('Tất cả Store'); // ensure state known (may toggle)
await sleep(2000);
const tag = async () => (await storeSel().innerText()).replace(/\s+/g, ' ');
console.log('tag now', await tag());
if (/Tất cả/.test(await tag())) { await pickStore('Boss 46'); } else { await pickStore('Boss 46'); }
console.log('tag after boss', await tag());
await snap('E11_boss_only_oct');
await preset('Tháng trước'); await snap('E13_boss_only_sep');
await preset('Tháng này');
await pickStore('Boss 46'); // toggle off boss -> maybe falls back to all
console.log('tag after toggle', await tag());
await pickStore('Hermès'); console.log('tag after hermes', await tag());
await snap('E12_hermes_only_oct');

fs.writeFileSync('evidence_out.json', JSON.stringify(out, null, 1));
await browser.close();
