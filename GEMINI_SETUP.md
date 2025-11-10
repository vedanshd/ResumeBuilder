# Gemini AI Integration Setup

## Get Your Free Gemini API Key

1. **Go to Google AI Studio**
   - Visit: https://makersuite.google.com/app/apikey
   - Or: https://aistudio.google.com/app/apikey

2. **Sign in with your Google Account**

3. **Create API Key**
   - Click "Create API Key"
   - Select "Create API key in new project" (or use existing)
   - Copy the API key

4. **Add to .env file**
   
Edit `/Users/vedanshdhawan/ResumeBuilder/.env`:

```bash
GEMINI_API_KEY=your-actual-api-key-here
```

5. **Restart the Flask server**

The app will automatically detect and use Gemini!

---

## How It Works

### With Gemini API (Recommended):
✅ **AI-Powered Parsing** - Gemini understands context and structure  
✅ **Better Accuracy** - Correctly identifies names, titles, dates  
✅ **Smart Formatting** - Cleans up messy LinkedIn text  
✅ **Handles Edge Cases** - Works even with unusual profile formats  

### Without Gemini API (Fallback):
⚠️ **Regex Parsing** - Uses pattern matching  
⚠️ **Less Accurate** - May miss some fields  
⚠️ **Still Works** - Basic functionality maintained  

The app automatically falls back to regex parsing if:
- No API key is provided
- API quota is exceeded
- Gemini API fails for any reason

---

## Free Tier Limits

Gemini API Free Tier:
- ✅ **60 requests per minute**
- ✅ **1,500 requests per day**
- ✅ **1 million tokens per day**

This is MORE than enough for personal use!

---

## Privacy & Security

- ✅ Your API key is stored locally in `.env` (never committed to git)
- ✅ LinkedIn text is sent to Google's Gemini API for parsing
- ✅ No data is permanently stored by Google (per their API terms)
- ✅ Resume PDFs are generated locally on your machine

---

## Testing

1. **Without API Key:**
   - App uses regex parsing
   - Works but less accurate

2. **With API Key:**
   - App uses Gemini AI
   - Much more accurate and intelligent

Try both and see the difference!

---

## Troubleshooting

### "Import google.generativeai could not be resolved"
```bash
pip install google-generativeai==0.3.2
```

### API Key not working
- Check for spaces or quotes in `.env`
- Verify key is active at https://makersuite.google.com/app/apikey
- Check API quota limits

### Gemini parsing fails
- App automatically falls back to regex parsing
- Check terminal output for error messages
- Verify internet connection

---

## Next Steps

1. Get your free Gemini API key (takes 1 minute)
2. Add it to `.env` file
3. Restart the server
4. Test with LinkedIn profile text
5. Enjoy much better parsing! 🎉
