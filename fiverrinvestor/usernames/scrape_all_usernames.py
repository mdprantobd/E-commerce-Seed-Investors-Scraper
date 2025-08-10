import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrape_usernames_load_more(target_count=240, max_clicks=30):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get("https://signal.nfx.com/investor-lists/top-e-commerce-seed-investors")
    time.sleep(5)  # wait initial load

    all_usernames = set()
    clicks = 0

    while len(all_usernames) < target_count and clicks < max_clicks:
        print(f"Click {clicks+1}: Collected {len(all_usernames)} usernames so far...")
        # Scrape usernames visible now
        links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/investors/']")
        for link in links:
            href = link.get_attribute("href")
            if href:
                username = href.split("/investors/")[-1].strip("/")
                all_usernames.add(username)

        try:
            load_more_button = driver.find_element(By.XPATH, "//button[contains(text(),'LOAD MORE INVESTORS')]")
            if load_more_button.is_displayed() and load_more_button.is_enabled():
                load_more_button.click()
                clicks += 1
                time.sleep(4)  # wait for more investors to load
            else:
                print("Load More button not clickable, stopping.")
                break
        except Exception:
            print("Load More button not found, probably no more investors.")
            break

    # Final scrape after last click (in case new investors loaded)
    links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/investors/']")
    for link in links:
        href = link.get_attribute("href")
        if href:
            username = href.split("/investors/")[-1].strip("/")
            all_usernames.add(username)

    driver.quit()
    return list(all_usernames)

if __name__ == "__main__":
    usernames = scrape_usernames_load_more()
    with open("username.txt", "w") as f:
        for u in usernames:
            f.write(u + "\n")
    print(f"Saved {len(usernames)} usernames to username.txt")
