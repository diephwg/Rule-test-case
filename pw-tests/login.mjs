import { chromium } from '@playwright/test';

const browser = await chromium.launch({
  headless: false,
  args: ['--disable-features=PrivateNetworkAccessSendPreflights,PrivateNetworkAccessRespectPreflightResults,BlockInsecurePrivateNetworkRequests,LocalNetworkAccessChecks,DnsOverHttps'],
});
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await context.newPage();
await page.goto('https://ca-app.sts.vn/dashboard');
console.log('Dang nhap trong cua so vua mo. Script tu luu phien moi 3 giay; dong cua so khi xong.');

let closed = false;
browser.on('disconnected', () => { closed = true; });
while (!closed) {
  await new Promise((r) => setTimeout(r, 3000));
  try { await context.storageState({ path: 'auth.json' }); } catch {}
}
console.log('Da luu auth.json');
