import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const source = path.join(here, 'entry.png');
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const destination = path.join(outputDir, 'entry.png');
const pngSignature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);

function fail(message: string): never {
  console.error(message);
  process.exit(1);
}

let data: Buffer;
try {
  data = readFileSync(source);
} catch {
  fail(`Unable to read ${source}`);
}

if (data.length > 1024 * 1024) {
  fail('Input PNG exceeds the 1 MiB cap');
}
if (data.length < 24 || !data.subarray(0, pngSignature.length).equals(pngSignature)) {
  fail('Input has an invalid PNG signature or IHDR header');
}
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  fail(`Input PNG must be 1024x1024; got ${width}x${height}`);
}

try {
  mkdirSync(outputDir, { recursive: true });
  writeFileSync(destination, data);
} catch {
  fail(`Unable to write ${destination}`);
}

console.log(`Copied entry.png (${width} ${height}) to ${destination}`);
