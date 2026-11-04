'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright')); }
const html = fs.readFileSync(process.argv[2]);
const server = http.createServer((req, res) => {
  if (req.url !== '/') { res.writeHead(404).end(); return; }
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.end(html);
});
(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1050 }, locale: 'fr-FR' });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('http://127.0.0.1:' + server.address().port);
    await page.locator('#nav [data-go="home"]').waitFor();
    assert.equal(await page.evaluate(() => ps().length), 6);
    assert.equal(await page.evaluate(() => seed.demo), true);
    assert.match(await page.locator('header .tag').innerText(), /fictives/);
    await page.waitForFunction(() => document.querySelector('.identity img').naturalWidth > 0);
    await page.screenshot({ path: '/tmp/LICK_Maquette_Accueil.png' });
    for (const name of ['catalogue', 'documents', 'marketplaces', 'rules']) {
      await page.locator('#nav [data-go="' + name + '"]').click();
      await page.locator('h1').waitFor();
    }
    await page.locator('#nav [data-go="marketplaces"]').click();
    assert.match(await page.locator('#main').innerText(), /Modèle fictif/);
    assert.equal(await page.evaluate(() => { try { auditChannel(); return false; } catch (e) { return /fictif/.test(e.message); } }), true);
    await page.locator('#nav [data-go="catalogue"]').click();
    await page.locator('#search').fill('DEMO-A001');
    await page.locator('[data-open="DEMO-A001"]').click();
    await page.locator('#editTitle').fill('Casque audio — titre relu');
    await page.locator('#editDescription').fill('Description rédigée pour tester la maquette.');
    await page.locator('#approve').click();
    await page.locator('#modal').waitFor({ state: 'hidden' });
    await page.waitForFunction(() => approvals.has('DEMO-A001'));
    await page.reload();
    await page.waitForFunction(() => typeof approvals !== 'undefined' && approvals.has('DEMO-A001'));
    assert.equal(await page.evaluate(() => approvals.get('DEMO-A001').title), 'Casque audio — titre relu');
    await page.locator('#nav [data-go="catalogue"]').click();
    await page.getByRole('button', { name: '↑ Nouvelle version' }).click();
    await page.locator('#importFile').setInputFiles({ name: 'mon-catalogue.csv', mimeType: 'text/csv', buffer: Buffer.from('reference;name;brand\nTEST-001;Mon article;Ma marque') });
    await page.locator('#confirm').click();
    await page.locator('#rows').waitFor();
    assert.equal(await page.evaluate(() => ps().length), 1);
    assert.match(await page.locator('header .tag').innerText(), /importé/);
    await page.setViewportSize({ width: 390, height: 844 });
    await page.locator('#nav [data-go="home"]').click();
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    assert.deepEqual(errors, []);
    console.log('PASS : cinq espaces navigables, six articles fictifs, logo, recherche, édition et validation persistante, import personnel, blocage des modèles fictifs et affichage mobile.');
  } finally {
    await browser.close();
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); server.close(); process.exitCode = 1; });
