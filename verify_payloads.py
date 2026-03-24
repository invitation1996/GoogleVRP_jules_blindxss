import asyncio
import os
from playwright.async_api import async_playwright

async def run_verification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        with open("verify_payloads.html", "r") as f:
            content = f.read()

        callbacks = []
        page.on("request", lambda request: (
            callbacks.append(request.url)
            if "1.hackeronce.com" in request.url
            else None
        ))

        print("Testing payloads in verify_payloads.html...")
        await page.set_content(content, wait_until="domcontentloaded")

        # Wait a bit for async payloads (onerror, onload, etc.)
        await asyncio.sleep(3)

        print("\n" + "="*50)
        print("VERIFICATION RESULTS")
        print("="*50)
        unique_callbacks = sorted(list(set(callbacks)))
        if unique_callbacks:
            print(f"Total unique callbacks captured: {len(unique_callbacks)}")
            for url in unique_callbacks:
                print(f"SUCCESS: Callback received from: {url}")
        else:
            print("FAILURE: No callbacks to 1.hackeronce.com were detected.")
        print("="*50)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_verification())
