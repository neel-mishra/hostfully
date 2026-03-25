#!/usr/bin/env node

import { execSync } from "child_process";
import fs from "fs";
import path from "path";
import os from "os";

function getCursorConfigPath() {
  // Cursor user settings.json (macOS)
  return path.join(os.homedir(), "Library", "Application Support", "Cursor", "User", "settings.json");
}

function checkConfiguration() {
  console.log("🔍 Meta Ads MCP Server Health Check\n");

  try {
    const version = execSync("node --version", { encoding: "utf8" }).trim();
    console.log(`✅ Node.js version: ${version}`);
  } catch {
    console.log("❌ Node.js not found");
    return false;
  }

  try {
    const version = execSync("npm --version", { encoding: "utf8" }).trim();
    console.log(`✅ npm version: ${version}`);
  } catch {
    console.log("❌ npm not found");
    return false;
  }

  const configPath = getCursorConfigPath();
  console.log(`\n📁 Checking Cursor configuration: ${configPath}`);

  if (!fs.existsSync(configPath)) {
    console.log("❌ Cursor settings.json not found");
    return false;
  }

  try {
    const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
    if (!config.mcpServers) {
      console.log("❌ No MCP servers configured in Cursor settings");
      return false;
    }

    if (!config.mcpServers["meta-ads"]) {
      console.log("❌ MCP server 'meta-ads' not configured");
      console.log("Available servers:", Object.keys(config.mcpServers));
      return false;
    }

    const serverConfig = config.mcpServers["meta-ads"];
    console.log("✅ meta-ads MCP server configuration found");

    if (!serverConfig.env || (!serverConfig.env.META_ACCESS_TOKEN && !process.env.META_ACCESS_TOKEN)) {
      console.log("⚠️ META_ACCESS_TOKEN not found in Cursor config env; ensure it is set in env vars or .env.local for local runs");
    } else {
      console.log("✅ META_ACCESS_TOKEN configured (Cursor or env)");
    }

    console.log("\n✅ Health check passed (configuration present).");
    return true;
  } catch (error) {
    console.log("❌ Invalid JSON in Cursor settings.json");
    console.log("Error:", error.message);
    return false;
  }
}

process.exit(checkConfiguration() ? 0 : 1);

