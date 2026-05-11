from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

messages = [
    """
কোরবানি হোক একদম ঝামেলামুক্ত!
কসাই ভাইদের জন্য: বেশি কাজ আর বাড়তি আয়ের সুযোগ! আজই ফ্রি রেজিস্ট্রেশন করুন: koshailagbe.devadda.site
কাস্টমারদের জন্য: শেষ মূহূর্তে কসাই খোঁজার টেনশন আর নয়। আপনার এলাকাতেই দক্ষ কসাই খুঁজে পেতে ভিজিট করুন আমাদের সাইটে। কসাই এবং কাস্টমারের সেরা মিলনমেলা—এখন এক ক্লিকেই!
""",
    """
কোরবানি হোক টেনশনমুক্ত!
কোরবানির ঈদে কসাই নিয়ে আর চিন্তা নেই। কসাই ভাইরা কাজ পেতে রেজিস্ট্রেশন করুন, আর কাস্টমাররা সেরা কসাই খুঁজে নিন আমাদের প্ল্যাটফর্মে।
ভিজিট করুন: koshailagbe.devadda.site
কসাই এবং কাস্টমারের মেলবন্ধন—এক ক্লিকেই সব সমাধান!
""",
    """
কোরবানি হোক টেনশনমুক্ত!
কোরবানির ঈদে কসাই নিয়ে আর চিন্তা নেই। কসাই ভাইরা কাজ পেতে রেজিস্ট্রেশন করুন, আর কাস্টমাররা সেরা কসাই খুঁজে নিন আমাদের প্ল্যাটফর্মে। ভিজিট করুন: koshailagbe.devadda.site
কসাই এবং কাস্টমারের মেলবন্ধন—এক ক্লিকেই সব সমাধান!
"""
]

# image_path = "/home/nahid/Projects/butcher-scrapper/promo.jpeg"

DAILY_LIMIT = 20  # Send to only 20 people

df = pd.read_excel('results/Dhaka.xlsx')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://web.whatsapp.com')
print("Scan QR code and press Enter...")
input()

sent_count = 0

for index, row in df.iterrows():
    if sent_count >= DAILY_LIMIT:
        print(f"\n✓ Daily limit reached ({DAILY_LIMIT} messages sent). Stopping...")
        break
    
    try:
        phone = str(row['Phone']).strip().replace(' ', '').replace('-', '')
        
        if len(phone) == 10 and not phone.startswith('0'):
            phone = '0' + phone
        if phone.startswith('0'):
            phone = phone[1:]
        
        full_number = f'880{phone}'
        print(f"\n[{sent_count+1}/{DAILY_LIMIT}] {row['Name']} → {full_number}")
        
        driver.get(f'https://web.whatsapp.com/send?phone={full_number}')
        
        # Wait for chat to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        print("Chat loaded")
        time.sleep(5)
        
        # Rotate messages (0, 1, 2, 0, 1, 2...)
        current_message = messages[sent_count % 3]
        
        # Send message only
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.send_keys(current_message)
        time.sleep(2)
        message_box.send_keys(Keys.ENTER)
        
        print("✓ Sent!")
        sent_count += 1
        time.sleep(8)
        
    except Exception as e:
        print(f"✗ {type(e).__name__}: {e}")
        driver.save_screenshot(f'debug_{index}.png')
        continue

driver.quit()
print(f"\n✓ Complete! Sent {sent_count} messages.")