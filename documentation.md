Butcher Shop Lead Generation & WhatsApp Marketing - Complete Guide
📁 Project Structure
butcher-scrapper/
├── venv/                    # Virtual environment
├── scraper.py              # Single district scraper
├── scraper_all.py          # All districts scraper
├── whatsapp_sender.py      # WhatsApp message sender
├── districts.txt           # List of 64 Bangladesh districts
├── promo.jpeg             # Promotional image for WhatsApp
└── results/               # Scraped data folder
    ├── Dhaka.xlsx
    ├── Chittagong.xlsx
    └── ALL_DISTRICTS.xlsx  # Combined data

🚀 Initial Setup
1. Install Dependencies
bash# Install Python virtual environment package
sudo apt-get install python3.12-venv

# Create project folder
mkdir butcher-scrapper
cd butcher-scrapper

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install selenium pandas webdriver-manager openpyxl

# For WhatsApp messaging (optional)
sudo apt-get install xclip
2. Create Required Files
Create districts.txt:
Dhaka
Chittagong
Sylhet
Rajshahi
Khulna
Barisal
Rangpur
Mymensingh
... (all 64 districts)
Add promotional image:

Place your promo.jpeg in the main folder


📊 Part 1: Data Collection (Lead Generation)
Single District Scraper
Create scraper.py:
pythonfrom selenium import webdriver
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
    
    # Scroll to load all results
    scrollable = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
    for _ in range(5):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable)
        time.sleep(3)
    
    # Get shop links
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
    district = input("Enter district name: ")
    scrape_district(district)
Usage:
bashpython scraper.py
# Enter: Dhaka

All Districts Scraper
Create scraper_all.py:
pythonfrom selenium import webdriver
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
    
    scrollable = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
    for _ in range(5):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable)
        time.sleep(3)
    
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
    with open('districts.txt', 'r') as f:
        districts = [line.strip() for line in f if line.strip()]
    
    print(f"Starting scrape for {len(districts)} districts...\n")
    
    for i, district in enumerate(districts):
        print(f"[{i+1}/{len(districts)}] Processing {district}...")
        scrape_district(district)
        time.sleep(5)
    
    print("✓ All districts completed!")
    
    # Combine all files
    all_data = []
    for district in districts:
        try:
            df = pd.read_excel(f'results/{district}.xlsx')
            all_data.append(df)
        except:
            pass
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined.to_excel('results/ALL_DISTRICTS.xlsx', index=False)
        print(f"✓ Combined: {len(combined)} total shops")
Usage:
bashpython scraper_all.py
# Runs automatically for all 64 districts
# Takes 4-6 hours
Output: Individual Excel files + ALL_DISTRICTS.xlsx with columns:

Name
Phone
District
Upazilla/Area


📱 Part 2: WhatsApp Marketing
Create whatsapp_sender.py:
pythonfrom selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# ===== CUSTOMIZE HERE =====
message = "Special offer on fresh meat! Visit us today."
image_path = "/home/nahid/Projects/butcher-scrapper/promo.jpeg"
# ==========================

df = pd.read_excel('results/ALL_DISTRICTS.xlsx')  # Or use specific district file

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://web.whatsapp.com')
print("Scan QR code and press Enter...")
input()

for index, row in df.iterrows():
    try:
        phone = str(row['Phone']).strip().replace(' ', '').replace('-', '')
        
        if len(phone) == 10 and not phone.startswith('0'):
            phone = '0' + phone
        if phone.startswith('0'):
            phone = phone[1:]
        
        full_number = f'880{phone}'
        print(f"\n[{index+1}/{len(df)}] {row['Name']} → {full_number}")
        
        driver.get(f'https://web.whatsapp.com/send?phone={full_number}')
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        time.sleep(5)
        
        # Click attach
        attach = driver.find_element(By.XPATH, '//button[@aria-label="Attach"]')
        driver.execute_script("arguments[0].click();", attach)
        time.sleep(3)
        
        # Upload image
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        file_input.send_keys(image_path)
        time.sleep(10)
        
        # Add caption
        caption = driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
        caption.send_keys(message)
        time.sleep(2)
        caption.send_keys(Keys.ENTER)
        
        print("✓ Sent!")
        time.sleep(8)
        
    except Exception as e:
        print(f"✗ {type(e).__name__}")
        continue

driver.quit()
Usage:
bashpython whatsapp_sender.py
# 1. Scan WhatsApp Web QR code
# 2. Press Enter
# 3. Script sends to all contacts automatically

📋 Complete Workflow
Step 1: Activate Environment
bashcd butcher-scrapper
source venv/bin/activate
Step 2: Collect Data
bash# Option A: Single district
python scraper.py

# Option B: All districts
python scraper_all.py
Step 3: Prepare Marketing Material

Design promotional image (promo.jpeg)
Write message in whatsapp_sender.py

Step 4: Send WhatsApp Messages
bashpython whatsapp_sender.py

⚙️ Customization
Change Search Query
In scraper files, modify:
pythonurl = f"https://www.google.com/maps/search/butcher+shop+{district_name}+Bangladesh"
# Change to: restaurant, pharmacy, salon, etc.
Filter by Upazilla
pythondf = pd.read_excel('results/Dhaka.xlsx')
filtered = df[df['Upazilla/Area'] == 'Gulshan']
filtered.to_excel('results/Gulshan_Only.xlsx')
Test with Small Sample
python# In whatsapp_sender.py
df = pd.read_excel('results/Demo.xlsx')  # Create Demo.xlsx with 2-3 test numbers

🎯 Use Cases

Lead Generation: Collect business contacts from Google Maps
Targeted Marketing: Send promotional messages to specific areas
Market Research: Analyze business distribution by district
Competitor Analysis: Map competitor locations


⚠️ Important Notes

Rate Limits: Google Maps may block if scraping too fast
WhatsApp Limits: Don't send 1000+ messages/day (risk of ban)
Phone Format: Script handles both 01XXXXXXXXX and 1XXXXXXXXX
Ethics: Only use for legitimate business purposes