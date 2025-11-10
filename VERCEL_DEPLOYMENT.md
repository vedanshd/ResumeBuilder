# Vercel Deployment Guide

## ✅ Configuration Complete!

Your code is now configured for Vercel deployment. The changes include:

1. ✅ **vercel.json** - Vercel deployment configuration
2. ✅ **app.py** - Modified for serverless compatibility
3. ✅ **generated_resumes/.gitkeep** - Ensures directory exists
4. ✅ **.gitignore** - Updated to exclude virtual environments

---

## 🔧 Important: Add Environment Variables to Vercel

**Your app will NOT work without setting up environment variables!**

### Steps to Add Environment Variables:

1. Go to your Vercel project dashboard:
   - https://vercel.com/vedanshd/resumebuilder (or your project URL)

2. Click **Settings** → **Environment Variables**

3. Add the following variable:

   | Name | Value |
   |------|-------|
   | `GEMINI_API_KEY` | Your Google Gemini API key |

4. **Important**: Select **All Environments** (Production, Preview, Development)

5. Click **Save**

6. **Redeploy** your project:
   - Go to **Deployments** tab
   - Click the **⋯** menu on the latest deployment
   - Click **Redeploy**

---

## 📋 Your Gemini API Key

Your API key should be in your local `.env` file. 

To view it:
```bash
cat .env
```

Copy the value after `GEMINI_API_KEY=` and paste it into Vercel.

---

## ⚠️ Known Limitations on Vercel Free Tier

Some features may not work on Vercel's free tier due to serverless limitations:

### ❌ Won't Work:
- **Selenium-based LinkedIn scraping** (requires browser automation)
- **Playwright scraping** (requires browser binaries)
- **Chrome WebDriver** (not available in serverless)

### ✅ Will Work:
- ✅ LinkedIn paste data parsing (with Gemini AI)
- ✅ Resume generation (4 templates)
- ✅ ATS scoring
- ✅ Cover letter generation
- ✅ Skill gap analysis
- ✅ Career path advisor
- ✅ **Interview question generator** (NEW!)
- ✅ Manual form input

---

## 🔄 Alternative: Recommended Deployment Options

If you need full functionality including scraping:

### Option 1: Render.com (Recommended)
- ✅ Free tier available
- ✅ Supports long-running processes
- ✅ Full Python environment
- ✅ Can run Selenium/Playwright
- 📝 Deploy: https://render.com

### Option 2: Railway.app
- ✅ Free trial credits
- ✅ Full containerization
- ✅ Easy GitHub integration
- 📝 Deploy: https://railway.app

### Option 3: Heroku
- ✅ Free dynos (with credit card)
- ✅ Full app support
- ✅ Mature platform
- 📝 Deploy: https://heroku.com

### Option 4: PythonAnywhere
- ✅ Free tier for Flask apps
- ✅ Good for smaller projects
- 📝 Deploy: https://pythonanywhere.com

---

## 🚀 After Adding Environment Variables

1. **Vercel will automatically redeploy** when you save the environment variable
2. Wait 1-2 minutes for deployment
3. Visit your app URL (Vercel will provide this)
4. Test the features:
   - ✅ Paste LinkedIn data
   - ✅ Generate resume
   - ✅ Get ATS score
   - ✅ Generate interview questions

---

## 📝 Deployment URL

Your app will be available at:
- `https://resume-builder-[random].vercel.app`

Vercel will show you the exact URL in the deployment dashboard.

---

## 🐛 Troubleshooting

### If you still get FUNCTION_INVOCATION_FAILED:

1. **Check Vercel Function Logs**:
   - Go to your deployment
   - Click **View Function Logs**
   - Look for specific error messages

2. **Common Issues**:
   - ❌ Missing `GEMINI_API_KEY` environment variable
   - ❌ Invalid API key
   - ❌ Function timeout (Vercel free tier = 10s max)
   - ❌ Large dependencies exceeding size limits

3. **Check Build Logs**:
   - Ensure all dependencies installed successfully
   - Look for any Python import errors

4. **Test Locally First**:
   ```bash
   python app.py
   ```
   If it works locally, the issue is Vercel-specific.

---

## 💡 Quick Fix if Still Broken

If after adding environment variables it still doesn't work, the issue might be:

1. **Serverless function timeout** - Some AI operations take > 10 seconds
2. **Package size too large** - Vercel has size limits

**Solution**: Consider deploying to **Render.com** instead for full functionality.

---

## ✅ What to Do Now

1. ✅ Add `GEMINI_API_KEY` to Vercel environment variables
2. ✅ Redeploy the project
3. ✅ Test the deployment
4. ⚠️ If issues persist, consider Render.com for full feature support

---

**Your code is pushed and ready! Just add the environment variable and you're live! 🚀**
