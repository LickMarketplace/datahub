'use strict';
const { createPreviewServer } = require('../preview/server.cjs');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');

(async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lick-preview-'));
  const html = '<!doctype html><html lang="fr"><body>Catalogue privé de test</body></html>';
  const htmlPath = path.join(dir, 'index.html');
  fs.writeFileSync(htmlPath, html);
  assert.throws(() => createPreviewServer({ htmlPath, password: '' }), /16 caractères/);
  const password = crypto.randomBytes(32).toString('base64url');
  const server = createPreviewServer({ htmlPath, password });
  try {
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}`;
    let response = await fetch(base);
    assert.equal(response.status, 401);
    assert.ok(!((await response.text()).includes('Catalogue privé de test')));
    assert.match(response.headers.get('www-authenticate'), /^Basic /);
    response = await fetch(base, { headers: { Authorization: 'Basic ' + Buffer.from('lick:incorrect').toString('base64') } });
    assert.equal(response.status, 401);
    const authorization = 'Basic ' + Buffer.from('lick:' + password).toString('base64');
    response = await fetch(base, { headers: { Authorization: authorization, 'Accept-Encoding': 'gzip' } });
    assert.equal(response.status, 200);
    assert.equal(await response.text(), html);
    assert.equal(response.headers.get('content-encoding'), 'gzip');
    assert.match(response.headers.get('cache-control'), /no-store/);
    assert.match(response.headers.get('content-security-policy'), /frame-ancestors 'none'/);
    response = await fetch(base + '/index.html', { method: 'HEAD', headers: { Authorization: authorization } });
    assert.equal(response.status, 200);
    assert.equal(await response.text(), '');
    for (const suffix of ['/documents', '/data.json', '/.git/config', '/%2e%2e/secret']) {
      response = await fetch(base + suffix, { headers: { Authorization: authorization } });
      assert.equal(response.status, 404);
    }
    response = await fetch(base, { method: 'POST', body: 'test', headers: { Authorization: authorization } });
    assert.equal(response.status, 405);
    response = await fetch(base + '/healthz');
    assert.equal(response.status, 200);
    assert.equal(await response.text(), 'ok');
    console.log('PASS : accès sans mot de passe refusé, authentification correcte, compression, HEAD, contrôle de santé et fichiers privés inaccessibles.');
  } finally {
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
    fs.rmSync(dir, { recursive: true, force: true });
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
