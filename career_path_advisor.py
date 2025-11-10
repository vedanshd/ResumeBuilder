"""
Career Path Advisor
Provides personalized career guidance using Gemini AI
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import json

load_dotenv()


class CareerPathAdvisor:
    """Analyze career trajectory and provide advancement recommendations"""
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.use_ai = True
        else:
            self.use_ai = False
            print("Warning: GEMINI_API_KEY not found. Using basic career suggestions.")
    
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
            
            target_context = f"\nTarget Role: {target_role}" if target_role else "\nNo specific target role specified - recommend best progression paths"
            
            prompt = f"""
You are an expert career advisor. Analyze this professional's career and provide comprehensive guidance.

{profile_summary}
{target_context}

Provide a detailed career path analysis in the following JSON format:

{{
    "current_level": "Current career level assessment (Junior/Mid-level/Senior/Lead/Principal/Executive)",
    "next_role_suggestions": [
        {{
            "title": "Next logical role title",
            "timeframe": "6-12 months or 1-2 years, etc.",
            "rationale": "Why this is a good next step",
            "readiness_score": 75,
            "required_skills": ["skill1", "skill2"],
            "difficulty": "Easy/Medium/Hard"
        }},
        // 3-5 suggestions
    ],
    "skill_roadmap": {{
        "immediate_focus": [
            {{
                "skill": "Skill name",
                "priority": "Critical/High/Medium",
                "learning_resources": ["Resource 1", "Resource 2"],
                "estimated_time": "2-3 months",
                "reason": "Why this skill matters for progression"
            }}
        ],
        "short_term": [
            // Skills for next 6-12 months
        ],
        "long_term": [
            // Skills for 1-3 years
        ]
    }},
    "industry_trends": {{
        "emerging_skills": ["AI/ML", "Cloud Architecture", "etc."],
        "declining_skills": ["Legacy tech that's becoming less relevant"],
        "hot_areas": ["Industry segments with growth"],
        "market_demand": "High/Medium/Low for your field",
        "salary_trends": "Growing/Stable/Declining",
        "recommendations": "How to stay relevant in changing landscape"
    }},
    "career_timeline": {{
        "year_1": {{
            "focus": "Primary goals for year 1",
            "target_position": "Expected role",
            "key_milestones": ["Milestone 1", "Milestone 2"],
            "skills_to_develop": ["Skill 1", "Skill 2"]
        }},
        "year_2": {{
            // Similar structure
        }},
        "year_3": {{
            // Similar structure
        }},
        "year_4": {{
            // Similar structure
        }},
        "year_5": {{
            "focus": "Primary goals for year 5",
            "target_position": "Expected senior role",
            "expected_salary_range": "$XXX,XXX - $XXX,XXX",
            "key_milestones": ["Milestone 1", "Milestone 2"],
            "skills_to_develop": ["Skill 1", "Skill 2"]
        }}
    }},
    "alternative_paths": [
        {{
            "path": "Alternative career direction",
            "description": "What this path looks like",
            "pros": ["Advantage 1", "Advantage 2"],
            "cons": ["Challenge 1", "Challenge 2"],
            "transition_difficulty": "Easy/Medium/Hard"
        }}
    ],
    "certifications": [
        {{
            "name": "Certification name",
            "provider": "Issuing organization",
            "value": "High/Medium/Low",
            "timeframe": "When to get it",
            "cost_estimate": "$XXX - $XXX",
            "roi": "Expected return on investment"
        }}
    ],
    "networking_strategy": {{
        "target_connections": "Types of people to connect with",
        "platforms": ["LinkedIn", "Industry forums", "etc."],
        "events": "Conferences or meetups to attend",
        "communities": "Online communities to join"
    }},
    "summary": "2-3 sentence summary of career outlook and top recommendation"
}}

Be specific, realistic, and actionable. Base recommendations on actual market trends and the user's background.
Consider their current experience level and provide achievable progression steps.
"""
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
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
            return self._basic_career_analysis(profile_data, target_role, years_ahead)
    
    def _basic_career_analysis(self, profile_data, target_role, years_ahead):
        """Fallback: Basic career progression suggestions"""
        
        experiences = profile_data.get('experience', [])
        current_title = experiences[0].get('title', 'Professional') if experiences else 'Professional'
        skills = profile_data.get('skills', [])
        
        # Simple progression logic
        title_lower = current_title.lower()
        
        if 'junior' in title_lower or 'associate' in title_lower:
            next_level = 'Mid-level'
            next_roles = [
                {'title': current_title.replace('Junior', '').replace('Associate', '').strip(), 'timeframe': '1-2 years'},
                {'title': 'Senior ' + current_title.replace('Junior', '').replace('Associate', '').strip(), 'timeframe': '3-4 years'}
            ]
        elif 'senior' in title_lower:
            next_level = 'Lead/Principal'
            next_roles = [
                {'title': 'Lead ' + current_title.replace('Senior', '').strip(), 'timeframe': '1-2 years'},
                {'title': 'Principal ' + current_title.replace('Senior', '').strip(), 'timeframe': '2-3 years'},
                {'title': 'Engineering Manager', 'timeframe': '2-3 years'}
            ]
        elif 'lead' in title_lower or 'principal' in title_lower:
            next_level = 'Executive'
            next_roles = [
                {'title': 'Director of Engineering', 'timeframe': '2-3 years'},
                {'title': 'VP of Engineering', 'timeframe': '4-5 years'}
            ]
        else:
            next_level = 'Advanced'
            next_roles = [
                {'title': 'Senior ' + current_title, 'timeframe': '1-2 years'},
                {'title': 'Lead ' + current_title, 'timeframe': '3-4 years'}
            ]
        
        return {
            'success': True,
            'analysis': {
                'current_level': next_level,
                'next_role_suggestions': [
                    {
                        'title': role['title'],
                        'timeframe': role['timeframe'],
                        'rationale': 'Natural career progression based on experience',
                        'readiness_score': 70,
                        'required_skills': skills[:5] if skills else ['Leadership', 'Technical Skills'],
                        'difficulty': 'Medium'
                    }
                    for role in next_roles[:3]
                ],
                'skill_roadmap': {
                    'immediate_focus': [
                        {
                            'skill': 'Leadership',
                            'priority': 'High',
                            'learning_resources': ['Leadership courses on Coursera', 'Management books'],
                            'estimated_time': '3-6 months',
                            'reason': 'Essential for advancement'
                        }
                    ],
                    'short_term': [
                        {
                            'skill': 'System Design',
                            'priority': 'High',
                            'learning_resources': ['System design courses', 'Architecture patterns'],
                            'estimated_time': '6-12 months',
                            'reason': 'Required for senior roles'
                        }
                    ],
                    'long_term': [
                        {
                            'skill': 'Strategic Planning',
                            'priority': 'Medium',
                            'learning_resources': ['MBA courses', 'Business strategy books'],
                            'estimated_time': '1-2 years',
                            'reason': 'For executive transition'
                        }
                    ]
                },
                'industry_trends': {
                    'emerging_skills': ['AI/ML', 'Cloud Computing', 'DevOps', 'Cybersecurity'],
                    'declining_skills': ['Legacy systems'],
                    'hot_areas': ['Technology', 'Remote work'],
                    'market_demand': 'High',
                    'salary_trends': 'Growing',
                    'recommendations': 'Stay updated with emerging technologies and develop leadership skills'
                },
                'career_timeline': {
                    f'year_{i}': {
                        'focus': f'Focus for year {i}',
                        'target_position': next_roles[min(i-1, len(next_roles)-1)]['title'] if i <= len(next_roles) else 'Executive role',
                        'key_milestones': ['Skill development', 'Project leadership'],
                        'skills_to_develop': skills[:2] if skills else ['Leadership', 'Technical skills']
                    }
                    for i in range(1, years_ahead + 1)
                },
                'alternative_paths': [
                    {
                        'path': 'Management Track',
                        'description': 'Transition to people management',
                        'pros': ['Leadership opportunities', 'Higher earning potential'],
                        'cons': ['Less hands-on technical work'],
                        'transition_difficulty': 'Medium'
                    },
                    {
                        'path': 'Technical Expert Track',
                        'description': 'Deep specialization in technical domain',
                        'pros': ['Deep expertise', 'Technical influence'],
                        'cons': ['Narrower scope'],
                        'transition_difficulty': 'Easy'
                    }
                ],
                'certifications': [
                    {
                        'name': 'PMP',
                        'provider': 'PMI',
                        'value': 'Medium',
                        'timeframe': 'Year 2',
                        'cost_estimate': '$500 - $1000',
                        'roi': 'Moderate salary increase'
                    }
                ],
                'networking_strategy': {
                    'target_connections': 'Senior leaders in your field',
                    'platforms': ['LinkedIn', 'Industry conferences'],
                    'events': 'Tech conferences and meetups',
                    'communities': 'Professional associations'
                },
                'summary': f'You are at {next_level} level. Focus on developing leadership skills and technical expertise to advance to {next_roles[0]["title"]} within {next_roles[0]["timeframe"]}.'
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
            if exp.get('description'):
                exp_text += f"\n  {exp['description'][:200]}"
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
    advisor = CareerPathAdvisor()
    
    test_profile = {
        'name': 'John Doe',
        'headline': 'Senior Software Engineer',
        'skills': ['Python', 'JavaScript', 'React', 'SQL', 'AWS', 'Docker', 'Kubernetes'],
        'experience': [
            {
                'title': 'Senior Software Engineer',
                'company': 'Tech Corp',
                'duration': '3 years',
                'description': 'Lead backend development team, architected microservices'
            },
            {
                'title': 'Software Engineer',
                'company': 'StartupXYZ',
                'duration': '2 years',
                'description': 'Full-stack development'
            }
        ],
        'education': [
            {'degree': 'BS Computer Science', 'school': 'University X'}
        ],
        'about': 'Passionate software engineer with 5 years of experience in building scalable systems'
    }
    
    result = advisor.analyze_career_path(test_profile, target_role="Engineering Manager", years_ahead=5)
    
    print(json.dumps(result, indent=2))
