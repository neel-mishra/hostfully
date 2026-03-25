#!/usr/bin/env node

/**
 * Minimal setup helper:
 * - Creates/merges Cursor settings.json `mcpServers.meta-ads`
 * - Does NOT store tokens unless you paste them in intentionally
 */

import fs from "fs";
import path from "path";
import os from "os";
import readline from "readline";

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

function question(query) {
  return new Promise((resolve) => rl.question(query, resolve));
}

function getCursorConfigPath() {
  return path.join(os.homedir(), "Library", "Application Support", "Cursor", "User", "settings.json");
}

function writeMergedConfig(configPath, serverConfig) {
  let existing = {};
  if (fs.existsSync(configPath)) {
    existing = JSON.parse(fs.readFileSync(configPath, "utf8"));
  }
  if (!existing.mcpServers) existing.mcpServers = {};
  existing.mcpServers["meta-ads"] = serverConfig;

  fs.writeFileSync(configPath, JSON.stringify(existing, null, 2));
}

async function main() {
  console.log("🚀 Meta Ads MCP setup (Cursor)");
  const configPath = getCursorConfigPath();

  const projectPath = await question("Absolute path to meta-ads-mcp folder: ");
  const buildPath = path.join(projectPath.trim(), "build", "src", "index.js");

  const useTokenPlaceholder = await question("Use env placeholders (recommended)? (Y/n): ");
  const usePlaceholders = useTokenPlaceholder.trim().toLowerCase() !== "n";

  const serverConfig = {
    command: process.execPath,
    args: [buildPath],
    env: usePlaceholders
      ? {
          META_ACCESS_TOKEN: "${META_ACCESS_TOKEN}",
          META_APP_ID: "${META_APP_ID}",
          META_APP_SECRET: "${META_APP_SECRET}",
          META_AUTO_REFRESH: "true",
          META_API_TIER: "standard",
        }
      : {
          META_ACCESS_TOKEN: await question("Meta access token (will be written to settings.json): "),
        },
  };

  writeMergedConfig(configPath, serverConfig);
  console.log(`✅ Wrote MCP config to: ${configPath}`);
  console.log("Restart Cursor to load the MCP server.");
  rl.close();
}

main().catch((err) => {
  console.error("❌ Setup failed:", err);
  process.exit(1);
});

