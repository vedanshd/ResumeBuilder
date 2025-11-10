"""
ATS Score Analyzer using Gemini AI
Analyzes resumes and provides ATS compatibility scores
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

load_dotenv()

class ATSAnalyzer:
    def __init__(self):
        """Initialize the ATS Analyzer with Gemini AI"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
            print("⚠️  Warning: GEMINI_API_KEY not found. ATS analysis disabled.")
    
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
    
    def _format_profile_for_analysis(self, profile_data):
        """Format profile data into readable text for analysis"""
        text_parts = []
        
        # Name and headline
        if profile_data.get('name'):
            text_parts.append(f"Name: {profile_data['name']}")
        if profile_data.get('headline'):
            text_parts.append(f"Headline: {profile_data['headline']}")
        
        # About
        if profile_data.get('about'):
            text_parts.append(f"\nAbout:\n{profile_data['about']}")
        
        # Experience
        if profile_data.get('experience'):
            text_parts.append("\nExperience:")
            for exp in profile_data['experience']:
                text_parts.append(f"- {exp.get('title', '')} at {exp.get('company', '')}")
                text_parts.append(f"  Duration: {exp.get('duration', '')}")
                if exp.get('description'):
                    text_parts.append(f"  {exp['description']}")
        
        # Education
        if profile_data.get('education'):
            text_parts.append("\nEducation:")
            for edu in profile_data['education']:
                text_parts.append(f"- {edu.get('degree', '')} in {edu.get('field', '')}")
                text_parts.append(f"  {edu.get('school', '')} ({edu.get('year', '')})")
        
        # Skills
        if profile_data.get('skills'):
            text_parts.append(f"\nSkills: {', '.join(profile_data['skills'])}")
        
        return "\n".join(text_parts)
    
    def _create_ats_prompt(self, resume_text, job_description=None):
        """Create prompt for ATS analysis"""
        base_prompt = f"""
You are an expert ATS (Applicant Tracking System) analyzer. Analyze the following resume and provide a comprehensive ATS compatibility score.

Resume:
{resume_text}
"""
        
        if job_description:
            base_prompt += f"""
Job Description to match against:
{job_description}
"""
        
        base_prompt += """
Provide your analysis in the following JSON format (respond with ONLY valid JSON, no markdown):
{
    "overall_score": <number between 0-100>,
    "category_scores": {
        "formatting": <number between 0-100>,
        "keywords": <number between 0-100>,
        "experience": <number between 0-100>,
        "skills": <number between 0-100>,
        "education": <number between 0-100>
    },
    "strengths": [
        "strength 1",
        "strength 2",
        "strength 3"
    ],
    "improvements": [
        "improvement suggestion 1",
        "improvement suggestion 2",
        "improvement suggestion 3"
    ],
    "missing_keywords": [
        "keyword1",
        "keyword2"
    ],
    "ats_friendly_rating": "Excellent|Good|Fair|Poor"
}

CRITICAL SCORING RULES:
- ALL scores MUST be integers between 0-100 (inclusive)
- overall_score: Weighted average of category scores (0-100 range)
- Each category_score: Individual rating from 0-100
- Score ranges: 90-100 = Excellent, 75-89 = Good, 60-74 = Fair, 0-59 = Poor
- Be realistic but fair in scoring

Evaluate based on:
1. Formatting: Clean structure, proper sections, readability
2. Keywords: Industry-relevant keywords, action verbs, technical terms
3. Experience: Quantifiable achievements, relevant experience
4. Skills: Technical and soft skills alignment
5. Education: Relevant qualifications

Provide actionable improvement suggestions.
"""
        return base_prompt
    
    def _parse_ats_response(self, response_text):
        """Parse Gemini response into structured analysis"""
        try:
            # Remove markdown code blocks if present
            json_text = re.sub(r'```json\s*|\s*```', '', response_text)
            json_text = json_text.strip()
            
            # Parse JSON
            analysis = json.loads(json_text)
            
            # Validate required fields
            required_fields = ['overall_score', 'category_scores', 'strengths', 'improvements']
            for field in required_fields:
                if field not in analysis:
                    raise ValueError(f"Missing required field: {field}")
            
            # Ensure scores are in 0-100 range
            analysis['overall_score'] = max(0, min(100, int(analysis['overall_score'])))
            for key in analysis['category_scores']:
                analysis['category_scores'][key] = max(0, min(100, int(analysis['category_scores'][key])))
            
            return analysis
            
        except Exception as e:
            print(f"Failed to parse ATS response: {str(e)}")
            print(f"Response was: {response_text[:200]}")
            return self._get_fallback_analysis()
    
    def _get_fallback_analysis(self, profile_data=None):
        """Return basic ATS analysis when AI is unavailable"""
        if profile_data:
            return self._calculate_smart_fallback_score(profile_data)
        
        # Generic fallback if no profile data
        return {
            "overall_score": 68,
            "category_scores": {
                "formatting": 70,
                "keywords": 65,
                "experience": 68,
                "skills": 67,
                "education": 70
            },
            "strengths": [
                "Clear professional experience listed",
                "Education background included",
                "Multiple skills documented"
            ],
            "improvements": [
                "Add more quantifiable achievements",
                "Include industry-specific keywords",
                "Expand skill descriptions"
            ],
            "missing_keywords": [
                "Add role-specific technical terms",
                "Include action verbs"
            ],
            "ats_friendly_rating": "Good"
        }
    
    def _calculate_smart_fallback_score(self, profile_data):
        """Calculate ATS score based on resume content depth - Range: 0-100"""
        score = 50  # Base score (minimum)
        category_scores = {
            "formatting": 50,
            "keywords": 50,
            "experience": 50,
            "skills": 50,
            "education": 50
        }
        strengths = []
        improvements = []
        
        # Calculate points (max 50 points to reach 100)
        points = 0
        
        # Experience scoring (max 15 points)
        experiences = profile_data.get('experience', [])
        if experiences:
            exp_points = min(10, len(experiences) * 3)
            points += exp_points
            category_scores['experience'] = min(100, 50 + (len(experiences) * 8))
            
            # Check for descriptions
            detailed_exp = sum(1 for exp in experiences if exp.get('description') and len(exp.get('description', '')) > 50)
            if detailed_exp > 0:
                desc_points = min(5, detailed_exp * 2)
                points += desc_points
                category_scores['experience'] = min(100, category_scores['experience'] + (detailed_exp * 5))
                strengths.append(f"Detailed descriptions for {detailed_exp} role(s)")
            else:
                improvements.append("Add detailed descriptions to your work experience")
        else:
            improvements.append("Add professional work experience")
        
        # Skills scoring (max 10 points)
        skills = profile_data.get('skills', [])
        if skills:
            skill_points = min(10, len(skills))
            points += skill_points
            category_scores['skills'] = min(100, 50 + (len(skills) * 4))
            
            if len(skills) >= 8:
                strengths.append(f"Strong skill set with {len(skills)} skills listed")
            elif len(skills) < 5:
                improvements.append("Add more relevant skills to improve ATS compatibility")
        else:
            improvements.append("Add technical and soft skills")
            
        # Education scoring (max 10 points)
        education = profile_data.get('education', [])
        if education:
            edu_points = min(10, len(education) * 5)
            points += edu_points
            category_scores['education'] = min(100, 50 + (len(education) * 15))
            strengths.append(f"Education credentials included ({len(education)} degree(s))")
        else:
            improvements.append("Add educational background")
        
        # About/Summary scoring (max 8 points)
        about = profile_data.get('about', '')
        if about and len(about) > 100:
            points += 8
            category_scores['keywords'] = min(100, category_scores['keywords'] + 20)
            strengths.append("Professional summary included")
        else:
            improvements.append("Add a compelling professional summary")
        
        # Formatting score (based on completeness) (max 5 points)
        name = profile_data.get('name', '')
        headline = profile_data.get('headline', '')
        
        if name and headline:
            category_scores['formatting'] = min(100, 75)
            points += 5
        else:
            improvements.append("Ensure name and headline are clear")
        
        # Keywords score (based on content richness) (max 7 points)
        total_text_length = len(about) + sum(len(exp.get('description', '')) for exp in experiences)
        if total_text_length > 500:
            points += 7
            category_scores['keywords'] = min(100, category_scores['keywords'] + 25)
        elif total_text_length > 200:
            points += 4
            category_scores['keywords'] = min(100, category_scores['keywords'] + 15)
        else:
            improvements.append("Add more descriptive content with relevant keywords")
        
        # Calculate final score (50-100 range)
        score = min(100, 50 + points)
        
        # Cap all category scores at 100
        for key in category_scores:
            category_scores[key] = min(100, max(50, category_scores[key]))
        
        # Ensure we have enough items in lists
        if len(strengths) < 3:
            default_strengths = [
                "Clear professional presentation",
                "Organized resume structure",
                "Contact information present"
            ]
            strengths.extend(default_strengths[:3 - len(strengths)])
            
        if len(improvements) < 3:
            default_improvements = [
                "Consider adding quantifiable achievements (numbers, percentages)",
                "Include action verbs to describe responsibilities",
                "Tailor content to specific job requirements"
            ]
            improvements.extend(default_improvements[:3 - len(improvements)])
        
        # Determine rating based on 0-100 scale
        if score >= 90:
            rating = "Excellent"
        elif score >= 75:
            rating = "Good"
        elif score >= 60:
            rating = "Fair"
        else:
            rating = "Poor"
        
        return {
            "overall_score": score,
            "category_scores": category_scores,
            "strengths": strengths[:3],
            "improvements": improvements[:3],
            "missing_keywords": [
                "Industry-specific technical terms",
                "Action verbs (achieved, implemented, led, etc.)"
            ],
            "ats_friendly_rating": rating
        }
    
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
            return self._calculate_smart_fallback_score(profile_data)
        
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
            return self._calculate_smart_fallback_score(profile_data)
