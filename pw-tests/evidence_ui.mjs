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
const out = {};
const T_TOTAL = 'Key customer metrics breakdown by CA — Total';
const T_PERIOD = 'Key customer metrics breakdown by CA — In selected period';
const section = (title) => page.locator('div').filter({ hasText: title }).filter({ has: page.locator('.ant-table') }).last();
async function act(fn, settle = 4500) {
  for (let i = 0; i < 4; i++) {
    api.length = 0; await fn(); await sleep(settle);
    if (!api.some(a => a.status === 429)) return true;
    console.log('429 cooling'); await sleep(50000);
  }
  return false;
}
async function rows(title) {
  return section(title).locator('.ant-table-tbody tr.ant-table-row').evaluateAll(trs => trs.map(tr => [...tr.querySelectorAll('td')].map(td => td.innerText.trim().replace(/\s+/g, ' '))));
}
async function foot(title) {
  return (await section(title).innerText()).split('\n').filter(l => /\/\s*\d+\s*hàng/.test(l)).join(' ');
}
async function shotSec(key, title) {
  await section(title).scrollIntoViewIfNeeded();
  await section(title).screenshot({ path: `evidence2/${key}.png` });
  out[key] = { footer: await foot(title), rows: await rows(title) };
  console.log(key, '|', out[key].footer, '| rows', out[key].rows.length, JSON.stringify(out[key].rows.slice(0, 2).map(r => r.slice(0, 4))));
}

await page.goto('https://ca-app.sts.vn/dashboard');
await page.getByText('Customer', { exact: true }).first().click();
await sleep(9000);

const sTotal = () => section(T_TOTAL).locator('input[placeholder^="Tìm theo"]');
await shotSec('U00_total_default', T_TOTAL);
await act(() => sTotal().fill('Huyền')); await shotSec('U01_search_CA_Huyen', T_TOTAL);
await act(() => sTotal().fill('Hermès')); await shotSec('U02_search_store_Hermes', T_TOTAL);
await act(() => sTotal().fill('zzzzqq')); await shotSec('U03_search_khong_ket_qua', T_TOTAL);
await shotSec('U03b_period_unchanged_khi_tim_total', T_PERIOD);
await act(() => sTotal().fill(''));
const hdr = (title, text) => section(title).locator('th').filter({ hasText: new RegExp('^' + text + '\\s*$') }).first();
await act(() => hdr(T_TOTAL, 'A7').click(), 6000); await shotSec('U04_sort_A7_lan1', T_TOTAL);
await act(() => hdr(T_TOTAL, 'A7').click(), 6000); await shotSec('U05_sort_A7_lan2', T_TOTAL);
await act(() => hdr(T_PERIOD, '# CONTACTED CUSTOMERS').click(), 6000); await shotSec('U06_period_sort_contacted', T_PERIOD);
await shotSec('U06b_total_van_giu_sort_A7', T_TOTAL);

// reload for pagination
await page.reload(); await sleep(2000);
await page.getByText('Customer', { exact: true }).first().click(); await sleep(9000);
const pageSize = () => section(T_TOTAL).locator('.ant-select').first();
await act(async () => { await pageSize().click(); await sleep(400); await page.locator('.ant-select-item-option').filter({ hasText: '30' }).first().click(); }, 3000);
await shotSec('U07_pagesize_30', T_TOTAL);
await act(async () => { await pageSize().click(); await sleep(400); await page.locator('.ant-select-item-option').filter({ hasText: '50' }).first().click(); }, 3000);
await shotSec('U08_pagesize_50', T_TOTAL);
await act(async () => { await pageSize().click(); await sleep(400); await page.locator('.ant-select-item-option').filter({ hasText: '15' }).first().click(); }, 3000);
await act(() => section(T_TOTAL).locator('button', { hasText: '›' }).first().click(), 3500);
await shotSec('U09_trang_2', T_TOTAL);

// 367-day attempt with toast capture
await page.reload(); await sleep(2000);
await page.getByText('Customer', { exact: true }).first().click(); await sleep(9000);
const toasts = [];
const iv = setInterval(async () => { try { const t = await page.locator('.ant-message, .ant-notification, [role=alert], [class*=toast], [class*=Toastify]').allInnerTexts(); t.filter(Boolean).forEach(x => toasts.push(x)); } catch {} }, 150);
api.length = 0;
await page.locator('input').nth(0).click();
await page.keyboard.press('Control+A'); await page.keyboard.type('01/03/2025', { delay: 60 }); await page.keyboard.press('Enter');
await sleep(400);
await page.keyboard.press('Control+A'); await page.keyboard.type('02/03/2026', { delay: 60 }); await page.keyboard.press('Enter');
await sleep(600); await page.screenshot({ path: 'evidence2/T367_a_sau_0_6s.png' });
await sleep(1400); await page.screenshot({ path: 'evidence2/T367_b_sau_2s.png' });
await sleep(4000); clearInterval(iv);
await page.evaluate(() => window.scrollTo(0, 0));
await page.screenshot({ path: 'evidence2/T367_c_sau_6s.png' });
out.t367 = { toasts: [...new Set(toasts)], inputs: await page.locator('input').evaluateAll(e => e.slice(0, 2).map(x => x.value)), calls: api.map(a => [a.url.split('dashboard/')[1], a.status, a.body?.message]), presetActive: await page.locator('button').evaluateAll(bs => bs.filter(b => /Tháng|Tuần|Năm/.test(b.innerText)).map(b => b.innerText + ':' + b.className.slice(-30))) };
console.log('T367', JSON.stringify(out.t367));

// Business tab for 002-06
await page.goto('https://ca-app.sts.vn/dashboard'); await sleep(5000);
await page.getByText('Month', { exact: true }).first().click(); await sleep(5000);
await page.screenshot({ path: 'evidence2/B_business_month.png', fullPage: true });
out.business = (await page.locator('body').innerText()).slice(0, 2500);
fs.writeFileSync('evidence_ui_out.json', JSON.stringify(out, null, 1));
await browser.close();
