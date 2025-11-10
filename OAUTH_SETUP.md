# LinkedIn OAuth Setup Guide

## Overview
This guide will help you set up LinkedIn OAuth authentication so users can sign in with their LinkedIn account and generate resumes from their own profile data.

---

## Step 1: Create a LinkedIn App

1. **Go to LinkedIn Developers**
   - Visit: https://www.linkedin.com/developers/apps
   - Sign in with your LinkedIn account

2. **Create a New App**
   - Click "Create app"
   - Fill in the required information:
     - **App name**: LinkedIn Resume Builder
     - **LinkedIn Page**: Create or select a company page (required)
     - **App logo**: Upload any logo (optional)
     - **Legal agreement**: Check the box to agree

3. **Configure OAuth Settings**
   - Go to the "Auth" tab
   - Under "OAuth 2.0 settings":
     - **Redirect URLs**: Add `http://localhost:8080/callback`
     - Click "Add redirect URL"
   
4. **Request API Products**
   - Go to the "Products" tab
   - Request access to "Sign In with LinkedIn using OpenID Connect"
   - ⚠️ LinkedIn may take time to approve (usually instant for Sign In)

5. **Get Your Credentials**
   - Go back to the "Auth" tab
   - Copy your **Client ID**
   - Copy your **Client Secret**

---

## Step 2: Configure Your Application

1. **Update .env file**

Create or edit `/Users/vedanshdhawan/ResumeBuilder/.env`:

```bash
# LinkedIn OAuth Credentials
LINKEDIN_CLIENT_ID=your-client-id-from-linkedin
LINKEDIN_CLIENT_SECRET=your-client-secret-from-linkedin
LINKEDIN_REDIRECT_URI=http://localhost:8080/callback

# Flask Secret Key
FLASK_SECRET_KEY=generate-a-random-secret-key-here
```

2. **Generate a Secret Key**

Run this command to generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_hex(16))"
```

Copy the output and paste it as your `FLASK_SECRET_KEY` value.

---

## Step 3: Test the Application

1. **Restart the Flask server**

```bash
python app.py
```

2. **Open your browser**

Navigate to: `http://localhost:8080`

3. **Click "Sign in with LinkedIn"**
   - You'll be redirected to LinkedIn
   - Authorize the app to access your profile
   - You'll be redirected back to the app

4. **Generate your resume**
   - Click "Generate My Resume"
   - Download the PDF!

---

## ⚠️ Important Notes

### API Limitations

LinkedIn's OAuth API has very limited data access:
- ✅ Name
- ✅ Email
- ✅ Profile picture
- ❌ Work experience (not available)
- ❌ Education (not available)
- ❌ Skills (not available)
- ❌ Headline (not available)

This means the generated resume will only have basic information unless you:
1. Apply for additional LinkedIn API products (very hard to get approved)
2. Implement manual data entry for missing fields
3. Use paid third-party APIs like Proxycurl

### For Production

If deploying to production:
1. Update redirect URL to your domain:
   - In LinkedIn app settings: `https://yourdomain.com/callback`
   - In .env: `LINKEDIN_REDIRECT_URI=https://yourdomain.com/callback`

2. Use environment variables (don't commit `.env` to git)

3. Use a production WSGI server (not Flask's development server)

---

## Troubleshooting

### "redirect_uri_mismatch" error
- Make sure the redirect URL in LinkedIn app matches exactly
- Check for http vs https
- Check for trailing slashes

### "invalid_client" error
- Double-check your Client ID and Secret
- Make sure there are no spaces or quotes in .env

### "Insufficient privileges"  
- Make sure "Sign In with LinkedIn" is approved in Products tab
- Wait a few minutes after requesting access

### Limited data in resume
- This is normal - LinkedIn's API is very restrictive
- Consider adding manual data entry forms
- Or use Proxycurl API for full profile data

---

## Alternative: Manual Data Entry

Since LinkedIn's API is so limited, I can add a manual form where users can input their:
- Work experience
- Education
- Skills
- Summary

Would you like me to implement this?

---

## Next Steps

1. Create LinkedIn app and get credentials
2. Update `.env` with your credentials
3. Test the OAuth flow
4. Decide if you want to add manual data entry for missing fields

Let me know if you need help with any step!
