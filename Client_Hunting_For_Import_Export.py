import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import re

async def scrape_target_site():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
        )
        page = await context.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        target_url = "https://www.sunpharma.com/contact-us/"
        print(f"Navigating to {target_url}...")
        
        try:
            await page.goto(target_url, timeout=90000, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)
        except Exception as e:
            print(f"Navigation warning: {e}")

        try:
            body_text = await page.inner_text("body")
        except:
            body_text = ""

        await browser.close()

        emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', body_text)
        phones = re.findall(r'\+?[0-9\-\s]{10,15}', body_text)
        
        unique_emails = list(set(emails))
        unique_phones = list(set([p.strip() for p in phones if len(p.strip()) >= 8]))

        print(f"Found Emails: {unique_emails}")
        print(f"Found Phones: {unique_phones}")

        extracted_data = [{
            "Company / Website": target_url,
            "Emails": ", ".join(unique_emails) if unique_emails else "N/A",
            "Phones": ", ".join(unique_phones[:3]) if unique_phones else "N/A"
        }]

        df = pd.DataFrame(extracted_data)
        df.to_excel("vip_target_leads.xlsx", index=False)
        print("Data successfully saved to 'vip_target_leads.xlsx'!")

asyncio.run(scrape_target_site())
