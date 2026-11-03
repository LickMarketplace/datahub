'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const { createPreviewServer } = require('../preview/server.cjs');
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright')); }
(async () => {
  const password = crypto.randomBytes(32).toString('base64url');
  const server = createPreviewServer({ htmlPath: process.argv[2], password });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', args: ['--no-sandbox'] });
  try {
    const context = await browser.newContext({ httpCredentials: { username: 'lick', password } });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(`http://127.0.0.1:${server.address().port}`);
    await page.locator('#nav [data-go="home"]').waitFor();
    assert.equal(await page.evaluate(() => ps().length), 0);
    await page.locator('#nav [data-go="catalogue"]').click();
    await page.getByRole('button', { name: 'Importer', exact: true }).click();
    await page.locator('#importFile').setInputFiles({ name: 'demo.csv', mimeType: 'text/csv', buffer: Buffer.from('reference;name\nDEMO-01;Produit de test') });
    await page.locator('#confirm').waitFor();
    await page.locator('#confirm').click();
    await page.locator('#rows').waitFor();
    assert.equal(await page.evaluate(() => ps().length), 1);
    assert.deepEqual(errors, []);
    console.log('PASS : accès authentifié à l’interface réelle, navigation et import CSV sous les règles de sécurité du serveur.');
    await context.close();
  } finally {
    await browser.close();
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
