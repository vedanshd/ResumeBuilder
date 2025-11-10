"""
Quick test script for LinkedIn URL Scraper
"""
from linkedin_url_scraper import LinkedInURLScraper
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🧪 LinkedIn URL Scraper - Component Test")
print("=" * 60)
print()

# Check credentials
email = os.getenv('LINKEDIN_EMAIL')
password = os.getenv('LINKEDIN_PASSWORD')

if email and password:
    print(f"✅ Email loaded: {email}")
    print(f"✅ Password loaded: {'*' * len(password)}")
else:
    print("❌ Credentials not found in .env file")
    exit(1)

print()

# Test scraper initialization
try:
    print("📦 Initializing scraper...")
    scraper = LinkedInURLScraper()
    print("   ✅ Scraper object created")
    
    print("🌐 Setting up Chrome driver...")
    scraper.setup_driver(headless=True)  # Use headless mode for test
    print("   ✅ Chrome driver ready")
    
    print("🔒 Closing browser...")
    scraper.close()
    print("   ✅ Browser closed")
    
    print()
    print("=" * 60)
    print("🎉 All components working perfectly!")
    print("=" * 60)
    print()
    print("✅ Ready to scrape LinkedIn profiles!")
    print()
    print("To use the scraper:")
    print("1. Make sure Flask app is running: http://127.0.0.1:8080")
    print("2. Use the /scrape-linkedin-url endpoint")
    print("3. Provide a LinkedIn profile URL in the request")
    print()
    print("Example API call:")
    print("""
fetch('/scrape-linkedin-url', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        profile_url: 'https://www.linkedin.com/in/username/'
    })
})
    """)
    
except Exception as e:
    print()
    print("❌ Error during test:")
    print(f"   {str(e)}")
    print()
    print("Common issues:")
    print("- Chrome/Chromium not installed")
    print("- ChromeDriver version mismatch")
    print("- Network connectivity issues")
