import { chromium } from '/Users/aryanmittal/BStackAutomation-new/percy/percy_playwright/node_modules/playwright/index.mjs';
const b = await chromium.launch();
const URL = 'https://aryanmittal-bs.github.io/percy-dynamic-text-ignore-test/';
for (let i = 0; i < 3; i++) {
  const ctx = await b.newContext();           // fresh context = no cache reuse
  const pg = await ctx.newPage();
  const errs = [];
  pg.on('pageerror', e => errs.push(String(e)));
  await pg.goto(URL + '?cb=' + Date.now(), { waitUntil: 'networkidle' });
  const r = await pg.evaluate(() => {
    const g = s => (document.querySelector(s) || {}).textContent;
    return {
      amount: g('[data-dyn="price"]'),
      invoice: g('.hero [data-dyn="custom"]'),
      issued: g('.hero [data-dyn="date"]'),
      email: g('.hero [data-dyn="email"]'),
      phone: g('.hero [data-dyn="phone"]'),
      search: document.querySelector('input[data-dyn="typed"]').getAttribute('value'),
      scriptPresent: !!document.querySelector('script'),
    };
  });
  console.log('load', i + 1, JSON.stringify(r));
  if (errs.length) console.log('   PAGE ERRORS:', errs);
  await ctx.close();
}
await b.close();
