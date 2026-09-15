import csv
import re
import time
from playwright.sync_api import sync_playwright

def scrape_fast_gmaps(queries, output_file="container_verified_leads_final.csv"):
    print("Launching Playwright for fast targeted extraction...")
    all_leads = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        for query in queries:
            print(f"\n--- Searching: {query} ---")
            url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
            try:
                page.goto(url, timeout=90000, wait_until="domcontentloaded")
            except Exception as e:
                continue

            time.sleep(4)
            
            # Scroll feed to load listings
            try:
                feed = page.locator('div[role="feed"]')
                for _ in range(10):
                    feed.evaluate("node => node.scrollTop = node.scrollHeight")
                    time.sleep(2)
            except Exception:
                pass

            listings = page.locator('div[role="article"]').all()
            print(f"Processing {len(listings)} listings...")

            for index, item in enumerate(listings):
                try:
                    item.scroll_into_view_if_needed()
                    item.click()
                    time.sleep(3) # Wait for panel load
                    
                    # Grab company name
                    name_elem = page.locator('h1.DUwDvf').first
                    name = name_elem.inner_text(timeout=1500) if name_elem.count() > 0 else f"Lead_{index+1}"

                    # Direct phone button selector on Google Maps
                    phone = "N/A"
                    try:
                        phone_elem = page.locator('button[data-item-id*="phone:tel:"]').first
                        if phone_elem.count() > 0:
                            phone = phone_elem.get_attribute("aria-label").replace("Phone: ", "").strip()
                    except Exception:
                        pass

                    # Fallback regex search on sidebar if button selector fails (using raw string to avoid warning)
                    if phone == "N/A":
                        sidebar = page.locator('div[role="main"]').last
                        sidebar_text = sidebar.inner_text() if sidebar.count() > 0 else ""
                        phone_match = re.search(r'(?:\+91[\-\s]?)?[6-9]\d{9}', sidebar_text)
                        if phone_match:
                            phone = phone_match.group(0).strip()

                    # Grab address
                    address = "N/A"
                    try:
                        addr_elem = page.locator('button[data-item-id="address"]').first
                        if addr_elem.count() > 0:
                            address = addr_elem.get_attribute("aria-label").replace("Address: ", "").strip()
                    except Exception:
                        pass

                    if name != "N/A" and not any(l['Company Name'] == name for l in all_leads):
                        all_leads.append({
                            "Company Name": name,
                            "Phone": phone,
                            "Address": address
                        })
                        print(f"[{len(all_leads)}] {name} | Phone: {phone}")

                except Exception:
                    continue

        if all_leads:
            with open(output_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["Company Name", "Phone", "Address"])
                writer.writeheader()
                writer.writerows(all_leads)
            print(f"\nSuccessfully saved {len(all_leads)} clean leads to {output_file}")
            
        browser.close()

if __name__ == "__main__":
    queries = [
        "Container Transporters in Nhava Sheva Navi Mumbai",
        "Logistics and Container Yards in Panvel",
        "Warehouse and Storage Companies in Taloja MIDC"
    ]
    scrape_fast_gmaps(queries)
