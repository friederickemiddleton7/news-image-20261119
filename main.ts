import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const entryName = "entry.png";
const maxBytes = 1_048_576;
const pngSignature = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

function main(): void {
  // Resolve the source beside this module, regardless of the working directory.
  const sourceDir = dirname(fileURLToPath(import.meta.url));
  const sourcePath = join(sourceDir, entryName);
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const outputPath = join(outputDir, entryName);

  // Validate the original bytes before creating or writing anything.
  const bytes = readFileSync(sourcePath);
  if (bytes.length >= maxBytes) {
    throw new Error(
      `${entryName} must be under ${maxBytes} bytes (found ${bytes.length}).`,
    );
  }

  if (!bytes.subarray(0, pngSignature.length).equals(pngSignature)) {
    throw new Error(`${entryName} has an invalid PNG signature.`);
  }

  // Write the same buffer without decoding or re-encoding the image.
  mkdirSync(dirname(outputPath), { recursive: true });
  writeFileSync(outputPath, bytes);
  console.log(`Copied ${entryName} (${bytes.length} bytes) to ${JSON.stringify(outputPath)}.`);
}

try {
  main();
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}
