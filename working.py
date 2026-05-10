from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

message = "Special offer on fresh meat! Visit us today."
image_path = "/home/nahid/Projects/butcher-scrapper/promo.jpeg"

df = pd.read_excel('results/Demo.xlsx')

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
        
        # Wait for chat to load - look for message input
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        print("Chat loaded")
        time.sleep(5)
        
        # Click attach with JavaScript
        attach = driver.find_element(By.XPATH, '//button[@aria-label="Attach"]')
        driver.execute_script("arguments[0].click();", attach)
        print("Clicked attach")
        time.sleep(3)
        
        # Upload
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        file_input.send_keys(image_path)
        print("Uploaded image")
        time.sleep(10)
        
        # Caption & send
        caption = driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
        caption.send_keys(message)
        time.sleep(2)
        caption.send_keys(Keys.ENTER)
        
        print("✓ Sent!")
        time.sleep(8)
        
    except Exception as e:
        print(f"✗ {type(e).__name__}: {e}")
        driver.save_screenshot(f'debug_{index}.png')
        continue

driver.quit()