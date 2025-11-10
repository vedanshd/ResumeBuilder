"""
LinkedIn Profile Scraper using Playwright
Extracts profile data directly from LinkedIn URLs
"""
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import os
import time
import json


class LinkedInScraper:
    """Scrape LinkedIn profiles using Playwright automation"""
    
    def __init__(self):
        self.linkedin_email = os.getenv('LINKEDIN_EMAIL', '')
        self.linkedin_password = os.getenv('LINKEDIN_PASSWORD', '')
    
    def scrape_profile(self, linkedin_url, timeout=30000):
        """
        Scrape a LinkedIn profile from URL
        
        Args:
            linkedin_url (str): LinkedIn profile URL
            timeout (int): Timeout in milliseconds
            
        Returns:
            str: Extracted profile text content
        """
        if not self.linkedin_email or not self.linkedin_password:
            raise ValueError("LinkedIn credentials not set. Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file")
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(
                headless=True,  # Run in headless mode
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = context.new_page()
            
            try:
                # Navigate to LinkedIn login
                print("Navigating to LinkedIn...")
                page.goto('https://www.linkedin.com/login', timeout=timeout)
                
                # Login
                print("Logging in...")
                page.fill('input[name="session_key"]', self.linkedin_email)
                page.fill('input[name="session_password"]', self.linkedin_password)
                page.click('button[type="submit"]')
                
                # Wait for login to complete
                time.sleep(3)
                
                # Check if we're logged in
                if 'feed' in page.url or 'checkpoint' in page.url:
                    print("Login successful!")
                else:
                    raise Exception("Login failed - please check credentials")
                
                # Navigate to the profile URL
                print(f"Navigating to profile: {linkedin_url}")
                page.goto(linkedin_url, timeout=timeout)
                
                # Wait for profile to load
                page.wait_for_selector('h1', timeout=timeout)
                time.sleep(2)
                
                # Scroll to load all content
                print("Loading full profile...")
                for _ in range(5):
                    page.evaluate('window.scrollBy(0, 500)')
                    time.sleep(0.5)
                
                # Extract all text content
                profile_text = page.evaluate('''() => {
                    return document.body.innerText;
                }''')
                
                print("Profile extracted successfully!")
                return profile_text
                
            except PlaywrightTimeout:
                raise Exception(f"Timeout while loading page. Please check the URL and try again.")
            
            except Exception as e:
                raise Exception(f"Error scraping profile: {str(e)}")
            
            finally:
                browser.close()
    
    def scrape_profile_structured(self, linkedin_url, timeout=30000):
        """
        Scrape LinkedIn profile and extract structured data
        
        Args:
            linkedin_url (str): LinkedIn profile URL
            timeout (int): Timeout in milliseconds
            
        Returns:
            dict: Structured profile data
        """
        if not self.linkedin_email or not self.linkedin_password:
            raise ValueError("LinkedIn credentials not set. Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = context.new_page()
            
            try:
                # Login process
                print("Logging in to LinkedIn...")
                page.goto('https://www.linkedin.com/login', timeout=timeout)
                page.fill('input[name="session_key"]', self.linkedin_email)
                page.fill('input[name="session_password"]', self.linkedin_password)
                page.click('button[type="submit"]')
                time.sleep(3)
                
                # Navigate to profile
                print(f"Loading profile: {linkedin_url}")
                page.goto(linkedin_url, timeout=timeout)
                page.wait_for_selector('h1', timeout=timeout)
                time.sleep(2)
                
                # Scroll to load content
                for _ in range(5):
                    page.evaluate('window.scrollBy(0, 500)')
                    time.sleep(0.5)
                
                # Extract structured data
                profile_data = page.evaluate('''() => {
                    const data = {};
                    
                    // Name
                    const nameEl = document.querySelector('h1');
                    data.name = nameEl ? nameEl.innerText.trim() : '';
                    
                    // Headline
                    const headlineEl = document.querySelector('.text-body-medium');
                    data.headline = headlineEl ? headlineEl.innerText.trim() : '';
                    
                    // Location
                    const locationEl = document.querySelector('.text-body-small.inline.t-black--light');
                    data.location = locationEl ? locationEl.innerText.trim() : '';
                    
                    // About
                    const aboutEl = document.querySelector('#about + * .inline-show-more-text');
                    data.about = aboutEl ? aboutEl.innerText.trim() : '';
                    
                    // Experience
                    const experiences = [];
                    document.querySelectorAll('#experience + * li').forEach(exp => {
                        const titleEl = exp.querySelector('.t-bold span[aria-hidden="true"]');
                        const companyEl = exp.querySelector('.t-14 span[aria-hidden="true"]');
                        const durationEl = exp.querySelector('.t-14.t-normal span[aria-hidden="true"]');
                        
                        if (titleEl) {
                            experiences.push({
                                title: titleEl.innerText.trim(),
                                company: companyEl ? companyEl.innerText.trim() : '',
                                duration: durationEl ? durationEl.innerText.trim() : ''
                            });
                        }
                    });
                    data.experience = experiences;
                    
                    // Education
                    const education = [];
                    document.querySelectorAll('#education + * li').forEach(edu => {
                        const schoolEl = edu.querySelector('.t-bold span[aria-hidden="true"]');
                        const degreeEl = edu.querySelector('.t-14 span[aria-hidden="true"]');
                        
                        if (schoolEl) {
                            education.push({
                                school: schoolEl.innerText.trim(),
                                degree: degreeEl ? degreeEl.innerText.trim() : ''
                            });
                        }
                    });
                    data.education = education;
                    
                    // Skills
                    const skills = [];
                    document.querySelectorAll('#skills + * .artdeco-list__item').forEach(skill => {
                        const skillText = skill.querySelector('span[aria-hidden="true"]');
                        if (skillText) {
                            skills.push(skillText.innerText.trim());
                        }
                    });
                    data.skills = skills;
                    
                    return data;
                }''')
                
                print("Structured data extracted successfully!")
                return profile_data
                
            except Exception as e:
                raise Exception(f"Error extracting structured data: {str(e)}")
            
            finally:
                browser.close()


# Test function
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    scraper = LinkedInScraper()
    
    # Test with a public profile URL
    test_url = "https://www.linkedin.com/in/williamhgates/"
    
    try:
        text_data = scraper.scrape_profile(test_url)
        print("\\n=== Text Extraction ===")
        print(text_data[:500] + "...")
        
        print("\\n=== Structured Extraction ===")
        structured_data = scraper.scrape_profile_structured(test_url)
        print(json.dumps(structured_data, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
