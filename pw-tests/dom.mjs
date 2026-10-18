import { open } from './lib.mjs';
const { browser, page } = await open();
const info = await page.evaluate(() => {
  const q = (s) => [...document.querySelectorAll(s)];
  return {
    tables: q('table').length,
    roleTables: q('[role=table], [role=grid]').length,
    searchInputs: q('input').map(i => ({ ph: i.placeholder, type: i.type, cls: i.className.slice(0, 40) })),
    selects: q('select').length,
    pageSizeCandidates: q('*').filter(e => e.children.length === 0 && /^Mỗi trang$/.test(e.textContent.trim())).length,
    headers: q('th').map(t => t.textContent.trim()).slice(0, 60),
    buttons: q('button').map(b => (b.textContent || b.getAttribute('aria-label') || '').trim()).filter(Boolean).slice(0, 60),
  };
});
console.log(JSON.stringify(info, null, 1));
const tt = await page.locator('table').first().innerText();
console.log('--- first table text ---\n' + tt.slice(0, 1500));
await browser.close();
