from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_district(district_name):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    data = []
    
    url = f"https://www.google.com/maps/search/butcher+shop+{district_name}+Bangladesh"
    driver.get(url)
    time.sleep(5)
    
    # Scroll to load all
    scrollable = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
    for _ in range(5):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable)
        time.sleep(3)
    
    # Get all shop links
    shops = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/maps/place/"]')
    shop_links = [shop.get_attribute('href') for shop in shops[:50]]  # Get first 50
    
    print(f"Found {len(shop_links)} shops in {district_name}\n")
    
    for i, link in enumerate(shop_links):
        try:
            driver.get(link)
            time.sleep(3)
            
            # Name
            name = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf').text
            
            # Phone - skip if none
            try:
                phone_button = driver.find_element(By.CSS_SELECTOR, 'button[data-item-id*="phone"]')
                phone = phone_button.get_attribute('data-item-id').replace('phone:tel:', '')
            except:
                print(f"  ✗ {name} - No phone")
                continue
            
            # Address
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
            
            print(f"  ✓ {len(data)}. {name} - {phone}")
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            continue
    
    driver.quit()
    
    if data:
        df = pd.DataFrame(data)
        df.to_excel(f'results/{district_name}.xlsx', index=False)
        print(f"\n✓ Saved {len(data)} shops to results/{district_name}.xlsx\n")
    else:
        print(f"\n✗ No shops found\n")

if __name__ == "__main__":
    district = input("Enter district name: ")
    scrape_district(district)