# APPENDIX A – SAMPLE CODE

## RESUME BUILDER PROJECT

---

## 1. GEMINI AI INTEGRATION

### 1.1 LinkedIn Profile Parsing with Gemini

```python
def _parse_with_gemini(self, text):
    """Use Gemini AI to parse LinkedIn profile text"""
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
You are a LinkedIn profile data extractor. Parse the following LinkedIn profile text 
and extract structured information.

Return ONLY a valid JSON object (no markdown, no code blocks, no explanations) 
with this exact structure:
{{
    "name": "Full Name",
    "headline": "Professional headline or job title",
    "about": "About/summary section (if available)",
    "experience": [
        {{
            "title": "Job Title",
            "company": "Company Name",
            "duration": "Start Date - End Date",
            "description": "Job description or achievements"
        }}
    ],
    "education": [
        {{
            "school": "School/University Name",
            "degree": "Degree Name",
            "field": "Field of Study",
            "dates": "Start Year - End Year"
        }}
    ],
    "skills": ["Skill 1", "Skill 2", "Skill 3"],
    "contact": {{
        "email": "email@example.com",
        "phone": "phone number",
        "location": "City, Country"
    }}
}}

PROFILE TEXT:
{text[:10000]}
"""
        
        response = model.generate_content(prompt)
        json_str = response.text.strip()
        
        # Clean markdown formatting if present
        json_str = re.sub(r'^```json\s*', '', json_str)
        json_str = re.sub(r'\s*```$', '', json_str)
        
        # Parse JSON
        profile_data = json.loads(json_str)
        print("✅ Successfully parsed with Gemini AI")
        return profile_data
        
    except Exception as e:
        print(f"❌ Gemini parsing error: {str(e)}")
        return None
```

---

## 2. ATS SCORING SYSTEM

### 2.1 ATS Analysis with Gemini

```python
def analyze_resume(self, profile_data, job_description=None):
    """
    Analyze resume for ATS compatibility
    
    Args:
        profile_data (dict): Parsed LinkedIn profile data
        job_description (str, optional): Job description to match against
    
    Returns:
        dict: ATS analysis results with score and recommendations
    """
    if not self.model:
        return self._get_fallback_analysis()
    
    try:
        # Prepare resume text from profile data
        resume_text = self._format_profile_for_analysis(profile_data)
        
        # Create ATS analysis prompt
        prompt = self._create_ats_prompt(resume_text, job_description)
        
        # Generate analysis
        response = self.model.generate_content(prompt)
        analysis_text = response.text.strip()
        
        # Parse the response
        analysis = self._parse_ats_response(analysis_text)
        
        print("✅ ATS analysis completed successfully")
        return analysis
        
    except Exception as e:
        print(f"❌ ATS analysis error: {str(e)}")
        return self._get_fallback_analysis()
```

### 2.2 ATS Prompt Generation

```python
def _create_ats_prompt(self, resume_text, job_description=None):
    """Create prompt for ATS analysis"""
    base_prompt = f"""
You are an expert ATS (Applicant Tracking System) analyzer. 
Analyze the following resume and provide a comprehensive ATS compatibility score.

RESUME:
{resume_text[:5000]}

Provide analysis in this JSON format:
{{
    "ats_score": 85,
    "strengths": [
        "Clear job titles and company names",
        "Quantifiable achievements with metrics",
        "Relevant keywords for the industry"
    ],
    "weaknesses": [
        "Missing contact information",
        "Lack of action verbs in descriptions"
    ],
    "keyword_optimization": {{
        "found_keywords": ["Python", "Machine Learning", "Data Analysis"],
        "missing_keywords": ["TensorFlow", "Deep Learning"],
        "keyword_density": "good"
    }},
    "formatting_issues": [
        "Use simple fonts for better parsing",
        "Avoid tables and graphics"
    ],
    "recommendations": [
        "Add more quantifiable metrics to achievements",
        "Include industry-specific certifications",
        "Use standard section headings (Experience, Education, Skills)"
    ],
    "match_score": 78,
    "overall_assessment": "Strong resume with good ATS compatibility..."
}}
"""
    
    if job_description:
        base_prompt += f"""

JOB DESCRIPTION:
{job_description[:2000]}

Additional analysis:
- Compare resume keywords with job description requirements
- Identify skill gaps
- Assess experience level match
- Provide job-specific recommendations
"""
    
    return base_prompt
```

---

## 3. SKILL GAP ANALYSIS

### 3.1 Skill Gap Detection with AI

```python
def _analyze_with_ai(self, profile_data, job_description):
    """Use Gemini AI to perform intelligent skill gap analysis"""
    
    try:
        # Prepare profile summary
        user_skills = profile_data.get('skills', [])
        experiences = profile_data.get('experience', [])
        education = profile_data.get('education', [])
        
        profile_summary = f"""
USER PROFILE:
Name: {profile_data.get('name', 'N/A')}
Headline: {profile_data.get('headline', 'N/A')}

Skills: {', '.join(user_skills) if user_skills else 'None listed'}

Experience:
{self._format_experiences(experiences)}

Education:
{self._format_education(education)}

About:
{profile_data.get('about', 'N/A')}
"""
        
        prompt = f"""
You are a career development expert. Analyze the skill gap between this 
user's profile and the job requirements.

{profile_summary}

JOB DESCRIPTION:
{job_description}

Provide a detailed skill gap analysis in the following JSON format:
{{
    "matching_skills": ["skill1", "skill2", ...],
    "missing_skills": ["skill1", "skill2", ...],
    "partially_matched_skills": ["skill1", "skill2", ...],
    "skill_gap_score": 75,
    "recommendations": [
        "Specific recommendation 1",
        "Specific recommendation 2"
    ],
    "learning_resources": [
        {{
            "skill": "Python",
            "resources": ["Coursera Python Course", "Real Python tutorials"],
            "priority": "high"
        }}
    ],
    "experience_gap": {{
        "years_required": 5,
        "years_you_have": 3,
        "gap": "2 years",
        "advice": "Focus on building projects that demonstrate advanced skills"
    }}
}}
"""
        
        response = self.model.generate_content(prompt)
        json_str = self._extract_json(response.text)
        analysis = json.loads(json_str)
        
        return {
            'analysis': analysis,
            'method': 'ai',
            'confidence': 'high'
        }
        
    except Exception as e:
        print(f"AI analysis error: {str(e)}")
        return self._basic_skill_analysis(profile_data, job_description)
```

---

## 4. CAREER PATH ADVISOR

### 4.1 Career Path Analysis Engine

```python
def analyze_career_path(self, profile_data, target_role=None, years_ahead=5):
    """
    Analyze career path and provide comprehensive guidance
    
    Args:
        profile_data (dict): User's profile data from LinkedIn
        target_role (str): Optional specific role they're targeting
        years_ahead (int): How many years to project (default 5)
        
    Returns:
        dict: Career path analysis with recommendations
    """
    if self.use_ai:
        return self._analyze_with_ai(profile_data, target_role, years_ahead)
    else:
        return self._basic_career_analysis(profile_data, target_role, years_ahead)
```

### 4.2 AI-Powered Career Guidance

```python
def _analyze_with_ai(self, profile_data, target_role, years_ahead):
    """Use Gemini AI to perform intelligent career path analysis"""
    
    try:
        # Prepare profile summary
        user_skills = profile_data.get('skills', [])
        experiences = profile_data.get('experience', [])
        education = profile_data.get('education', [])
        current_title = experiences[0].get('title', 'N/A') if experiences else 'N/A'
        
        profile_summary = f"""
CURRENT PROFILE:
Name: {profile_data.get('name', 'N/A')}
Current Role: {current_title}
Headline: {profile_data.get('headline', 'N/A')}

Skills: {', '.join(user_skills[:20]) if user_skills else 'None listed'}

Experience History:
{self._format_experiences(experiences)}

Education:
{self._format_education(education)}

About:
{profile_data.get('about', 'N/A')[:500]}
"""
        
        target_context = f"\nTarget Role: {target_role}" if target_role else \
                        "\nNo specific target role - recommend best progression paths"
        
        prompt = f"""
You are an expert career advisor. Analyze this professional's career and 
provide comprehensive guidance.

{profile_summary}
{target_context}

Provide detailed career path analysis in JSON format with:
- current_level: Career level assessment
- next_role_suggestions: 3-5 logical next roles with timeframes
- skill_roadmap: Immediate, short-term, and long-term skill development
- industry_trends: Emerging skills, market demand, salary trends
- career_timeline: Year-by-year progression plan for {years_ahead} years
- alternative_paths: Alternative career directions with pros/cons
- certifications: Recommended certifications ranked by priority
- networking_advice: Industry events, communities, mentorship strategies

Focus on actionable, specific recommendations tailored to this individual.
"""
        
        response = self.model.generate_content(prompt)
        json_str = self._extract_json_from_response(response.text)
        career_analysis = json.loads(json_str)
        
        return {
            'success': True,
            'analysis': career_analysis,
            'method': 'ai_powered',
            'model': 'gemini-2.0-flash'
        }
        
    except Exception as e:
        print(f"Career analysis error: {str(e)}")
        return self._basic_career_analysis(profile_data, target_role, years_ahead)
```

---

## 5. COVER LETTER GENERATION

### 5.1 AI-Powered Cover Letter Creator

```python
def generate_cover_letter_content(self, profile_data, job_description):
    """
    Use Gemini AI to generate personalized cover letter
    
    Args:
        profile_data (dict): Resume/profile data
        job_description (str): Job description text
        
    Returns:
        str: Generated cover letter text
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Prepare profile summary
        experience_summary = "\n".join([
            f"- {exp.get('title', '')} at {exp.get('company', '')} "
            f"({exp.get('duration', '')})"
            for exp in profile_data.get('experience', [])[:3]
        ])
        
        education_summary = "\n".join([
            f"- {edu.get('degree', '')} from {edu.get('school', '')}"
            for edu in profile_data.get('education', [])[:2]
        ])
        
        skills = ", ".join(profile_data.get('skills', [])[:8])
        
        prompt = f"""
You are a professional career coach and cover letter writer. 
Write a compelling, personalized cover letter based on the candidate's 
profile and the job description.

CANDIDATE PROFILE:
Name: {profile_data.get('name', '')}
Headline: {profile_data.get('headline', '')}

Recent Experience:
{experience_summary}

Education:
{education_summary}

Skills: {skills}

About: {profile_data.get('about', '')[:300]}

JOB DESCRIPTION:
{job_description[:2000]}

CRITICAL INSTRUCTIONS:
1. Write a professional cover letter (250-350 words maximum)
2. Address it "Dear Hiring Manager,"
3. Start with a strong opening showing genuine enthusiasm for THIS role
4. Highlight 2-3 MOST RELEVANT experiences matching job requirements
5. Use SPECIFIC examples and metrics (e.g., "increased efficiency by 30%")
6. Demonstrate understanding of the company's needs
7. Explain WHY you're excited about THIS role specifically
8. Include 1-2 key technical skills mentioned in job description
9. End with confident call to action
10. Sign off with "Sincerely," followed by candidate's name
11. Use professional but warm and authentic tone
12. Make it personalized to THIS job - NOT generic
13. NO placeholders like [Your Name], [Company Name]
14. Keep paragraphs short (3-4 sentences) for readability
15. Focus on VALUE you bring, not just what you want

Write ONLY the cover letter text (no subject line, no commentary).
"""
        
        response = model.generate_content(prompt)
        cover_letter = response.text.strip()
        
        print("✅ Cover letter generated successfully with AI")
        return cover_letter
        
    except Exception as e:
        print(f"❌ AI cover letter generation failed: {str(e)}")
        return self._generate_template_cover_letter(profile_data, job_description)
```

---

## 6. RESUME GENERATION - MULTIPLE TEMPLATES

### 6.1 Modern Template Builder

```python
def _build_modern_template(self, profile_data):
    """Build modern template resume - Blue accent colors, clean design"""
    story = []
    styles = getSampleStyleSheet()
    
    # Modern styles with blue accents
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#0071E3'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0071E3'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6
    )
    
    # Build header
    story.append(Paragraph(profile_data.get('name', 'Name Not Available'), 
                          name_style))
    
    if profile_data.get('headline'):
        story.append(Paragraph(profile_data['headline'], headline_style))
    
    # Contact information
    contact = profile_data.get('contact', {})
    contact_info = []
    if contact.get('location'):
        contact_info.append(contact['location'])
    if contact.get('email'):
        contact_info.append(contact['email'])
    if contact.get('phone'):
        contact_info.append(contact['phone'])
    
    if contact_info:
        story.append(Paragraph(' | '.join(contact_info), headline_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Experience section
    experiences = profile_data.get('experience', [])
    if experiences:
        story.append(Paragraph('EXPERIENCE', section_title_style))
        for exp in experiences:
            title_text = f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')}"
            story.append(Paragraph(title_text, body_style))
            
            if exp.get('duration'):
                duration_text = f"<i>{exp['duration']}</i>"
                story.append(Paragraph(duration_text, body_style))
            
            if exp.get('description'):
                # Format with bullet points
                desc = exp['description']
                if len(desc) > 150:
                    sentences = [s.strip() for s in 
                               desc.replace('. ', '.|').split('|') if s.strip()]
                    for sentence in sentences[:5]:
                        if sentence:
                            bullet_style = ParagraphStyle(
                                'Bullet', 
                                parent=body_style, 
                                leftIndent=15, 
                                firstLineIndent=-10
                            )
                            story.append(Paragraph(f"• {sentence}", bullet_style))
                else:
                    story.append(Paragraph(exp['description'], body_style))
                
                story.append(Spacer(1, 0.1*inch))
    
    return story
```

### 6.2 Executive Template Builder

```python
def _build_executive_template(self, profile_data):
    """Build executive template - Professional, formal, serif fonts"""
    story = []
    styles = getSampleStyleSheet()
    
    # Executive styles - formal and elegant
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=4,
        alignment=TA_CENTER,
        fontName='Times-Bold'
    )
    
    title_divider_style = ParagraphStyle(
        'DividerStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        spaceBefore=14,
        fontName='Times-Bold',
        borderWidth=0,
        borderColor=colors.HexColor('#1a1a1a'),
        borderPadding=4
    )
    
    # Build content with elegant formatting
    story.append(Paragraph(profile_data.get('name', '').upper(), name_style))
    story.append(Paragraph('━━━━━━━━━━━━━━━━━━━━━━━━', title_divider_style))
    
    # Professional experience with detailed achievements
    experiences = profile_data.get('experience', [])
    if experiences:
        story.append(Paragraph('PROFESSIONAL EXPERIENCE', section_title_style))
        
        for exp in experiences:
            # Company and title on separate emphasized lines
            company_style = ParagraphStyle(
                'CompanyStyle',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#1a1a1a'),
                fontName='Times-Bold',
                spaceAfter=2
            )
            story.append(Paragraph(exp.get('company', ''), company_style))
            
            title_duration = f"<i>{exp.get('title', '')}</i> | {exp.get('duration', '')}"
            story.append(Paragraph(title_duration, body_style))
            
            # Achievement-focused descriptions
            if exp.get('description'):
                achievement_style = ParagraphStyle(
                    'Achievement',
                    parent=body_style,
                    leftIndent=20,
                    firstLineIndent=-15,
                    spaceAfter=3
                )
                story.append(Paragraph(f"▪ {exp['description']}", 
                                      achievement_style))
            
            story.append(Spacer(1, 0.12*inch))
    
    return story
```

---

## 7. FLASK ROUTES AND API ENDPOINTS

### 7.1 Resume Generation Endpoint

```python
@app.route('/generate', methods=['POST'])
def generate_resume():
    """Generate resume from pasted LinkedIn text"""
    try:
        data = request.get_json()
        linkedin_text = data.get('linkedin_text', '')
        template = data.get('template', 'modern')
        
        if not linkedin_text or len(linkedin_text.strip()) < 50:
            return jsonify({
                'error': 'Please paste your LinkedIn profile content'
            }), 400
        
        # Parse the pasted LinkedIn content
        parser = LinkedInParser()
        profile_data = parser.parse_linkedin_text(linkedin_text)
        
        if not profile_data:
            return jsonify({
                'error': 'Failed to extract data from pasted content'
            }), 500
        
        # Generate resume PDF with selected template
        generator = ResumeGenerator()
        pdf_path = generator.create_resume(profile_data, template=template)
        
        return jsonify({
            'success': True,
            'pdf_path': pdf_path,
            'profile_data': profile_data,
            'message': f'Resume generated with {template.capitalize()} template!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 7.2 ATS Analysis Endpoint

```python
@app.route('/analyze-ats', methods=['POST'])
def analyze_ats():
    """Analyze resume for ATS compatibility"""
    try:
        data = request.get_json()
        profile_data = data.get('profile_data', {})
        job_description = data.get('job_description', None)
        
        if not profile_data:
            return jsonify({'error': 'Profile data is required'}), 400
        
        # Analyze ATS score
        analyzer = ATSAnalyzer()
        ats_analysis = analyzer.analyze_resume(profile_data, job_description)
        
        return jsonify({
            'success': True,
            'analysis': ats_analysis,
            'message': 'ATS analysis completed!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 7.3 Career Path Analysis Endpoint

```python
@app.route('/analyze-career-path', methods=['POST'])
def analyze_career_path():
    """Generate career path recommendations"""
    try:
        data = request.get_json()
        profile_data = data.get('profile_data')
        target_role = data.get('target_role', None)
        years_ahead = data.get('years_ahead', 5)
        
        if not profile_data:
            return jsonify({'error': 'Profile data is required'}), 400
        
        # Validate years_ahead
        try:
            years_ahead = int(years_ahead)
            if years_ahead < 1 or years_ahead > 20:
                years_ahead = 5
        except:
            years_ahead = 5
        
        # Generate career path analysis
        advisor = CareerPathAdvisor()
        career_analysis = advisor.analyze_career_path(
            profile_data, 
            target_role, 
            years_ahead
        )
        
        return jsonify({
            'success': True,
            'analysis': career_analysis,
            'message': 'Career path analysis completed!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

---

## 8. FRONTEND JAVASCRIPT INTEGRATION

### 8.1 Career Path Results Display

```javascript
function displayCareerPathResults(data) {
    const container = document.getElementById('career-path-results');
    const analysis = data.analysis;
    
    let html = `
        <div class="career-path-container">
            <div class="current-level">
                <h3>Current Career Level</h3>
                <div class="level-badge">${analysis.current_level}</div>
            </div>
    `;
    
    // Next Role Suggestions
    if (analysis.next_role_suggestions && 
        analysis.next_role_suggestions.length > 0) {
        html += `
            <div class="next-roles-section">
                <h3>🎯 Next Role Suggestions</h3>
                <div class="roles-grid">
        `;
        
        analysis.next_role_suggestions.forEach(role => {
            const difficultyClass = role.difficulty.toLowerCase();
            const readinessPercent = role.readiness_score || 0;
            
            html += `
                <div class="next-role-card ${difficultyClass}">
                    <div class="role-header">
                        <h4>${role.title}</h4>
                        <span class="difficulty-badge">${role.difficulty}</span>
                    </div>
                    <div class="timeframe">📅 ${role.timeframe}</div>
                    <div class="readiness-bar">
                        <div class="readiness-fill" 
                             style="width: ${readinessPercent}%">
                            ${readinessPercent}% Ready
                        </div>
                    </div>
                    <p class="rationale">${role.rationale}</p>
                    
                    <div class="required-skills">
                        <strong>Required Skills:</strong>
                        <div class="skills-tags">
                            ${role.required_skills.map(skill => 
                                `<span class="skill-tag">${skill}</span>`
                            ).join('')}
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    // Skill Roadmap with Tabs
    if (analysis.skill_roadmap) {
        html += displaySkillRoadmap(analysis.skill_roadmap);
    }
    
    // Industry Trends
    if (analysis.industry_trends) {
        html += displayIndustryTrends(analysis.industry_trends);
    }
    
    // Career Timeline
    if (analysis.career_timeline) {
        html += displayCareerTimeline(analysis.career_timeline);
    }
    
    html += `</div>`;
    container.innerHTML = html;
    container.style.display = 'block';
}
```

### 8.2 Dynamic Template Selection

```javascript
document.querySelectorAll('.template-option').forEach(option => {
    option.addEventListener('click', function() {
        // Remove active class from all
        document.querySelectorAll('.template-option').forEach(opt => {
            opt.classList.remove('active');
        });
        
        // Add active to selected
        this.classList.add('active');
        
        // Store selected template
        const selectedTemplate = this.dataset.template;
        console.log(`Selected template: ${selectedTemplate}`);
    });
});
```

---

## 9. ERROR HANDLING AND FALLBACKS

### 9.1 Gemini API Error Handling

```python
def _parse_with_gemini(self, text):
    """Use Gemini AI with comprehensive error handling"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        json_str = response.text.strip()
        
        # Clean markdown formatting
        json_str = re.sub(r'^```json\s*', '', json_str)
        json_str = re.sub(r'\s*```$', '', json_str)
        
        profile_data = json.loads(json_str)
        print("✅ Successfully parsed with Gemini AI")
        return profile_data
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {str(e)}")
        print("Falling back to regex parsing...")
        return None
        
    except Exception as e:
        print(f"❌ Gemini API error: {str(e)}")
        return None
```

### 9.2 ATS Fallback Analysis

```python
def _get_fallback_analysis(self):
    """Provide basic ATS analysis when AI is unavailable"""
    return {
        'ats_score': 65,
        'strengths': [
            'Profile includes work experience',
            'Education information present',
            'Skills section included'
        ],
        'weaknesses': [
            'AI analysis unavailable - using basic scoring',
            'Manual review recommended for detailed feedback'
        ],
        'keyword_optimization': {
            'found_keywords': [],
            'missing_keywords': [],
            'keyword_density': 'unknown'
        },
        'formatting_issues': [
            'Use standard section headers (Experience, Education, Skills)',
            'Include quantifiable achievements',
            'Add relevant keywords for your industry'
        ],
        'recommendations': [
            'Configure GEMINI_API_KEY for AI-powered analysis',
            'Use action verbs to describe responsibilities',
            'Include metrics and measurable results',
            'Tailor resume to specific job descriptions'
        ],
        'match_score': None,
        'overall_assessment': 'Basic analysis complete. Enable AI for detailed insights.',
        'analysis_method': 'fallback'
    }
```

---

## 10. UTILITY FUNCTIONS

### 10.1 JSON Extraction from AI Responses

```python
def _extract_json(self, text):
    """Extract JSON from AI response that may contain markdown"""
    # Remove markdown code blocks
    text = re.sub(r'^```json\s*', '', text.strip())
    text = re.sub(r'^```\s*', '', text.strip())
    text = re.sub(r'\s*```$', '', text.strip())
    
    # Find JSON object bounds
    start = text.find('{')
    end = text.rfind('}') + 1
    
    if start != -1 and end > start:
        return text[start:end]
    
    return text
```

### 10.2 Experience Formatting Helper

```python
def _format_experiences(self, experiences):
    """Format experience list for AI prompts"""
    if not experiences:
        return "No experience listed"
    
    formatted = []
    for i, exp in enumerate(experiences[:5], 1):
        formatted.append(f"""
{i}. {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}
   Duration: {exp.get('duration', 'N/A')}
   Description: {exp.get('description', 'N/A')[:200]}
""")
    
    return "\n".join(formatted)
```

### 10.3 Profile Data Validation

```python
def _validate_profile_data(self, profile_data):
    """Validate that profile data has minimum required fields"""
    required_fields = ['name']
    recommended_fields = ['headline', 'experience', 'skills']
    
    # Check required fields
    for field in required_fields:
        if not profile_data.get(field):
            raise ValueError(f"Missing required field: {field}")
    
    # Warn about missing recommended fields
    for field in recommended_fields:
        if not profile_data.get(field):
            print(f"⚠️  Warning: Missing recommended field: {field}")
    
    return True
```

---

## END OF APPENDIX
