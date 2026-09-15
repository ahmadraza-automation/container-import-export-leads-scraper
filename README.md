# Container & Import-Export Leads Scraper

Playwright-based scrapers for generating business leads in logistics, container brokering, and import/export sectors.

## Scripts

### 1. `Container_Brokering_Lead_Scraper.py`
- Scrapes Google Maps for container transporters, logistics yards, and warehouse companies.
- Targets areas: Nhava Sheva (Navi Mumbai), Panvel, Taloja MIDC.
- Extracts: Company Name, Phone, Address.
- Output: `container_verified_leads_final.csv`

### 2. `Client_Hunting_For_Import_Export.py`
- Visits target company websites (example: Sun Pharma contact page).
- Extracts emails and phone numbers using regex.
- Output: `vip_target_leads.xlsx`

## Requirements
```bash
pip install playwright pandas openpyxl
playwright install chromium
```

## Usage
```bash
# Container / Logistics leads from Google Maps
python Container_Brokering_Lead_Scraper.py

# Client hunting (email + phone extraction)
python Client_Hunting_For_Import_Export.py
```

## Notes
- Run with `headless=False` for better reliability on Google Maps.
- Update the `queries` list or `target_url` as needed for different locations/companies.
