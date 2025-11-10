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


class LinkedInScraper:
    """Scraper for LinkedIn profiles"""
    
    def __init__(self):
        """Initialize the scraper with Chrome driver"""
        self.driver = None
        self.use_login = os.getenv('LINKEDIN_EMAIL') and os.getenv('LINKEDIN_PASSWORD')
        
    def setup_driver(self):
        """Set up Chrome WebDriver with options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            # Try without service  
            self.driver = webdriver.Chrome(options=chrome_options)
        
    def scrape_profile(self, linkedin_url):
        """
        Scrape LinkedIn profile data
        
        Args:
            linkedin_url (str): LinkedIn profile URL
            
        Returns:
            dict: Profile data including name, headline, experience, education, skills
        """
        # For testing: Use sample data only if explicitly requested
        if linkedin_url.lower().strip() in ['test', 'demo']:
            return self._get_sample_data()
        
        # If credentials are provided, use login-based scraping
        if self.use_login:
            return self._scrape_with_login(linkedin_url)
        
        # Otherwise try without login (will likely fail)
        try:
            self.setup_driver()
            self.driver.get(linkedin_url)
            time.sleep(5)  # Wait for page to load
            
            # Save page source for debugging
            print(f"Page title: {self.driver.title}")
            
            profile_data = {
                'name': self._get_name(),
                'headline': self._get_headline(),
                'about': self._get_about(),
                'experience': self._get_experience(),
                'education': self._get_education(),
                'skills': self._get_skills(),
                'contact': self._get_contact_info()
            }
            
            # Check if we got any data
            if profile_data['name'] == "Name Not Found":
                print("Warning: Could not extract profile data from LinkedIn.")
                return None
            
            return profile_data
            
        except Exception as e:
            print(f"Error scraping profile: {str(e)}")
            return None
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def _scrape_with_login(self, linkedin_url):
        """Scrape using login credentials"""
        from scraper_with_login import LinkedInScraperWithLogin
        
        email = os.getenv('LINKEDIN_EMAIL')
        password = os.getenv('LINKEDIN_PASSWORD')
        
        scraper = LinkedInScraperWithLogin(email, password)
        return scraper.scrape_profile(linkedin_url)
    
    def _get_sample_data(self):
        """Return sample profile data for testing"""
        return {
            'name': 'John Doe',
            'headline': 'Senior Software Engineer | Full Stack Developer | Tech Enthusiast',
            'about': 'Experienced software engineer with 5+ years of expertise in building scalable web applications. Passionate about clean code, modern technologies, and solving complex problems. Skilled in Python, JavaScript, and cloud technologies.',
            'experience': [
                {
                    'title': 'Senior Software Engineer',
                    'company': 'Tech Company Inc.',
                    'duration': 'Jan 2022 - Present',
                    'description': '• Led development of microservices architecture serving 1M+ users\n• Improved application performance by 40% through optimization\n• Mentored junior developers and conducted code reviews'
                },
                {
                    'title': 'Software Engineer',
                    'company': 'StartUp Solutions',
                    'duration': 'Jun 2019 - Dec 2021',
                    'description': '• Built RESTful APIs using Python Flask and Django\n• Implemented CI/CD pipelines reducing deployment time by 60%\n• Collaborated with cross-functional teams on product features'
                }
            ],
            'education': [
                {
                    'school': 'University of Technology',
                    'degree': 'Bachelor of Science',
                    'field': 'Computer Science',
                    'dates': '2015 - 2019'
                }
            ],
            'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker', 'PostgreSQL', 'Git', 'Agile', 'REST APIs'],
            'contact': {
                'email': 'john.doe@email.com',
                'phone': '+1 (555) 123-4567',
                'location': 'San Francisco, CA'
            }
        }
    
    def _get_name(self):
        """Extract profile name"""
        try:
            name = self.driver.find_element(By.CSS_SELECTOR, 'h1.text-heading-xlarge').text
            return name
        except:
            return "Name Not Found"
    
    def _get_headline(self):
        """Extract profile headline"""
        try:
            headline = self.driver.find_element(By.CSS_SELECTOR, 'div.text-body-medium').text
            return headline
        except:
            return ""
    
    def _get_about(self):
        """Extract about section"""
        try:
            about = self.driver.find_element(By.CSS_SELECTOR, 'section.artdeco-card div.display-flex.ph5.pv3').text
            return about
        except:
            return ""
    
    def _get_experience(self):
        """Extract work experience"""
        experiences = []
        try:
            exp_section = self.driver.find_elements(By.CSS_SELECTOR, 'section#experience-section ul > li')
            
            for exp in exp_section[:5]:  # Limit to 5 most recent
                try:
                    title = exp.find_element(By.CSS_SELECTOR, 'h3').text
                    company = exp.find_element(By.CSS_SELECTOR, 'p.pv-entity__secondary-title').text
                    duration = exp.find_element(By.CSS_SELECTOR, 'h4.pv-entity__date-range span:nth-child(2)').text
                    description = ""
                    try:
                        description = exp.find_element(By.CSS_SELECTOR, 'div.pv-entity__description').text
                    except:
                        pass
                    
                    experiences.append({
                        'title': title,
                        'company': company,
                        'duration': duration,
                        'description': description
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
            edu_section = self.driver.find_elements(By.CSS_SELECTOR, 'section#education-section ul > li')
            
            for edu in edu_section:
                try:
                    school = edu.find_element(By.CSS_SELECTOR, 'h3').text
                    degree = edu.find_element(By.CSS_SELECTOR, 'p.pv-entity__degree-name span:nth-child(2)').text
                    field = ""
                    try:
                        field = edu.find_element(By.CSS_SELECTOR, 'p.pv-entity__fos span:nth-child(2)').text
                    except:
                        pass
                    dates = ""
                    try:
                        dates = edu.find_element(By.CSS_SELECTOR, 'p.pv-entity__dates span:nth-child(2)').text
                    except:
                        pass
                    
                    education.append({
                        'school': school,
                        'degree': degree,
                        'field': field,
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
            skills_section = self.driver.find_elements(By.CSS_SELECTOR, 'section.pv-skill-categories-section ol > li')
            
            for skill in skills_section[:10]:  # Limit to 10 skills
                try:
                    skill_name = skill.find_element(By.CSS_SELECTOR, 'p.pv-skill-category-entity__name').text
                    skills.append(skill_name)
                except:
                    continue
                    
        except Exception as e:
            print(f"Error getting skills: {str(e)}")
            
        return skills
    
    def _get_contact_info(self):
        """Extract contact information"""
        contact = {
            'email': '',
            'phone': '',
            'location': ''
        }
        
        try:
            location = self.driver.find_element(By.CSS_SELECTOR, 'span.text-body-small.inline').text
            contact['location'] = location
        except:
            pass
            
        return contact
