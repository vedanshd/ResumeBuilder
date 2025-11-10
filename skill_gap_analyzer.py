"""
Skill Gap Analyzer
Compares user skills with job requirements and identifies gaps
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

load_dotenv()


class SkillGapAnalyzer:
    """Analyze skill gaps between user profile and job requirements"""
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.use_ai = True
        else:
            self.use_ai = False
            print("Warning: GEMINI_API_KEY not found. Using basic skill matching.")
    
    def analyze_skill_gap(self, profile_data, job_description):
        """
        Analyze skill gaps between user and job requirements
        
        Args:
            profile_data (dict): User's profile data from LinkedIn
            job_description (str): Job description text
            
        Returns:
            dict: Skill gap analysis with recommendations
        """
        if self.use_ai:
            return self._analyze_with_ai(profile_data, job_description)
        else:
            return self._basic_skill_analysis(profile_data, job_description)
    
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
You are a career development expert. Analyze the skill gap between this user's profile and the job requirements.

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
        "Specific recommendation 2",
        ...
    ],
    "learning_resources": [
        {{
            "skill": "Python",
            "resources": ["Coursera Python Course", "Real Python tutorials"],
            "priority": "high"
        }},
        ...
    ],
    "experience_gap": {{
        "years_required": 5,
        "years_you_have": 3,
        "gap": "2 years",
        "advice": "Focus on building projects that demonstrate advanced skills"
    }},
    "summary": "Brief summary of the overall fit and what needs improvement"
}}

Be specific, actionable, and honest in your analysis. Focus on skills explicitly mentioned in the job description.
"""
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                import json
                analysis = json.loads(json_match.group())
                return {
                    'success': True,
                    'analysis': analysis,
                    'method': 'ai'
                }
            else:
                raise ValueError("Could not parse AI response")
                
        except Exception as e:
            print(f"AI analysis failed: {e}")
            # Fallback to basic analysis
            return self._basic_skill_analysis(profile_data, job_description)
    
    def _basic_skill_analysis(self, profile_data, job_description):
        """Fallback: Basic keyword matching for skill analysis"""
        
        user_skills = [s.lower() for s in profile_data.get('skills', [])]
        job_desc_lower = job_description.lower()
        
        # Common tech skills and keywords
        common_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'aws',
            'docker', 'kubernetes', 'git', 'agile', 'scrum', 'machine learning',
            'data analysis', 'project management', 'leadership', 'communication',
            'problem solving', 'teamwork', 'css', 'html', 'typescript', 'angular',
            'vue', 'django', 'flask', 'mongodb', 'postgresql', 'redis', 'graphql',
            'rest api', 'microservices', 'ci/cd', 'jenkins', 'terraform', 'azure'
        ]
        
        # Find skills mentioned in job description
        required_skills = []
        for skill in common_skills:
            if skill in job_desc_lower:
                required_skills.append(skill)
        
        # Match user skills with required skills
        matching_skills = []
        missing_skills = []
        
        for req_skill in required_skills:
            if any(req_skill in user_skill or user_skill in req_skill for user_skill in user_skills):
                matching_skills.append(req_skill.title())
            else:
                missing_skills.append(req_skill.title())
        
        # Calculate score
        if required_skills:
            score = int((len(matching_skills) / len(required_skills)) * 100)
        else:
            score = 70  # Default if no specific skills found
        
        # Generate recommendations
        recommendations = []
        if missing_skills:
            recommendations.append(f"Learn these missing skills: {', '.join(missing_skills[:5])}")
        if score < 70:
            recommendations.append("Consider taking online courses to bridge skill gaps")
            recommendations.append("Build projects showcasing required technologies")
        
        learning_resources = []
        for skill in missing_skills[:5]:
            learning_resources.append({
                'skill': skill,
                'resources': [
                    f"{skill} course on Coursera",
                    f"{skill} tutorials on YouTube"
                ],
                'priority': 'high' if skill in missing_skills[:3] else 'medium'
            })
        
        return {
            'success': True,
            'analysis': {
                'matching_skills': matching_skills,
                'missing_skills': missing_skills,
                'partially_matched_skills': [],
                'skill_gap_score': score,  # Use full 0-100 range
                'recommendations': recommendations if recommendations else [
                    "Your skills align well with the job requirements",
                    "Continue building experience in your current areas",
                    "Stay updated with industry trends"
                ],
                'learning_resources': learning_resources,
                'experience_gap': {
                    'years_required': 'Not specified',
                    'years_you_have': len(profile_data.get('experience', [])),
                    'gap': 'Unknown',
                    'advice': 'Focus on quality of experience over quantity'
                },
                'summary': f"You match {len(matching_skills)} out of {len(required_skills)} key skills. " + 
                          ("Strong candidate!" if score >= 70 else "Focus on bridging skill gaps.")
            },
            'method': 'basic'
        }
    
    def _format_experiences(self, experiences):
        """Format experience list for prompt"""
        if not experiences:
            return "No experience listed"
        
        formatted = []
        for exp in experiences[:5]:  # Limit to 5 most recent
            exp_text = f"- {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}"
            if exp.get('duration'):
                exp_text += f" ({exp['duration']})"
            formatted.append(exp_text)
        
        return '\n'.join(formatted)
    
    def _format_education(self, education):
        """Format education list for prompt"""
        if not education:
            return "No education listed"
        
        formatted = []
        for edu in education:
            edu_text = f"- {edu.get('degree', 'N/A')} from {edu.get('school', 'N/A')}"
            if edu.get('field'):
                edu_text += f" in {edu['field']}"
            formatted.append(edu_text)
        
        return '\n'.join(formatted)


# Test
if __name__ == "__main__":
    analyzer = SkillGapAnalyzer()
    
    test_profile = {
        'name': 'John Doe',
        'headline': 'Software Engineer',
        'skills': ['Python', 'JavaScript', 'React', 'SQL'],
        'experience': [
            {'title': 'Software Engineer', 'company': 'Tech Corp', 'duration': '2 years'}
        ],
        'education': [
            {'degree': 'BS Computer Science', 'school': 'University X'}
        ],
        'about': 'Passionate software engineer with 2 years of experience'
    }
    
    test_job = """
    We are looking for a Senior Full Stack Developer with:
    - 5+ years experience in Python and JavaScript
    - Strong knowledge of React, Node.js, and MongoDB
    - Experience with AWS and Docker
    - Machine Learning background preferred
    """
    
    result = analyzer.analyze_skill_gap(test_profile, test_job)
    
    import json
    print(json.dumps(result, indent=2))
