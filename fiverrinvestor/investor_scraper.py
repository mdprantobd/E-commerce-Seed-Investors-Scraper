import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def scrape_investor(username):
    url = f"https://signal.nfx.com/investors/{username}"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(6)  # Wait for JS to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # --- Name ---
    name = soup.find("h1").get_text(strip=True) if soup.find("h1") else "N/A"

    # --- Investment amount ---
    inv_amount_tag = soup.find("span", string=lambda s: s and "Investment Range" in s)
    investment_amount = inv_amount_tag.find_next("span").get_text(strip=True) if inv_amount_tag else "N/A"

    # --- Website ---
    website_tag = soup.find("a", class_="ml1 subheader lower-subheader")
    website = website_tag.get("href") if website_tag else "N/A"

    # --- Email ---
    email_tag = soup.find("a", href=lambda h: h and "mailto:" in h)
    email = email_tag.get("href").replace("mailto:", "") if email_tag else "N/A"

    # --- Location ---
    location_tag = soup.find("span", class_="ml1")
    location = location_tag.get_text(strip=True) if location_tag else "N/A"

    return {
        "Name": name,
        "Investment amount": investment_amount,
        "Website": website,
        "Email": email,
        "Location": location
    }

def scrape_from_file(filename):
    with open(filename, "r") as f:
        usernames = [line.strip() for line in f if line.strip()]

    all_data = []
    for username in usernames:
        print(f"Scraping: {username}")
        data = scrape_investor(username)
        all_data.append(data)

    df = pd.DataFrame(all_data)
    df.to_csv("investors_info.csv", index=False)
    df.to_excel("investors_info.xlsx", index=False)
    print("\n✅ All data saved to investors_info.csv and investors_info.xlsx")

if __name__ == "__main__":
    scrape_from_file("usernames.txt")
