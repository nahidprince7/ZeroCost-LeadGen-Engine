from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_district(district_name):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    data = []
    
    url = f"https://www.google.com/maps/search/clothing+shop+{district_name}+Bangladesh"
    driver.get(url)
    time.sleep(5)
    
    # Scroll
    scrollable = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
    for _ in range(5):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable)
        time.sleep(3)
    
    # Get links
    shops = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/maps/place/"]')
    shop_links = [shop.get_attribute('href') for shop in shops[:50]]
    
    print(f"Found {len(shop_links)} shops in {district_name}")
    
    for i, link in enumerate(shop_links):
        try:
            driver.get(link)
            time.sleep(3)
            
            name = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf').text
            
            try:
                phone_button = driver.find_element(By.CSS_SELECTOR, 'button[data-item-id*="phone"]')
                phone = phone_button.get_attribute('data-item-id').replace('phone:tel:', '')
            except:
                continue
            
            try:
                address = driver.find_element(By.CSS_SELECTOR, 'button[data-item-id="address"]').get_attribute('aria-label')
                parts = [p.strip() for p in address.replace('Address: ', '').split(',')]
                upazilla = parts[1] if len(parts) > 1 else parts[0]
            except:
                upazilla = "N/A"
            
            data.append({
                'Name': name,
                'Phone': phone,
                'District': district_name,
                'Upazilla/Area': upazilla
            })
            
        except:
            continue
    
    driver.quit()
    
    if data:
        df = pd.DataFrame(data)
        df.to_excel(f'results/{district_name}.xlsx', index=False)
        print(f"✓ {district_name}: {len(data)} shops saved\n")
    else:
        print(f"✗ {district_name}: No shops found\n")

if __name__ == "__main__":
    # Read districts from file
    with open('districts.txt', 'r') as f:
        districts = [line.strip() for line in f if line.strip()]
    
    print(f"Starting scrape for {len(districts)} districts...\n")
    
    for i, district in enumerate(districts):
        print(f"[{i+1}/{len(districts)}] Processing {district}...")
        scrape_district(district)
        time.sleep(5)  # Wait between districts
    
    print("✓ All districts completed!")

    # Add at the end of scraper_all.py, replace the last print statement:
    
    # Combine all files into one
    all_data = []
    for district in districts:
        file_path = f'results/{district}.xlsx'
        try:
            df = pd.read_excel(file_path)
            all_data.append(df)
        except:
            pass
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined.to_excel('results/ALL_DISTRICTS.xlsx', index=False)
        print(f"✓ Combined file created: {len(combined)} total shops")