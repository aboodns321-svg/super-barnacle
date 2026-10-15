// Bundles src/app.js with three.js into one inline script so the page needs no CDN or import maps.
// Run: npm install && node build.mjs
import { build } from 'esbuild';
import { readFileSync, writeFileSync } from 'node:fs';
const out = await build({ entryPoints: ['src/app.js'], bundle: true, minify: true, format: 'iife', target: ['safari13', 'chrome80'], write: false });
const js = out.outputFiles[0].text.replace(/<\/script/gi, '<\\/script');
const page = readFileSync('src/page.html', 'utf8').replace('<script>/*APP*/</script>', () => `<script>${js}</script>`);
writeFileSync('index.html', page);
writeFileSync('villa-3d.html', `<!doctype html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n</head>\n<body>\n${page}</body>\n</html>\n`);
console.log('built', (page.length / 1024).toFixed(0) + ' KB');
