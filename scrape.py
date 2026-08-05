import re
from playwright.sync_api import sync_playwright

SEEDS = range(14, 24)  # 14..23 inclusive
URL_TMPL = "https://sanand0.github.io/tdsdata/js_table/?seed={seed}"

number_re = re.compile(r"-?\d+(?:\.\d+)?")

def main():
    grand_total = 0.0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for seed in SEEDS:
            url = URL_TMPL.format(seed=seed)
            page.goto(url, wait_until="networkidle")
            # wait for at least one table to be rendered by JS
            page.wait_for_selector("table")

            seed_total = 0.0
            tables = page.query_selector_all("table")
            for table in tables:
                cells = table.query_selector_all("td")
                for cell in cells:
                    text = cell.inner_text().strip()
                    for match in number_re.findall(text):
                        seed_total += float(match)

            print(f"Seed {seed}: {seed_total}")
            grand_total += seed_total

        browser.close()

    print(f"TOTAL SUM ACROSS ALL SEEDS: {grand_total}")

if __name__ == "__main__":
    main()
