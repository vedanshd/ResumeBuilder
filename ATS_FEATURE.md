# ATS Score Feature

## Overview
The ATS (Applicant Tracking System) Score feature provides real-time analysis of generated resumes using Gemini AI. It evaluates resume quality and ATS compatibility with actionable insights.

## Features

### 📊 Live ATS Scoring
- **Overall Score (0-100)**: Comprehensive resume quality assessment
- **Visual Score Ring**: Animated circular progress indicator with color coding:
  - Green (80-100): Excellent
  - Blue (60-79): Good
  - Orange (40-59): Fair
  - Red (0-39): Poor

### 📈 Category Breakdown
Evaluates 5 key categories with individual scores:
1. **Formatting**: Clean structure, proper sections, readability
2. **Keywords**: Industry-relevant keywords, action verbs, technical terms
3. **Experience**: Quantifiable achievements, relevant experience
4. **Skills**: Technical and soft skills alignment
5. **Education**: Relevant qualifications

### ✅ Strengths Analysis
Lists top 3 resume strengths based on:
- Content quality
- Professional presentation
- Experience relevance

### 💡 Improvement Suggestions
Provides actionable recommendations:
- Missing keywords
- Formatting improvements
- Content optimization tips

### 🔄 Refresh Feature
- Real-time re-analysis capability
- Updates score based on any changes
- Animated refresh button

## Technical Implementation

### Backend (`ats_analyzer.py`)
```python
class ATSAnalyzer:
    - analyze_resume(profile_data, job_description)
    - Gemini AI integration
    - Fallback analysis when API unavailable
```

### API Endpoint
```
POST /analyze-ats
Body: {
    "profile_data": {...},
    "job_description": "optional"
}
```

### Frontend Components
- **HTML**: ATS score container with loading states
- **CSS**: Glassmorphism design, animated progress bars
- **JavaScript**: Score animation, data visualization

## User Flow
1. User generates resume
2. ATS analysis automatically triggered
3. Loading state shown while analyzing
4. Animated score reveal with category breakdown
5. Strengths and improvements displayed
6. Optional: Refresh score anytime

## AI Analysis Criteria
The Gemini AI evaluates based on:
- Professional formatting standards
- Industry-specific keywords
- Achievement quantification
- Skills relevance
- Education credentials
- ATS system compatibility

## Score Calculation
- AI provides comprehensive JSON analysis
- Overall score: weighted average of categories
- Rating: Excellent | Good | Fair | Poor
- Actionable insights for improvement

## Benefits
✅ Instant feedback on resume quality
✅ Data-driven improvement suggestions
✅ ATS compatibility assurance
✅ Professional presentation insights
✅ Keyword optimization guidance
