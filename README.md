# LinkedIn Resume Builder

A simple Python web application that generates professional PDF resumes from LinkedIn profile content.

## ✨ Features

- 📋 **Copy & Paste** - No scraping, no authentication needed
- 🤖 **AI-Powered** - Optional Gemini AI for intelligent parsing
- 🔒 **100% Private** - Your data is processed locally, not stored
- 📄 **Professional PDFs** - Clean, formatted resume output
- ⚡ **Fast & Simple** - Generate in seconds
- 🎯 **Smart Fallback** - Works with or without API keys

## 🚀 Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **(Optional) Get Gemini API Key for better parsing**
   - Visit: https://makersuite.google.com/app/apikey
   - Create a free API key
   - Add to `.env` file: `GEMINI_API_KEY=your-key-here`
   - See [GEMINI_SETUP.md](GEMINI_SETUP.md) for details

3. **Run the app**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://localhost:8080
   ```

4. **Generate your resume:**
   - Go to any LinkedIn profile
   - Press `Ctrl+A` (or `Cmd+A` on Mac) to select all
   - Press `Ctrl+C` (or `Cmd+C`) to copy
   - Paste into the text box
   - Click "Generate Resume"
   - Download your PDF!

## 💡 How It Works

### With Gemini AI (Recommended):
1. You copy LinkedIn profile text (Ctrl+A, Ctrl+C)
2. Paste into the text box
3. **Gemini AI intelligently extracts and formats:**
   - Name, headline, contact info
   - Work experience with descriptions
   - Education with degrees and dates
   - Skills and achievements
4. Resume generator creates a professional PDF

### Without Gemini (Fallback):
1. Same copy-paste process
2. Regex-based parser extracts basic structure
3. Still generates a working resume (just less accurate)

**The app automatically uses Gemini if you have an API key, otherwise falls back to regex parsing!**

## Features

- 🔍 Scrapes LinkedIn profile data automatically
- 📄 Generates clean, professional PDF resumes
- 🎨 Modern web interface
- ⬇️ Downloadable PDF output
- 🚀 Easy to use - just paste your LinkedIn URL

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Scraping**: Selenium WebDriver
- **PDF Generation**: ReportLab
- **Frontend**: HTML, CSS, JavaScript

## Prerequisites

- Python 3.8 or higher
- Chrome browser (for Selenium WebDriver)
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd /Users/vedanshdhawan/ResumeBuilder
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Flask application**
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Enter your LinkedIn profile URL** in the format:
   ```
   https://www.linkedin.com/in/your-profile-name
   ```

4. **Click "Generate Resume"** and wait for the scraping process to complete

5. **Download your PDF resume** using the download button

## Project Structure

```
ResumeBuilder/
├── app.py                  # Flask application main file
├── scraper.py             # LinkedIn scraping logic
├── resume_generator.py    # PDF generation logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend JavaScript
└── generated_resumes/    # Output folder for PDFs (auto-created)
```

## Important Notes

⚠️ **LinkedIn Profile Privacy**: Your LinkedIn profile must be set to public for the scraper to access your information. Private profiles cannot be scraped.

⚠️ **LinkedIn Scraping Methods**:

### Method 1: Test Mode (Recommended for Demo)
- Type `test` or `demo` as the URL
- Generates resume with sample data
- No LinkedIn interaction

### Method 2: Login-Based Scraping (May Work, but Risky)
1. Copy `.env.example` to `.env`
2. Add your LinkedIn email and password
3. The scraper will login and extract data
4. ⚠️ **WARNING**: This may violate LinkedIn's Terms of Service and get your account banned!

### Method 3: Alternative Solutions
- **LinkedIn Official API**: Requires developer approval (very limited access)
- **Proxycurl API**: Paid service ($49/month) but very reliable
- **Manual Data Entry**: Safest option (I can add a form for this)
- **Browser Extension**: Copy profile HTML and parse locally

⚠️ **Rate Limiting**: LinkedIn may rate-limit or block automated scraping. Use responsibly and at your own risk.

⚠️ **Selenium Requirements**: The scraper uses Chrome WebDriver. Chrome browser must be installed on your system.

## Dependencies

- Flask==3.0.0
- selenium==4.15.2
- beautifulsoup4==4.12.2
- reportlab==4.0.7
- python-dotenv==1.0.0
- Pillow==10.1.0
- webdriver-manager==4.0.1

## Troubleshooting

### Chrome Driver Issues
If you encounter Chrome driver errors:
- Ensure Chrome browser is installed
- The `webdriver-manager` package should automatically download the correct driver
- Check your Chrome version matches the driver version

### Scraping Fails
If scraping doesn't work:
- Verify the LinkedIn URL is correct and accessible
- Ensure your profile is set to public
- LinkedIn's HTML structure may change - CSS selectors might need updates
- Check your internet connection

### Import Errors
If you see import errors:
```bash
pip install --upgrade -r requirements.txt
```

## Future Enhancements

- [ ] Add authentication for private profiles
- [ ] Support multiple resume templates
- [ ] Add customization options (colors, fonts, sections)
- [ ] Export to different formats (DOCX, HTML)
- [ ] Bulk processing for multiple profiles
- [ ] Resume preview before download

## License

This project is for educational purposes. Please respect LinkedIn's Terms of Service and robots.txt when using this tool.

## Contributing

Feel free to fork this project and submit pull requests with improvements!

## Support

For issues or questions, please create an issue in the repository.

---

**Note**: This tool is intended for personal use only. Always ensure you have permission to scrape and use someone's LinkedIn data.
