#!/usr/bin/env node

/**
 * Test Meta API Connection
 *
 * Loads META_ACCESS_TOKEN from .env.local and verifies /me + /me/adaccounts.
 */

import { config } from "dotenv";
config({ path: ".env.local" });

import fetch from "node-fetch";

console.log("🧪 Testing Meta API Connection");
console.log("==============================");

async function testMetaAPI() {
  try {
    const token = process.env.META_ACCESS_TOKEN;
    if (!token) {
      console.error("❌ META_ACCESS_TOKEN not found in .env.local");
      return false;
    }

    console.log("✅ Token found:", token.substring(0, 20) + "...");

    const meResponse = await fetch(`https://graph.facebook.com/v23.0/me?access_token=${encodeURIComponent(token)}`);
    const meData = await meResponse.json();
    if (meData.error) {
      console.error("❌ API Error:", meData.error.message);
      return false;
    }
    console.log("✅ Connected as:", meData.name || meData.id);

    console.log("\n📊 Getting Ad Accounts...");
    const accountsResponse = await fetch(
      `https://graph.facebook.com/v23.0/me/adaccounts?fields=id,name,account_status,currency&access_token=${encodeURIComponent(token)}`,
    );
    const accountsData = await accountsResponse.json();
    if (accountsData.error) {
      console.error("❌ Cannot access ad accounts:", accountsData.error.message);
      console.log("\n💡 Make sure your token has these permissions:");
      console.log(" • ads_management");
      console.log(" • ads_read");
      console.log(" • business_management");
      return false;
    }

    if (accountsData.data?.length) {
      console.log(`✅ Found ${accountsData.data.length} ad accounts:`);
      accountsData.data.forEach((account) => console.log(` • ${account.name} (${account.id}) - ${account.currency}`));
    } else {
      console.log("⚠️ No ad accounts found.");
    }

    console.log("\n🎉 Meta API connection test successful!");
    return true;
  } catch (error) {
    console.error("❌ Connection test failed:", error.message);
    return false;
  }
}

testMetaAPI()
  .then((success) => process.exit(success ? 0 : 1))
  .catch((error) => {
    console.error("❌ Unexpected error:", error);
    process.exit(1);
  });

