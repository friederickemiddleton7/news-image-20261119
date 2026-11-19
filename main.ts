/**
 * make.fun entry — news-image-20261119
 *
 * Copies the poster beside this entrypoint to <output>/entry.png, byte for byte.
 * Output dir: $MAKEFUN_OUTPUT_DIR, default /output.
 * Standard library only, no network.
 */
import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1024 * 1024; // 1 MiB, the entry size cap
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function fail(message: string): never {
  console.error(`entry.png: ${message}`);
  process.exit(1);
}

const sourcePath = join(dirname(fileURLToPath(import.meta.url)), "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const targetPath = join(outputDir, "entry.png");

// --- read ------------------------------------------------------------------
let bytes: Buffer;
try {
  const info = statSync(sourcePath);
  if (!info.isFile()) fail(`${sourcePath} is not a regular file`);
  if (info.size === 0) fail(`${sourcePath} is empty`);
  if (info.size > MAX_BYTES) {
    fail(`${sourcePath} is ${info.size} bytes, over the ${MAX_BYTES} byte (1 MiB) limit`);
  }
  bytes = readFileSync(sourcePath);
} catch (error) {
  const reason = error instanceof Error ? error.message : String(error);
  fail(`cannot read ${sourcePath} (${reason})`);
}

// --- validate PNG ----------------------------------------------------------
if (bytes.length < PNG_SIGNATURE.length || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  fail(`${sourcePath} is not a PNG (bad signature)`);
}
if (bytes.length <= 24 || bytes.toString("latin1", 12, 16) !== "IHDR") {
  fail(`${sourcePath} is not a PNG (no IHDR header)`);
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width === 0 || height === 0) fail(`${sourcePath} has a zero-sized IHDR (${width}x${height})`);

// --- write -----------------------------------------------------------------
try {
  mkdirSync(outputDir, { recursive: true });
  writeFileSync(targetPath, bytes);
} catch (error) {
  const reason = error instanceof Error ? error.message : String(error);
  fail(`cannot write ${targetPath} (${reason})`);
}

const written = statSync(targetPath).size;
if (written !== bytes.length) {
  fail(`wrote ${written} bytes to ${targetPath}, expected ${bytes.length}`);
}

console.log(`wrote ${written} bytes to ${targetPath} (${width}x${height} PNG)`);
