#!/usr/bin/env node
import {renderMedia} from '@remotion/renderer';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootDir = path.join(__dirname, '..');

const comp = process.env.COMP || 'HypeVertical-9x16';
const outPath =
  process.env.OUT || path.join(rootDir, 'out', comp === 'HypeVertical-9x16' ? 'hype-9x16.mp4' : 'hype-16x9.mp4');

async function main() {
  await renderMedia({
    serveUrl: rootDir,
    composition: comp,
    codec: 'h264',
    outputLocation: outPath,
  });
}

main().catch((err) => {
  // eslint-disable-next-line no-console
  console.error(err);
  process.exit(1);
});

