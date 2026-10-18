import { open, shot } from './lib.mjs';
import fs from 'node:fs';

const { browser, page, api } = await open();
const out = {};
const inputsVal = async () => page.locator('input').evaluateAll(e => e.slice(0, 2).map(x => x.value));

async function settle(ms = 4500) { await page.waitForTimeout(ms); }
function grab(name) {
  const pick = (k) => api.filter(a => a.url.includes(k)).slice(-1)[0]?.body ?? null;
  out[name] = {
    overview: pick('/overview'), top: pick('/top-customers'),
    totalTbl: pick('/portfolio-health/customer-assignments'), statuses: pick('/portfolio-health/active-statuses'),
    periodTbl: pick('/clienteling-performance/assignments'), engagement: pick('/clienteling-performance/engagement'),
    composition: pick('/clienteling-performance/customer-composition'),
  };
}
async function preset(label) {
  api.length = 0;
  await page.getByText(label, { exact: true }).first().click();
  await settle();
}
async function custom(from, to) {
  for (let attempt = 0; attempt < 3; attempt++) {
    await page.getByText('Tháng này', { exact: true }).first().click();
    await page.waitForTimeout(2500);
    api.length = 0;
    const a = page.locator('input').nth(0);
    await a.click();
    await page.keyboard.press('Control+A'); await page.keyboard.type(from, { delay: 60 }); await page.keyboard.press('Enter');
    await page.waitForTimeout(400);
    await page.keyboard.press('Control+A'); await page.keyboard.type(to, { delay: 60 }); await page.keyboard.press('Enter');
    await settle(5500);
    const v = await inputsVal();
    if (v[0] === from && v[1] === to) return true;
    console.log('retry custom', from, to, JSON.stringify(v));
  }
  return false;
}
async function snap(name) {
  grab(name);
  out[name].toast = await page.locator('text=Không thể tải dữ liệu').count();
  out[name].inputs = await inputsVal();
  out[name].text = (await page.locator('main, body').first().innerText()).slice(0, 6000);
  await shot(page, name);
  console.log('snap', name, JSON.stringify(out[name].inputs), JSON.stringify(out[name].overview?.metrics), 'filters', JSON.stringify(out[name].overview?.filters), 'toast', out[name].toast);
}

grab('A_default'); out.A_default.inputs = await inputsVal(); out.A_default.text = (await page.locator('body').innerText()).slice(0, 6000); await shot(page, 'A_default');
await preset('Tháng trước'); await snap('B_thang_truoc');
await preset('Tuần này'); await snap('C_tuan_nay');
await preset('Năm nay'); await snap('D_nam_nay');
await custom('01/03/2026', '31/03/2026'); await snap('F_custom_thang3');
await custom('01/10/2026', '31/10/2026'); await snap('G_custom_future_end');
await custom('17/10/2026', '17/10/2026'); await snap('H_custom_1day_yesterday');
await custom('01/01/2020', '31/01/2020'); await snap('K_empty_period');
await custom('01/03/2025', '02/03/2026'); await snap('E_custom_367days');
await custom('01/03/2025', '01/03/2026'); await snap('E2_custom_366days');
await custom('01/03/2025', '30/09/2026'); await snap('E3_custom_579days');
await custom('01/09/2026', '30/09/2026'); await snap('M_sep');
await custom('30/09/2026', '30/09/2026'); await snap('N_30sep');
await preset('Tháng này'); await snap('Z_back_thang_nay');

fs.writeFileSync('scenarios_out.json', JSON.stringify(out, null, 1));
await browser.close();
