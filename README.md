ZeroCost-LeadGen-Engine
Automate your B2B outreach from Map to Message for $0.

This project is an end-to-end Python pipeline designed to bypass expensive lead-generation tools. It crawls Google Maps for restaurant data across 64 districts, cleans the data into professional Excel reports, and automates personalized WhatsApp outreach using Selenium.

Project Structure

```
ZeroCost-LeadGen-Engine/
├── venv/                    # Isolated Python environment
├── scraper_all.py           # The "Data Miner": Multi-district crawler
├── whatsapp_sender.py       # The "Messenger": Automated outreach engine
├── districts.txt            # Targeting list: (e.g., list of 64 districts)
├── promo.jpeg               # Marketing flyer to be attached in WhatsApp
└── results/                 # Output directory for leads
    ├── .gitkeep             # Keeps folder in Git while ignoring data
    ├── Dhaka.xlsx           # Sample district-specific lead data
    └── ALL_DISTRICTS.xlsx   # Combined Master Database
```

 The Tech Stack: Why These Tools?
To keep this project Zero-Cost, we utilize a specific "Digital Workforce" of open-source libraries:

Selenium: Essential for SPAs (Single Page Applications). It simulates real human interaction (scrolling/clicking) to render dynamic content that standard scrapers can't see.

Pandas: The "Data Scientist’s Swiss Army Knife." It performs vectorized operations to clean malformed phone numbers and merge 64+ datasets in seconds.

Webdriver-Manager: Ensures environment stability by automatically syncing the Chrome driver with your current browser version. No manual downloads required.

Openpyxl: A standalone engine that writes professional .xlsx files without requiring a paid Microsoft Office license.

Getting Started

1. Installation
Clone the repository and install the dependencies:
```
Bash
# Clone the repo
git clone https://github.com/yourusername/ZeroCost-LeadGen-Engine.git
cd ZeroCost-LeadGen-Engine

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install selenium pandas webdriver-manager openpyxl
```
2. Data Collection
Add your target regions to districts.txt and run the crawler:
```
Bash
python scraper_all.py
```
The script will iterate through every district, scroll through Google Maps results, and save individual Excel files in the /results folder.

3. Automated Outreach
Place your promotional image as promo.jpeg.

Update the message variable in whatsapp_sender.py.

Run the sender:
```
Bash
python whatsapp_sender.py
```
Note: You will be prompted to scan the WhatsApp Web QR code once. The script handles the rest.

Dev Perspective: How it Works
The Infinite Scroll Hack
Google Maps lazy-loads results. The scraper injects JavaScript to force-scroll the results pane:
```
Python
scrollable = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable)
```
Data Sanitization
Using Pandas, we ensure every phone number follows the international format required for WhatsApp URL schemes, removing spaces, dashes, and local prefixes automatically.

Ethical Use & Limitations
Rate Limiting: This tool includes time.sleep() intervals to mimic human behavior. Do not remove these, or you risk an IP ban.

Anti-Spam: WhatsApp has strict policies. It is recommended to send no more than 200-300 messages per day to avoid account flagging.

Disclaimer: This project is for educational and legitimate B2B marketing purposes only.

 Contributing
Found a bug or want to add a feature (like Telegram support)? Feel free to fork and submit a PR!

Built with for Growth Hackers and Devs.