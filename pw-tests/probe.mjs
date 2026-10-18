import { chromium } from '@playwright/test';

const browser = await chromium.launch({
  args: ['--disable-features=PrivateNetworkAccessSendPreflights,PrivateNetworkAccessRespectPreflightResults,BlockInsecurePrivateNetworkRequests,LocalNetworkAccessChecks,DnsOverHttps'],
});
const context = await browser.newContext({ storageState: 'auth.json', viewport: { width: 1440, height: 900 } });
const page = await context.newPage();
page.on('response', (r) => { if (r.url().includes('api-caapp')) console.log(r.status(), r.url().slice(0, 140)); });
page.on('requestfailed', (r) => { if (r.url().includes('api-caapp')) console.log('FAILED', r.failure()?.errorText, r.url().slice(0, 140)); });
await page.goto('https://ca-app.sts.vn/dashboard');
await page.getByText('Customer', { exact: true }).first().click();
await page.waitForTimeout(8000);
await page.screenshot({ path: 'probe.png', fullPage: true });
console.log((await page.locator('body').innerText()).slice(0, 1500));
await browser.close();
