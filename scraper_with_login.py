from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv

load_dotenv()


class LinkedInScraperWithLogin:
    """
    LinkedIn scraper that uses login credentials
    WARNING: This may violate LinkedIn's Terms of Service
    Use at your own risk. LinkedIn may block or ban your account.
    """
    
    def __init__(self, email=None, password=None):
        """Initialize with LinkedIn credentials"""
        self.driver = None
        self.email = email or os.getenv('LINKEDIN_EMAIL')
        self.password = password or os.getenv('LINKEDIN_PASSWORD')
        
    def setup_driver(self, headless=False):
        """Set up Chrome WebDriver with options"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Add user agent to look more like a real browser
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            # Try without service
            self.driver = webdriver.Chrome(options=chrome_options)
        
    def login(self):
        """Login to LinkedIn"""
        try:
            print("Logging into LinkedIn...")
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(2)
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'username'))
            )
            email_field.send_keys(self.email)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, 'password')
            password_field.send_keys(self.password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            
            # Check if login was successful
            if 'feed' in self.driver.current_url or 'checkpoint' in self.driver.current_url:
                print("Login successful!")
                return True
            else:
                print("Login may have failed. Check credentials.")
                return False
                
        except Exception as e:
            print(f"Login error: {str(e)}")
            return False
    
    def scrape_profile(self, linkedin_url):
        """
        Scrape LinkedIn profile after logging in
        
        Args:
            linkedin_url (str): LinkedIn profile URL
            
        Returns:
            dict: Profile data
        """
        if not self.email or not self.password:
            print("ERROR: LinkedIn credentials not provided!")
            print("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file")
            return None
        
        try:
            self.setup_driver(headless=False)  # Set to True for background mode
            
            # Login first
            if not self.login():
                return None
            
            # Navigate to profile
            print(f"Navigating to profile: {linkedin_url}")
            self.driver.get(linkedin_url)
            time.sleep(5)
            
            # Scroll to load all content
            self._scroll_page()
            
            profile_data = {
                'name': self._get_name(),
                'headline': self._get_headline(),
                'about': self._get_about(),
                'experience': self._get_experience(),
                'education': self._get_education(),
                'skills': self._get_skills(),
                'contact': self._get_contact_info()
            }
            
            return profile_data
            
        except Exception as e:
            print(f"Error scraping profile: {str(e)}")
            return None
            
        finally:
            if self.driver:
                time.sleep(2)
                self.driver.quit()
    
    def _scroll_page(self):
        """Scroll to load dynamic content"""
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        except:
            pass
    
    def _get_name(self):
        """Extract profile name"""
        try:
            # Try multiple selectors
            selectors = [
                'h1.text-heading-xlarge',
                'h1.inline.t-24.v-align-middle.break-words',
                'div.mt2.relative h1'
            ]
            
            for selector in selectors:
                try:
                    name = self.driver.find_element(By.CSS_SELECTOR, selector).text
                    if name:
                        return name.strip()
                except:
                    continue
                    
        except Exception as e:
            print(f"Error getting name: {str(e)}")
        
        return "Name Not Found"
    
    def _get_headline(self):
        """Extract profile headline"""
        try:
            selectors = [
                'div.text-body-medium.break-words',
                'div.mt1.text-body-medium',
                'h2.mt1.t-18'
            ]
            
            for selector in selectors:
                try:
                    headline = self.driver.find_element(By.CSS_SELECTOR, selector).text
                    if headline:
                        return headline.strip()
                except:
                    continue
                    
        except Exception as e:
            print(f"Error getting headline: {str(e)}")
        
        return ""
    
    def _get_about(self):
        """Extract about section"""
        try:
            # Click "Show more" if present
            try:
                show_more = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'more in About section')]")
                show_more.click()
                time.sleep(1)
            except:
                pass
            
            selectors = [
                'section.artdeco-card div.display-flex.ph5.pv3 span[aria-hidden="true"]',
                'div.pv-about__summary-text span',
                'section#about ~ div span'
            ]
            
            for selector in selectors:
                try:
                    about = self.driver.find_element(By.CSS_SELECTOR, selector).text
                    if about:
                        return about.strip()
                except:
                    continue
                    
        except Exception as e:
            print(f"Error getting about: {str(e)}")
        
        return ""
    
    def _get_experience(self):
        """Extract work experience"""
        experiences = []
        try:
            # Try to find experience section
            exp_elements = self.driver.find_elements(By.CSS_SELECTOR, 'section#experience ~ div li.artdeco-list__item')
            
            if not exp_elements:
                exp_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.pvs-list__item--line-separated')
            
            for exp in exp_elements[:5]:  # Limit to 5
                try:
                    title = exp.find_element(By.CSS_SELECTOR, 'span[aria-hidden="true"]').text
                    company = exp.find_elements(By.CSS_SELECTOR, 'span[aria-hidden="true"]')[1].text if len(exp.find_elements(By.CSS_SELECTOR, 'span[aria-hidden="true"]')) > 1 else ""
                    duration = exp.find_elements(By.CSS_SELECTOR, 'span[aria-hidden="true"]')[2].text if len(exp.find_elements(By.CSS_SELECTOR, 'span[aria-hidden="true"]')) > 2 else ""
                    
                    experiences.append({
                        'title': title,
                        'company': company,
                        'duration': duration,
                        'description': ''
                    })
                except:
                    continue
                    
        except Exception as e:
            print(f"Error getting experience: {str(e)}")
        
        return experiences
    
    def _get_education(self):
        """Extract education information"""
        education = []
        try:
            edu_elements = self.driver.find_elements(By.CSS_SELECTOR, 'section#education ~ div li.artdeco-list__item')
            
            for edu in edu_elements:
                try:
                    texts = edu.find_elements(By.CSS_SELECTOR, 'span[aria-hidden="true"]')
                    
                    school = texts[0].text if len(texts) > 0 else ""
                    degree = texts[1].text if len(texts) > 1 else ""
                    dates = texts[2].text if len(texts) > 2 else ""
                    
                    education.append({
                        'school': school,
                        'degree': degree,
                        'field': '',
                        'dates': dates
                    })
                except:
                    continue
                    
        except Exception as e:
            print(f"Error getting education: {str(e)}")
        
        return education
    
    def _get_skills(self):
        """Extract skills"""
        skills = []
        try:
            skill_elements = self.driver.find_elements(By.CSS_SELECTOR, 'section#skills ~ div span[aria-hidden="true"]')
            
            for skill in skill_elements[:10]:  # Limit to 10
                try:
                    skill_text = skill.text.strip()
                    if skill_text and len(skill_text) < 50:
                        skills.append(skill_text)
                except:
                    continue
                    
        except Exception as e:
            print(f"Error getting skills: {str(e)}")
        
        return list(set(skills))[:10]  # Remove duplicates
    
    def _get_contact_info(self):
        """Extract contact information"""
        contact = {
            'email': '',
            'phone': '',
            'location': ''
        }
        
        try:
            location = self.driver.find_element(By.CSS_SELECTOR, 'span.text-body-small.inline').text
            contact['location'] = location.strip()
        except:
            pass
        
        return contact
