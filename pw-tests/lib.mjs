import { chromium } from '@playwright/test';
import fs from 'node:fs';

export const ARGS = ['--disable-features=PrivateNetworkAccessSendPreflights,PrivateNetworkAccessRespectPreflightResults,BlockInsecurePrivateNetworkRequests,LocalNetworkAccessChecks,DnsOverHttps'];

export async function open() {
  const browser = await chromium.launch({ args: ARGS });
  const context = await browser.newContext({ storageState: 'auth.json', viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();
  const api = [];
  page.on('response', async (r) => {
    if (!r.url().includes('api-caapp') || r.request().method() === 'OPTIONS') return;
    let body = null;
    try { body = await r.json(); } catch {}
    api.push({ url: r.url(), status: r.status(), body, t: Date.now() });
  });
  await page.goto('https://ca-app.sts.vn/dashboard');
  await page.getByText('Customer', { exact: true }).first().click();
  await page.waitForTimeout(6000);
  return { browser, context, page, api };
}

export function shot(page, name) {
  fs.mkdirSync('evidence', { recursive: true });
  return page.screenshot({ path: `evidence/${name}.png`, fullPage: true });
}
