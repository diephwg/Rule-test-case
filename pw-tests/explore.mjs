import { open } from './lib.mjs';
import fs from 'node:fs';

const { browser, page, api } = await open();
fs.writeFileSync('api_default.json', JSON.stringify(api.map(a => ({ url: a.url, status: a.status, body: a.body })), null, 1));

// store dropdown options
await page.locator('text=Tất cả Store').first().click();
await page.waitForTimeout(800);
console.log('--- STORE DROPDOWN ---');
console.log((await page.locator('[role=listbox], [role=option], .ant-select-dropdown, [class*=dropdown], [class*=menu]').allInnerTexts()).join('\n').slice(0, 1500));
await page.screenshot({ path: 'explore_store.png' });
await page.keyboard.press('Escape');

// date picker
await page.locator('input').nth(0).click().catch(() => {});
await page.waitForTimeout(800);
await page.screenshot({ path: 'explore_date.png' });
console.log('--- INPUTS ---');
const inputs = await page.locator('input').evaluateAll(els => els.map(e => ({ph: e.placeholder, v: e.value, type: e.type, ro: e.readOnly})));
console.log(JSON.stringify(inputs));
await browser.close();
