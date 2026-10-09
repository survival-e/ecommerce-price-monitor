import csv
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging for a professional execution trace
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class PriceMonitor:
    def __init__(self, base_url):
        self.base_url = base_url

        # Professional Driver Setup
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Runs silently in the background for production speed
        options.add_argument("--disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)  # Dynamic wait up to 10s

    def scrape_catalog(self, pages_to_scrape=2):
        scraped_data = []

        for page in range(1, pages_to_scrape + 1):
            target_url = f"{self.base_url}/catalogue/page-{page}.html"
            logging.info(f"Fetching page {page}: {target_url}")

            self.driver.get(target_url)

            # Explicit Wait: Wait until product cards are actually rendered in the DOM
            try:
                products = self.wait.until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod"))
                )
            except Exception as e:
                logging.error(f"Timed out waiting for elements on page {page}: {e}")
                break

            for product in products:
                title = product.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
                price = product.find_element(By.CLASS_NAME, "price_color").text
                availability = product.find_element(By.CLASS_NAME, "availability").text.strip()

                # Sanitize price float for data analysis
                clean_price = float(price.replace("£", "").replace("$", ""))

                scraped_data.append({
                    "title": title,
                    "price_currency": clean_price,
                    "in_stock": "In stock" in availability
                })

        return scraped_data

    def export_to_csv(self, filename, data):
        if not data:
            logging.warning("No data to export.")
            return

        keys = data[0].keys()
        with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

        logging.info(f"Successfully exported {len(data)} items to {filename} 📦")

    def close(self):
        self.driver.quit()


# --- Execution ---
if __name__ == "__main__":
    BASE_URL = "https://books.toscrape.com"

    monitor = PriceMonitor(BASE_URL)
    try:
        data = monitor.scrape_catalog(pages_to_scrape=3)
        monitor.export_to_csv("portfolio_price_tracker.csv", data)
    finally:
        monitor.close()