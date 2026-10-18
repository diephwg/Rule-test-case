import { chromium } from '@playwright/test';
import { ARGS, shot } from './lib.mjs';
import fs from 'node:fs';

await new Promise(r => setTimeout(r, 75000)); // let rate limit reset

const browser = await chromium.launch({ args: ARGS });
const context = await browser.newContext({ storageState: 'auth.json', viewport: { width: 1440, height: 900 } });
const page = await context.newPage();
const api = [];
page.on('response', async (r) => {
  if (!r.url().includes('api-caapp') || r.request().method() === 'OPTIONS') return;
  let body = null; try { body = await r.json(); } catch {}
  api.push({ url: r.url(), status: r.status(), body });
});
const out = {};
const sleep = (ms) => page.waitForTimeout(ms);
const T_TOTAL = 'Key customer metrics breakdown by CA — Total';
const T_PERIOD = 'Key customer metrics breakdown by CA — In selected period';
const section = (title) => page.locator('div').filter({ hasText: title }).filter({ has: page.locator('.ant-table') }).last();
async function rows(title) {
  return section(title).locator('.ant-table-tbody tr.ant-table-row').evaluateAll(trs => trs.map(tr => [...tr.querySelectorAll('td')].map(td => td.innerText.trim().replace(/\s+/g, ' '))));
}
async function footer(title) {
  const t = await section(title).innerText();
  return t.split('\n').filter(l => /\/\s*\d+\s*hàng|^\d+\s*\/\s*\d+$/.test(l.trim())).map(l => l.trim()).join(' | ');
}
// run an action, wait until API quiet, retry if rate limited
async function act(fn, { settle = 3500 } = {}) {
  for (let i = 0; i < 4; i++) {
    api.length = 0;
    await fn();
    await sleep(settle);
    if (!api.some(a => a.status === 429)) return true;
    console.log('429 -> cooling 45s');
    await sleep(45000);
  }
  return false;
}
async function state(name, title) {
  const r = await rows(title);
  out[name] = { footer: await footer(title), n: r.length, all: r, calls: api.map(a => a.url.split('dashboard/')[1] + ' ' + a.status) };
  await shot(page, name);
  console.log(name, '|', out[name].footer, '| rows', r.length, JSON.stringify(r.slice(0, 3).map(x => x.slice(0, 3))), '| calls', out[name].calls.join(','));
}

await page.goto('https://ca-app.sts.vn/dashboard');
await page.getByText('Customer', { exact: true }).first().click();
await sleep(8000);
await state('V00_default', T_TOTAL);

const sTotal = section(T_TOTAL).locator('input[placeholder^="Tìm theo"]');
await act(() => sTotal.fill('Huyền')); await state('V01_search_CA_Huyen', T_TOTAL);
await act(() => sTotal.fill('Hermès')); await state('V02_search_store_Hermes', T_TOTAL);
await act(() => sTotal.fill('zzzzqq')); await state('V03_search_empty', T_TOTAL);
out.V03_period_after = { footer: await footer(T_PERIOD), rows: await rows(T_PERIOD) };
await act(() => sTotal.fill('Lê Mạnh')); await state('V04_search_LeManh_page2item', T_TOTAL);
await act(() => sTotal.fill('')); await state('V05_search_cleared', T_TOTAL);

const hdr = (title, text) => section(title).locator('th').filter({ hasText: new RegExp('^' + text + '\\s*$') }).first();
await act(() => hdr(T_TOTAL, 'A7').click(), { settle: 5000 }); await state('V06_sort_A7_click1', T_TOTAL);
await act(() => hdr(T_TOTAL, 'A7').click(), { settle: 5000 }); await state('V07_sort_A7_click2', T_TOTAL);
await act(() => hdr(T_PERIOD, '# CONTACTED CUSTOMERS').click(), { settle: 5000 }); await state('V08_period_sort_contacted', T_PERIOD);
await state('V08b_total_unchanged_after_period_sort', T_TOTAL);

fs.writeFileSync('scenarios4_out.json', JSON.stringify(out, null, 1));
await browser.close();
