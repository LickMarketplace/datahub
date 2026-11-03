'use strict';
// Private prototype access only. No catalogue or document upload API is exposed.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const zlib = require('node:zlib');
const { pipeline } = require('node:stream');

function createPreviewServer({ htmlPath, username = 'lick', password }) {
  if (typeof password !== 'string' || password.length < 16) {
    throw new Error('DATAHUB_PREVIEW_PASSWORD doit contenir au moins 16 caractères.');
  }
  if (!username || username.includes(':') || /[\r\n]/.test(username)) {
    throw new Error('Nom utilisateur invalide.');
  }
  const absolutePath = path.resolve(htmlPath || '');
  if (!fs.statSync(absolutePath).isFile()) throw new Error('Le fichier HTML est introuvable.');
  const digest = value => crypto.createHash('sha256').update(value).digest();
  const expected = digest(`${username}:${password}`);
  const headers = {
    'Cache-Control': 'private, no-store, max-age=0',
    'Referrer-Policy': 'no-referrer',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
    'Content-Security-Policy': "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: https: http:; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
  };
  const server = http.createServer({ maxHeaderSize: 16384 }, (req, res) => {
    for (const [key, value] of Object.entries(headers)) res.setHeader(key, value);
    const pathname = new URL(req.url, 'http://localhost').pathname;
    if (!['GET', 'HEAD'].includes(req.method)) {
      res.setHeader('Allow', 'GET, HEAD');
      res.writeHead(405).end();
      return;
    }
    if (pathname === '/healthz') {
      res.setHeader('Content-Type', 'text/plain; charset=utf-8');
      res.writeHead(200).end(req.method === 'HEAD' ? undefined : 'ok');
      return;
    }
    let supplied = '';
    const match = /^Basic ([A-Za-z0-9+/]+={0,2})$/i.exec(req.headers.authorization || '');
    if (match) supplied = Buffer.from(match[1], 'base64').toString('utf8');
    if (!crypto.timingSafeEqual(expected, digest(supplied))) {
      res.setHeader('WWW-Authenticate', 'Basic realm="Lick Datahub - acces prive", charset="UTF-8"');
      res.setHeader('Content-Type', 'text/plain; charset=utf-8');
      res.writeHead(401).end(req.method === 'HEAD' ? undefined : 'Accès privé. Identifiant et mot de passe requis.');
      return;
    }
    if (!['/', '/index.html'].includes(pathname)) {
      res.writeHead(404).end();
      return;
    }
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Vary', 'Accept-Encoding');
    if (req.method === 'HEAD') { res.writeHead(200).end(); return; }
    const source = fs.createReadStream(absolutePath);
    // Compress the response without keeping a second copy of the catalogue in memory.
    const gzip = /(?:^|,)\s*gzip(?:\s*;\s*q=(?!0(?:\.0*)?\b)[\d.]+)?\s*(?:,|$)/i.test(req.headers['accept-encoding'] || '');
    if (gzip) res.setHeader('Content-Encoding', 'gzip');
    const streams = gzip ? [source, zlib.createGzip({ level: 4 }), res] : [source, res];
    pipeline(...streams, error => { if (error && !res.destroyed) res.destroy(); });
  });
  server.headersTimeout = 15000;
  server.requestTimeout = 30000;
  server.keepAliveTimeout = 5000;
  return server;
}

if (require.main === module) {
  try {
    const port = Number(process.env.PORT || 8080);
    if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error('Port invalide.');
    const server = createPreviewServer({
      htmlPath: process.env.DATAHUB_HTML_PATH,
      username: process.env.DATAHUB_PREVIEW_USER || 'lick',
      password: process.env.DATAHUB_PREVIEW_PASSWORD
    });
    server.listen(port, process.env.DATAHUB_BIND_HOST || '127.0.0.1', () => {
      console.log('Accès privé Lick Datahub démarré. Aucun contenu du catalogue ne sera journalisé.');
    });
    server.on('error', () => { console.error('Impossible de démarrer le serveur d’aperçu.'); process.exitCode = 1; });
    process.on('SIGTERM', () => server.close());
    process.on('SIGINT', () => server.close());
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
module.exports = { createPreviewServer };
