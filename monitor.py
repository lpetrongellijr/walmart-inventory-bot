"""Safe Walmart diagnostic monitor. Does not claim stock without validated checks."""
import json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path
import requests
from playwright.sync_api import sync_playwright

URL = 'https://www.walmart.com/ip/15308304145'
LOW, HIGH = 105.45, 116.55
OUT = Path('diagnostics'); OUT.mkdir(exist_ok=True)

def discord(message):
    url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not url: raise RuntimeError('DISCORD_WEBHOOK_URL secret missing')
    response = requests.post(url, json={'content': message}, timeout=20)
    response.raise_for_status()

def main():
    if os.environ.get('TEST_DISCORD') == '1':
        discord('Test successful: Walmart monitor can reach Discord. This is NOT a stock alert.')
        print('Discord test sent'); return
    result = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'product_id':'15308304145', 'store_id_expected':'2817',
              'store_verified':False, 'shipping_verified':False,
              'shipping_price_verified':False, 'price':None, 'eligible':False,
              'status':'UNVERIFIED — diagnostic only'}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(locale='en-US', viewport={'width':1440,'height':900})
            response = page.goto(URL, wait_until='domcontentloaded', timeout=60000)
            page.wait_for_timeout(3000)
            result['http_status'] = response.status if response else None
            body = page.locator('body').inner_text(timeout=15000)
            result['page_title'] = page.title()
            # Diagnostics only. Text mentioning a store or a price does not verify
            # the selected fulfillment store, shipping eligibility, or shipping price.
            result['mentions_lansing'] = 'lansing' in body.lower()
            result['mentions_shipping'] = 'shipping' in body.lower()
            result['sample_price_strings'] = re.findall(r'\$\s*\d[\d,]*\.\d{2}', body)[:10]
            page.screenshot(path=str(OUT/'page.png'), full_page=False)
            (OUT/'page_excerpt.txt').write_text(body[:10000], encoding='utf-8')
            browser.close()
    except Exception as e:
        result['status'] = 'CHECK FAILED — no stock claim'
        result['error'] = f'{type(e).__name__}: {str(e)[:300]}'
    (OUT/'result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    # Intentionally NO purchase alerts. Must implement & validate reliable store,
    # shipping, and price checks before turning on alerts.

if __name__ == '__main__': main()
