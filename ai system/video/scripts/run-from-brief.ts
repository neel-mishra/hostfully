#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

type RunOptions = {
  briefPath: string;
  comp: 'HypeVertical-9x16' | 'HypeHorizontal-16x9';
  outPath?: string;
};

function parseArgs(argv: string[]): RunOptions {
  const args = new Map<string, string>();
  for (let i = 0; i < argv.length; i += 2) {
    const key = argv[i];
    const value = argv[i + 1];
    if (key && value) args.set(key, value);
  }

  const briefPath = args.get('--brief');
  if (!briefPath) {
    throw new Error('Missing required argument: --brief <path-to-brief.md>');
  }

  const compRaw = args.get('--comp') ?? 'HypeVertical-9x16';
  if (compRaw !== 'HypeVertical-9x16' && compRaw !== 'HypeHorizontal-16x9') {
    throw new Error('Invalid --comp value. Use HypeVertical-9x16 or HypeHorizontal-16x9.');
  }

  return {
    briefPath,
    comp: compRaw,
    outPath: args.get('--out'),
  };
}

function main() {
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);
  const rootDir = path.join(__dirname, '..');
  const options = parseArgs(process.argv.slice(2));
  const resolvedBrief = path.resolve(process.cwd(), options.briefPath);

  if (!fs.existsSync(resolvedBrief)) {
    throw new Error(`Brief file not found: ${resolvedBrief}`);
  }

  const brief = fs.readFileSync(resolvedBrief, 'utf-8');
  const outputPath =
    options.outPath ??
    path.join(rootDir, 'out', options.comp === 'HypeVertical-9x16' ? 'hype-9x16.mp4' : 'hype-16x9.mp4');

  process.stdout.write('\n=== VibeHype Brief Ingest ===\n');
  process.stdout.write(`Brief: ${resolvedBrief}\n`);
  process.stdout.write(`Composition: ${options.comp}\n`);
  process.stdout.write(`Output: ${outputPath}\n`);
  process.stdout.write('\nNo auto-storyboard rewrite is applied yet.\n');
  process.stdout.write('Use this brief while editing src/storyboard/default20s.ts, then render.\n\n');
  process.stdout.write('--- Brief Preview ---\n');
  process.stdout.write(`${brief.slice(0, 800)}\n`);
  process.stdout.write('--- End Preview ---\n\n');

  const env = {
    ...process.env,
    COMP: options.comp,
    OUT: outputPath,
  };

  const renderScript = path.join(rootDir, 'scripts', 'render.ts');
  const render = spawnSync('node', [renderScript], {cwd: rootDir, env, stdio: 'inherit'});
  if (render.status !== 0) {
    process.exit(render.status ?? 1);
  }
}

main();
