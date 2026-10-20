# Walmart Blackstone — Discord + GitHub Actions starter

**Diagnostic-only. Does NOT yet send stock alerts.** Walmart's store-specific shipping price and availability need reliable live validation before enabling alerts. A page that merely mentions Lansing or Shipping is not proof.

## Setup
1. Create a public GitHub repository with a README, then upload `monitor.py`, `requirements.txt`, and `.github/workflows/check.yml` preserving the folders. Alternatively upload the files using GitHub's web interface and create `.github/workflows/check.yml` with **Add file → Create new file**.
2. Create a Discord server and text channel; in channel settings choose **Integrations → Webhooks → New Webhook**, then **Copy Webhook URL**. If Webhooks is unavailable, check Manage Webhooks permissions or desktop interface.
3. GitHub repository → **Settings → Secrets and variables → Actions → New repository secret**. Name: `DISCORD_WEBHOOK_URL`. Value: your copied webhook URL. Never commit the URL.
4. Repository **Actions** → select **Walmart Blackstone check** → **Run workflow** → check `test_discord` → **Run workflow**. Check Discord for a test message.
5. Run workflow again with `test_discord` unchecked. In Actions job summary, download **walmart-diagnostics-...** artifact and inspect `result.json`, `page.png`, and `page_excerpt.txt`.
6. GitHub scheduled workflows on the default branch will start approximately every 5 minutes, but may be delayed or skipped. Monitor the Actions tab.

## Expected behavior
- `test_discord=true`: sends exactly one Discord test message.
- Otherwise: opens the listing, logs evidence and marks availability `UNVERIFIED`.
- **Never sends a purchase alert** until actual store ID 2817, Shipping availability, and shipping-specific price $105.45–$116.55 can be reliably verified.

## Privacy and safety
- Public repository source code is visible. GitHub Secrets keep the webhook out of source and logs unless you accidentally print it.
- Avoid bypassing CAPTCHA, bot detection, or access restrictions. If Walmart doesn't allow reliable automation, use a permitted inventory provider.
- Five-minute schedule is not a persistent process and has no strict real-time guarantee.
- Check GitHub's current Actions terms and usage before enabling continuous checks.

## Next development milestone
Calibrate Playwright selectors and store selection against a legitimate live session, with fail-closed logic and tests for incorrect store, pickup-only inventory, wrong price, and blocked pages. Until then, this package is a safe working scheduling/notification/diagnostic foundation, not a finished Walmart stock bot.
