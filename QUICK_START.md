# LinkedIn Resume Builder - Quick Start Guide

## Setup Login-Based Scraping

### Step 1: Create your .env file

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` in your editor and add your LinkedIn credentials:
   ```
   LINKEDIN_EMAIL=your-actual-email@example.com
   LINKEDIN_PASSWORD=your-actual-password
   ```

### Step 2: Restart the Flask Application

The server should auto-reload, but if not:
1. Stop the server (Ctrl+C in terminal)
2. Start it again:
   ```bash
   python app.py
   ```

### Step 3: Test It

1. Go to `http://localhost:8080`
2. Enter a LinkedIn profile URL (e.g., `https://www.linkedin.com/in/williamhgates`)
3. Click "Generate Resume"
4. Wait (it will take 10-20 seconds as it logs in and scrapes)
5. Download your PDF!

---

## ⚠️ Important Warnings

### Security Risks:
- **Your LinkedIn password is stored in plain text** in the `.env` file
- Make sure `.env` is in `.gitignore` (it already is)
- Never commit your `.env` file to git
- Consider using a burner LinkedIn account for testing

### Account Risks:
- LinkedIn **may detect** automated activity
- Your account **could be temporarily or permanently banned**
- LinkedIn may ask you to verify CAPTCHA or 2FA
- Use at your own risk!

### When It Won't Work:
- ❌ If LinkedIn shows CAPTCHA
- ❌ If you have 2FA enabled on LinkedIn
- ❌ If LinkedIn detects automation
- ❌ If your credentials are wrong

---

## Troubleshooting

### "Login failed"
- Check your email/password in `.env`
- Disable 2FA on your LinkedIn account temporarily
- Make sure there are no extra spaces in `.env`

### "CAPTCHA detected"
- LinkedIn is blocking automation
- Try again later or use a different account
- Consider using "test" mode or manual entry instead

### Browser window opens but nothing happens
- The scraper is working - wait 20-30 seconds
- Check the terminal for debug messages
- The browser will close when done

### Still doesn't work?
- Try "test" mode to verify the PDF generation works
- Check terminal output for error messages
- LinkedIn's HTML structure may have changed (would need to update selectors)

---

## Alternative: Use Test Mode

If scraping doesn't work, you can always use test mode:
1. Enter `test` or `demo` as the URL
2. Get a sample resume instantly
3. No LinkedIn account needed!

---

## Next Steps

Once you have scraping working:
- Test with different LinkedIn profiles
- Customize the resume template
- Add more fields or formatting options

**Remember**: This is for educational/personal use only. Respect LinkedIn's Terms of Service!
