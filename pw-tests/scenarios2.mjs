import { open, shot } from './lib.mjs';
import fs from 'node:fs';

const { browser, page, api } = await open();
const out = {};
const sleep = (ms) => page.waitForTimeout(ms);
const inputsVal = async () => page.locator('input').evaluateAll(e => e.slice(0, 2).map(x => x.value));

function grab(name) {
  const pick = (k) => api.filter(a => a.url.includes(k)).slice(-1)[0]?.body ?? null;
  out[name] = {
    overview: pick('/overview'), top: pick('/top-customers'),
    totalTbl: pick('/portfolio-health/customer-assignments'), statuses: pick('/portfolio-health/active-statuses'),
    periodTbl: pick('/clienteling-performance/assignments'), engagement: pick('/clienteling-performance/engagement'),
    composition: pick('/clienteling-performance/customer-composition'),
  };
}
async function preset(label) { api.length = 0; await page.getByText(label, { exact: true }).first().click(); await sleep(4500); }
const section = (title) => page.locator('div').filter({ hasText: title }).filter({ has: page.locator('.ant-table') }).last();
async function rowsOf(title) {
  const sec = section(title);
  return sec.locator('.ant-table-tbody tr.ant-table-row').evaluateAll(trs => trs.map(tr => [...tr.querySelectorAll('td')].map(td => td.innerText.trim().replace(/\s+/g, ' '))));
}
async function footerOf(title) {
  const sec = section(title);
  return (await sec.innerText()).split('\n').filter(l => /hàng|Mỗi trang/.test(l)).join(' | ');
}
async function storeSelect() {
  const sel = page.locator('.ant-select').filter({ hasText: /Store|Boss|Hermès/ }).last();
  return sel;
}
async function setStores(names) {
  api.length = 0;
  const sel = await storeSelect();
  await sel.click(); await sleep(500);
  for (const n of names) { await page.locator('.ant-select-item-option').filter({ hasText: n }).first().click(); await sleep(400); }
  await page.keyboard.press('Escape'); await sleep(4500);
  return (await sel.innerText()).replace(/\s+/g, ' ');
}
async function snap(name, extra = {}) {
  grab(name);
  out[name].inputs = await inputsVal();
  out[name].tags = (await (await storeSelect()).innerText()).replace(/\s+/g, ' ');
  Object.assign(out[name], extra);
  await shot(page, name);
  console.log('snap', name, JSON.stringify(out[name].inputs), out[name].tags, JSON.stringify(out[name].overview?.metrics), 'top', out[name].top?.data?.length);
}

const T_TOTAL = 'Key customer metrics breakdown by CA — Total';
const T_PERIOD = 'Key customer metrics breakdown by CA — In selected period';
const T_TOP = 'Top 50 Customers Board';

// ---- store scenarios
for (const [pLabel, pKey] of [['Tháng này', 'oct'], ['Tháng trước', 'sep'], ['Năm nay', 'year']]) {
  await preset(pLabel);
  out[`rows_top_${pKey}`] = await rowsOf(T_TOP);
  for (const [sKey, names] of [['boss', ['Boss 46']], ['hermes', ['Hermès']]]) {
    // reset to all first
    await (await storeSelect()).click(); await sleep(400);
    await page.locator('.ant-select-item-option').filter({ hasText: 'Tất cả Store' }).first().click(); await sleep(400);
    await page.keyboard.press('Escape'); await sleep(3000);
    const tags = await setStores(names);
    await snap(`S_${pKey}_${sKey}`, { tagsAfter: tags, rowsTop: await rowsOf(T_TOP), rowsTotal: await rowsOf(T_TOTAL), rowsPeriod: await rowsOf(T_PERIOD) });
  }
  // both explicit
  const tags = await setStores(['Boss 46', 'Hermès']);
  await snap(`S_${pKey}_both`, { tagsAfter: tags, rowsTop: await rowsOf(T_TOP), rowsTotal: await rowsOf(T_TOTAL), rowsPeriod: await rowsOf(T_PERIOD) });
  // back to all
  await (await storeSelect()).click(); await sleep(400);
  await page.locator('.ant-select-item-option').filter({ hasText: 'Tất cả Store' }).first().click(); await sleep(400);
  await page.keyboard.press('Escape'); await sleep(3500);
}

fs.writeFileSync('scenarios2_out.json', JSON.stringify(out, null, 1));
await browser.close();
