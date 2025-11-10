"""
LinkedIn URL Scraper using Selenium
Scrapes LinkedIn profile data from a profile URL using browser automation
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv
from linkedin_parser import LinkedInParser

load_dotenv()


class LinkedInURLScraper:
    """Scrape LinkedIn profiles from URLs using Selenium"""
    
    def __init__(self):
        """Initialize the scraper"""
        self.driver = None
        self.parser = LinkedInParser()
        
    def setup_driver(self, headless=True):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless=new')
        
        # Anti-detection measures
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Disable automation flags
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize driver - let webdriver-manager handle the driver
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            # Get driver path
            driver_path = ChromeDriverManager().install()
            
            # Fix for macOS ARM64 chromedriver path issue
            if 'THIRD_PARTY_NOTICES' in driver_path:
                import os
                driver_dir = os.path.dirname(driver_path)
                # Look for actual chromedriver executable
                for file in os.listdir(driver_dir):
                    if file == 'chromedriver' and os.access(os.path.join(driver_dir, file), os.X_OK):
                        driver_path = os.path.join(driver_dir, file)
                        break
            
            service = Service(executable_path=driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Failed with webdriver-manager: {e}")
            print("Trying system chromedriver...")
            # Fallback to system chromedriver
            self.driver = webdriver.Chrome(options=chrome_options)
        
        # Execute script to hide webdriver
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Chrome driver initialized")
        
    def login_to_linkedin(self, email=None, password=None):
        """
        Login to LinkedIn (required to view full profiles)
        
        Args:
            email (str): LinkedIn email/username
            password (str): LinkedIn password
        """
        if not email:
            email = os.getenv('LINKEDIN_EMAIL')
        if not password:
            password = os.getenv('LINKEDIN_PASSWORD')
            
        if not email or not password:
            raise ValueError("LinkedIn credentials not provided. Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file")
        
        try:
            print("🔐 Logging into LinkedIn...")
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(2)
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'username'))
            )
            email_field.send_keys(email)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, 'password')
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()
            
            # Wait for redirect to feed or handle 2FA
            time.sleep(5)
            
            # Check if login successful
            if 'feed' in self.driver.current_url or 'checkpoint' in self.driver.current_url:
                if 'checkpoint' in self.driver.current_url:
                    print("⚠️  2FA/Security check detected. Please complete manually in the browser window.")
                    print("   Waiting 30 seconds for manual completion...")
                    time.sleep(30)
                
                print("✅ Logged in successfully")
                return True
            else:
                print("❌ Login failed. Check credentials.")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False
    
    def scrape_profile(self, profile_url, login_required=True, email=None, password=None):
        """
        Scrape a LinkedIn profile from URL
        
        Args:
            profile_url (str): Full LinkedIn profile URL
            login_required (bool): Whether to login first (recommended)
            email (str, optional): LinkedIn email
            password (str, optional): LinkedIn password
            
        Returns:
            dict: Parsed profile data
        """
        try:
            # Setup driver
            if not self.driver:
                self.setup_driver(headless=False)  # Set to True for production
            
            # Login if required
            if login_required:
                if not self.login_to_linkedin(email, password):
                    raise Exception("Failed to login to LinkedIn")
            
            # Navigate to profile
            print(f"🌐 Navigating to profile: {profile_url}")
            self.driver.get(profile_url)
            time.sleep(3)
            
            # Scroll to load all content
            print("📜 Scrolling to load content...")
            self._scroll_page()
            
            # Click "Show more" buttons
            self._expand_sections()
            
            # Extract page source
            page_source = self.driver.page_source
            
            # Also get text content
            body_text = self.driver.find_element(By.TAG_NAME, 'body').text
            
            print("✅ Profile data extracted")
            
            # Parse the extracted text using LinkedInParser
            profile_data = self.parser.parse_linkedin_text(body_text)
            
            return profile_data
            
        except Exception as e:
            print(f"❌ Scraping error: {str(e)}")
            return None
        
    def _scroll_page(self):
        """Scroll the page to load all dynamic content"""
        try:
            # Get initial height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Scroll in increments
            for i in range(5):  # Scroll 5 times
                # Scroll down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Calculate new height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                # Break if no new content loaded
                if new_height == last_height:
                    break
                    
                last_height = new_height
                
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
        except Exception as e:
            print(f"⚠️  Scroll error: {str(e)}")
    
    def _expand_sections(self):
        """Click 'Show more' buttons to expand sections"""
        try:
            # Find and click all "Show more" / "See more" buttons
            show_more_buttons = self.driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'Show more') or contains(text(), 'See more') or contains(@aria-label, 'Show more')]")
            
            print(f"📋 Found {len(show_more_buttons)} expandable sections")
            
            for button in show_more_buttons[:10]:  # Limit to first 10 to avoid issues
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(0.5)
                    button.click()
                    time.sleep(0.5)
                except:
                    pass  # Some buttons may not be clickable
                    
        except Exception as e:
            print(f"⚠️  Expand sections error: {str(e)}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def scrape_linkedin_url(profile_url, email=None, password=None):
    """
    Helper function to scrape a LinkedIn profile URL
    
    Args:
        profile_url (str): LinkedIn profile URL
        email (str, optional): LinkedIn email
        password (str, optional): LinkedIn password
        
    Returns:
        dict: Parsed profile data
    """
    with LinkedInURLScraper() as scraper:
        profile_data = scraper.scrape_profile(profile_url, login_required=True, email=email, password=password)
        return profile_data


# Example usage
if __name__ == "__main__":
    # Test the scraper
    test_url = "https://www.linkedin.com/in/example/"
    
    print("🚀 Starting LinkedIn URL Scraper Test")
    print("=" * 50)
    
    profile = scrape_linkedin_url(test_url)
    
    if profile:
        print("\n✅ Profile scraped successfully!")
        print(f"Name: {profile.get('name', 'N/A')}")
        print(f"Headline: {profile.get('headline', 'N/A')}")
        print(f"Experience: {len(profile.get('experience', []))} positions")
        print(f"Education: {len(profile.get('education', []))} degrees")
        print(f"Skills: {len(profile.get('skills', []))} skills")
    else:
        print("\n❌ Failed to scrape profile")
