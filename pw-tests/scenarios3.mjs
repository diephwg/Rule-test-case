import { open, shot } from './lib.mjs';
import fs from 'node:fs';

const { browser, page, api } = await open();
const out = {};
const sleep = (ms) => page.waitForTimeout(ms);
const T_TOTAL = 'Key customer metrics breakdown by CA — Total';
const T_PERIOD = 'Key customer metrics breakdown by CA — In selected period';
const T_TOP = 'Top 50 Customers Board';
const section = (title) => page.locator('div.ant-card, section, div').filter({ hasText: title }).filter({ has: page.locator('.ant-table') }).last();
async function rows(title, n = 100) {
  return section(title).locator('.ant-table-tbody tr.ant-table-row').evaluateAll((trs, n) => trs.slice(0, n).map(tr => [...tr.querySelectorAll('td')].map(td => td.innerText.trim().replace(/\s+/g, ' '))), n);
}
async function footer(title) {
  const t = await section(title).innerText();
  return t.split('\n').filter(l => /\/\s*\d+\s*hàng|Mỗi trang|^\d+\s*\/\s*\d+$/.test(l.trim())).map(l => l.trim()).join(' | ');
}
async function state(name, title) {
  const r = await rows(title);
  out[name] = { footer: await footer(title), n: r.length, first: r.slice(0, 5), all: r };
  await shot(page, name);
  console.log(name, out[name].footer, 'rows', r.length, JSON.stringify(r.slice(0, 2)));
}

// Top 50 full cell text (PIC col)
out.top_oct_rows = await rows(T_TOP);
console.log('TOP rows', JSON.stringify(out.top_oct_rows));
out.total_rows_default = await rows(T_TOTAL);
out.period_rows_default = await rows(T_PERIOD);
await state('U00_default_total', T_TOTAL);

// --- search by CA name
const sTotal = section(T_TOTAL).locator('input[placeholder^="Tìm theo"]');
await sTotal.fill('Huyền'); await sleep(1500); await state('U01_search_CA_total', T_TOTAL);
await sTotal.fill('Hermès'); await sleep(1500); await state('U02_search_store_total', T_TOTAL);
await sTotal.fill('zzzzqq'); await sleep(1500); await state('U03_search_empty_total', T_TOTAL);
out.U03_period_rows_after_total_search = await rows(T_PERIOD);
await sTotal.fill('Lê Mạnh'); await sleep(1500); await state('U04_search_page2_item', T_TOTAL);
await sTotal.fill(''); await sleep(1500);

// --- sorting by A7 (header click x2)
const hdr = (title, text) => section(title).locator('th').filter({ hasText: new RegExp('^' + text + '\\s*$') }).first();
await hdr(T_TOTAL, 'A7').click(); await sleep(800); await state('U05_sort_A7_asc1', T_TOTAL);
await hdr(T_TOTAL, 'A7').click(); await sleep(800); await state('U06_sort_A7_click2', T_TOTAL);
await hdr(T_TOTAL, 'A7').click(); await sleep(800); await state('U06b_sort_A7_click3', T_TOTAL);
// independent sort on the period table by contacted
await hdr(T_PERIOD, '# CONTACTED CUSTOMERS').click().catch(e => console.log('contacted hdr', e.message)); await sleep(800);
await state('U07_period_sort_contacted', T_PERIOD);
await state('U07b_total_after_period_sort', T_TOTAL);

// --- pagination
await page.reload(); await sleep(1500);
await page.getByText('Customer', { exact: true }).first().click(); await sleep(6000);
const ps = section(T_TOTAL).locator('.ant-select').first();
await ps.click(); await sleep(500);
out.pagesize_options = await page.locator('.ant-select-item-option').allInnerTexts();
console.log('page size options', JSON.stringify(out.pagesize_options));
for (const opt of out.pagesize_options) {
  await page.locator('.ant-select-item-option').filter({ hasText: opt }).first().click(); await sleep(1200);
  await state(`U08_pagesize_${opt.replace(/\W+/g, '_')}`, T_TOTAL);
  await section(T_TOTAL).locator('.ant-select').first().click(); await sleep(400);
}
await page.keyboard.press('Escape');
await section(T_TOTAL).locator('.ant-select').first().click(); await sleep(400);
await page.locator('.ant-select-item-option').filter({ hasText: '15' }).first().click(); await sleep(1000);
await section(T_TOTAL).locator('button', { hasText: '›' }).first().click(); await sleep(1000);
await state('U09_page2', T_TOTAL);
await sTotal.fill('Lê Mạnh'); await sleep(1500); await state('U10_search_from_page2', T_TOTAL);
await sTotal.fill('');

// --- 367 day message capture
await page.reload(); await sleep(1500);
await page.getByText('Customer', { exact: true }).first().click(); await sleep(6000);
const texts = [];
const watch = setInterval(async () => {
  try {
    const t = await page.locator('.ant-message, .ant-notification, [role=alert], [class*=toast], [class*=Toastify]').allInnerTexts();
    if (t.length) texts.push({ t: Date.now(), t2: t });
  } catch {}
}, 150);
api.length = 0;
const a = page.locator('input').nth(0);
await a.click();
await page.keyboard.press('Control+A'); await page.keyboard.type('01/03/2025', { delay: 60 }); await page.keyboard.press('Enter');
await sleep(400);
await page.keyboard.press('Control+A'); await page.keyboard.type('02/03/2026', { delay: 60 }); await page.keyboard.press('Enter');
await sleep(700); await shot(page, 'T367_after_0_7s');
await sleep(1500); await shot(page, 'T367_after_2_2s');
await sleep(3000);
clearInterval(watch);
out.t367 = { toasts: texts.map(x => x.t2).flat().filter((v, i, arr) => arr.indexOf(v) === i), inputs: await page.locator('input').evaluateAll(e => e.slice(0, 2).map(x => x.value)), calls: api.map(x => [x.url.split('dashboard/')[1], x.status, x.body?.message]) };
console.log('T367', JSON.stringify(out.t367));
await shot(page, 'T367_final');

fs.writeFileSync('scenarios3_out.json', JSON.stringify(out, null, 1));
await browser.close();
