import { chromium } from '@playwright/test';
import { ARGS } from './lib.mjs';
import fs from 'node:fs';

await new Promise(r => setTimeout(r, 20000));
const browser = await chromium.launch({ args: ARGS });
const context = await browser.newContext({ storageState: 'auth.json', viewport: { width: 2200, height: 1200 } });
const page = await context.newPage();
const api = [];
page.on('response', async (r) => { if (r.url().includes('api-caapp') && r.request().method() !== 'OPTIONS') api.push({ s: r.status() }); });
const sleep = (ms) => page.waitForTimeout(ms);
const T_TOTAL = 'Key customer metrics breakdown by CA — Total';
const T_PERIOD = 'Key customer metrics breakdown by CA — In selected period';
const T_TOP = 'Top 50 Customers Board';
const section = (title) => page.locator('div').filter({ hasText: title }).filter({ has: page.locator('.ant-table') }).last();
async function act(fn, settle = 5000) {
  for (let i = 0; i < 4; i++) { api.length = 0; await fn(); await sleep(settle); if (!api.some(a => a.s === 429)) return; await sleep(50000); }
}
async function snap(key) {
  for (const [name, title] of [['top', T_TOP], ['total', T_TOTAL], ['period', T_PERIOD]]) {
    await section(title).scrollIntoViewIfNeeded();
    await section(title).screenshot({ path: `evidence2/${key}__wide_${name}.png` });
  }
  console.log('wide', key);
}
await page.goto('https://ca-app.sts.vn/dashboard');
await page.getByText('Customer', { exact: true }).first().click();
await sleep(9000);
await snap('E01');
await act(() => page.getByText('Tháng trước', { exact: true }).first().click());
await snap('E02');
await act(() => page.getByText('Năm nay', { exact: true }).first().click());
await snap('E04');
await act(() => page.getByText('Tháng này', { exact: true }).first().click());
// store dropdown evidence
await page.evaluate(() => window.scrollTo(0, 0));
await page.locator('.ant-select').filter({ hasText: /Store|Boss|Hermès/ }).last().click(); await sleep(700);
await page.screenshot({ path: 'evidence2/DROPDOWN_stores.png', clip: { x: 0, y: 80, width: 2200, height: 560 } });
await page.keyboard.press('Escape');
await browser.close();
