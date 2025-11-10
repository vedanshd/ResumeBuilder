"""
Interview Question Generator
Generates personalized interview questions based on resume and job description
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()


class InterviewQuestionGenerator:
    """Generate personalized interview questions for job preparation"""
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.use_ai = True
        else:
            self.use_ai = False
            print("Warning: GEMINI_API_KEY not found. Using basic question templates.")
    
    def generate_questions(self, profile_data, job_description=None, question_count=25):
        """
        Generate personalized interview questions
        
        Args:
            profile_data (dict): User's profile data from LinkedIn
            job_description (str): Target job description (optional)
            question_count (int): Number of questions to generate (default 25)
            
        Returns:
            dict: Interview questions with categories, difficulty, and tips
        """
        if self.use_ai:
            return self._generate_with_ai(profile_data, job_description, question_count)
        else:
            return self._generate_basic_questions(profile_data, job_description)
    
    def _generate_with_ai(self, profile_data, job_description, question_count):
        """Use Gemini AI to generate intelligent, personalized interview questions"""
        
        try:
            # Prepare profile summary
            user_skills = profile_data.get('skills', [])
            experiences = profile_data.get('experience', [])
            education = profile_data.get('education', [])
            current_title = experiences[0].get('title', 'N/A') if experiences else 'N/A'
            
            profile_summary = f"""
CANDIDATE PROFILE:
Name: {profile_data.get('name', 'N/A')}
Current/Recent Role: {current_title}
Headline: {profile_data.get('headline', 'N/A')}

Skills: {', '.join(user_skills[:25]) if user_skills else 'None listed'}

Experience History:
{self._format_experiences(experiences)}

Education:
{self._format_education(education)}

About:
{profile_data.get('about', 'N/A')[:500]}
"""
            
            job_context = ""
            if job_description:
                job_context = f"""

TARGET JOB DESCRIPTION:
{job_description[:2000]}

NOTE: Questions should be highly relevant to this specific job posting.
"""
            else:
                job_context = "\n\nNOTE: No specific job provided. Generate questions based on the candidate's background and common interview patterns for their field."
            
            prompt = f"""
You are an expert interview coach and technical recruiter. Generate a comprehensive, personalized set of interview questions for this candidate.

{profile_summary}
{job_context}

Generate EXACTLY {question_count} interview questions in the following JSON format:

{{
    "technical_questions": [
        {{
            "question": "Explain how you would design a scalable microservices architecture",
            "category": "System Design",
            "difficulty": "Hard",
            "why_asking": "Tests your understanding of distributed systems mentioned in your resume",
            "key_points": ["Mention load balancing", "Discuss database sharding", "Address fault tolerance"],
            "star_template": {{
                "situation": "Describe a project where you implemented this",
                "task": "What was your specific responsibility?",
                "action": "What steps did you take?",
                "result": "What was the measurable outcome?"
            }},
            "red_flags": ["Avoid being too theoretical", "Don't skip over scalability concerns"],
            "follow_up_questions": [
                "How would you handle service failures?",
                "What monitoring tools would you use?"
            ]
        }}
    ],
    "behavioral_questions": [
        {{
            "question": "Tell me about a time when you had to deal with a difficult team member",
            "category": "Teamwork & Collaboration",
            "difficulty": "Medium",
            "why_asking": "You mentioned leading teams in your experience at [Company]",
            "key_points": ["Show empathy and communication skills", "Demonstrate conflict resolution", "Highlight positive outcome"],
            "star_template": {{
                "situation": "Set the context - what was the conflict about?",
                "task": "What was at stake? What needed to be resolved?",
                "action": "What specific steps did you take to address the situation?",
                "result": "How did it turn out? What did you learn?"
            }},
            "good_answer_example": "Brief example of a strong answer approach",
            "red_flags": ["Don't blame others entirely", "Avoid being vague about your role"]
        }}
    ],
    "experience_based_questions": [
        {{
            "question": "I see you worked on [specific project/technology]. Can you walk me through your contribution?",
            "category": "Experience Verification",
            "difficulty": "Medium",
            "why_asking": "Directly from your resume - verifying your actual involvement",
            "key_points": ["Be specific about YOUR role vs team's role", "Mention concrete deliverables", "Discuss challenges overcome"],
            "preparation_tip": "Review this project in detail before the interview",
            "likely_follow_ups": [
                "What was the biggest technical challenge?",
                "How did you measure success?",
                "What would you do differently now?"
            ]
        }}
    ],
    "company_culture_questions": [
        {{
            "question": "Why do you want to work for our company?",
            "category": "Cultural Fit",
            "difficulty": "Medium",
            "why_asking": "Assessing genuine interest and culture alignment",
            "key_points": ["Research the company's mission and values", "Connect your experience to their needs", "Show enthusiasm"],
            "preparation_tip": "Research the company's recent news, products, and culture",
            "avoid": ["Don't just talk about salary/benefits", "Avoid generic answers"]
        }}
    ],
    "situational_questions": [
        {{
            "question": "How would you handle a situation where you're assigned a project with an unrealistic deadline?",
            "category": "Problem Solving",
            "difficulty": "Medium",
            "why_asking": "Tests your prioritization and communication skills",
            "key_points": ["Show you can assess scope realistically", "Demonstrate communication with stakeholders", "Discuss negotiation or trade-offs"],
            "good_approach": "Framework for answering this type of question"
        }}
    ],
    "weakness_questions": [
        {{
            "question": "I notice you have a gap in employment from [date] to [date]. Can you explain?",
            "category": "Resume Gaps & Concerns",
            "difficulty": "Hard",
            "why_asking": "Addressing potential red flags from your resume",
            "key_points": ["Be honest but positive", "Emphasize what you learned/did during that time", "Pivot to current readiness"],
            "preparation_tip": "Prepare honest, concise explanation in advance",
            "avoid": ["Don't be defensive", "Don't overshare personal details"]
        }}
    ],
    "questions_to_ask_interviewer": [
        {{
            "question": "What does success look like in this role after 6 months?",
            "why_effective": "Shows you're thinking about performance and impact",
            "category": "Role Clarity"
        }},
        {{
            "question": "What are the biggest challenges facing the team right now?",
            "why_effective": "Demonstrates problem-solving mindset and genuine interest",
            "category": "Team Dynamics"
        }},
        {{
            "question": "How does the company support professional development and learning?",
            "why_effective": "Shows commitment to growth and long-term thinking",
            "category": "Career Growth"
        }}
    ],
    "overall_strategy": {{
        "strengths_to_highlight": [
            "Based on resume, emphasize these 3-5 key strengths"
        ],
        "potential_concerns": [
            "Areas where you might face skepticism (lack of specific experience, etc.)"
        ],
        "preparation_priorities": [
            "Top 3-5 things to prepare before the interview"
        ],
        "company_research_checklist": [
            "Recent company news",
            "Product/service offerings",
            "Company culture and values",
            "Team structure",
            "Competitors and market position"
        ]
    }},
    "mock_interview_scorecard": {{
        "criteria": [
            {{
                "area": "Technical Competence",
                "weight": 30,
                "evaluation_points": ["Depth of knowledge", "Problem-solving approach", "Code quality if applicable"]
            }},
            {{
                "area": "Communication Skills",
                "weight": 25,
                "evaluation_points": ["Clarity", "Conciseness", "Active listening"]
            }},
            {{
                "area": "Cultural Fit",
                "weight": 20,
                "evaluation_points": ["Values alignment", "Team collaboration", "Adaptability"]
            }},
            {{
                "area": "Experience Relevance",
                "weight": 15,
                "evaluation_points": ["Direct experience with required skills", "Transferable skills", "Learning agility"]
            }},
            {{
                "area": "Professionalism",
                "weight": 10,
                "evaluation_points": ["Punctuality", "Preparedness", "Follow-up"]
            }}
        ]
    }}
}}

CRITICAL INSTRUCTIONS:
1. Make questions SPECIFIC to this candidate's background - reference actual companies, technologies, or experiences from their resume
2. Mix difficulty levels: 40% Easy, 40% Medium, 20% Hard
3. Include questions that address any gaps or weaknesses in the resume
4. For technical roles, include coding/system design questions based on their stated skills
5. For each question, explain WHY it's being asked in context of their profile
6. Provide actionable preparation tips, not generic advice
7. Include realistic follow-up questions interviewers might ask
8. Generate questions that test DEPTH of knowledge in their claimed skills
9. If job description provided, heavily weight questions toward that specific role
10. Include behavioral questions based on their actual work experiences

Return ONLY valid JSON, no markdown formatting.
"""
            
            response = self.model.generate_content(prompt)
            json_str = self._extract_json(response.text)
            questions_data = json.loads(json_str)
            
            print(f"✅ Generated {question_count} personalized interview questions with AI")
            
            return {
                'success': True,
                'questions': questions_data,
                'total_questions': self._count_questions(questions_data),
                'method': 'ai_powered',
                'personalization_level': 'high'
            }
            
        except Exception as e:
            print(f"❌ AI question generation error: {str(e)}")
            return self._generate_basic_questions(profile_data, job_description)
    
    def _generate_basic_questions(self, profile_data, job_description):
        """Generate basic template questions when AI is unavailable"""
        
        current_title = profile_data.get('experience', [{}])[0].get('title', 'professional') if profile_data.get('experience') else 'professional'
        skills = profile_data.get('skills', [])
        
        basic_questions = {
            "technical_questions": [
                {
                    "question": f"Explain your experience with {skills[0] if skills else 'your main technical skill'}",
                    "category": "Technical Skills",
                    "difficulty": "Medium",
                    "why_asking": "Listed on your resume",
                    "key_points": ["Provide specific examples", "Mention projects", "Discuss challenges"]
                },
                {
                    "question": "Describe a challenging technical problem you solved",
                    "category": "Problem Solving",
                    "difficulty": "Medium",
                    "key_points": ["Explain the problem clearly", "Describe your approach", "Share the outcome"]
                },
                {
                    "question": "How do you stay updated with the latest technology trends?",
                    "category": "Continuous Learning",
                    "difficulty": "Easy",
                    "key_points": ["Mention specific resources", "Discuss recent learnings", "Show passion"]
                }
            ],
            "behavioral_questions": [
                {
                    "question": "Tell me about yourself and your background",
                    "category": "Introduction",
                    "difficulty": "Easy",
                    "key_points": ["Keep it under 2 minutes", "Focus on professional journey", "Connect to this role"],
                    "star_template": {
                        "situation": "Your current/recent role",
                        "task": "What you're responsible for",
                        "action": "Key achievements",
                        "result": "Why you're interested in this opportunity"
                    }
                },
                {
                    "question": "Describe a time when you had to work under pressure",
                    "category": "Stress Management",
                    "difficulty": "Medium",
                    "key_points": ["Show composure", "Explain prioritization", "Highlight successful outcome"],
                    "star_template": {
                        "situation": "What was the high-pressure scenario?",
                        "task": "What was expected of you?",
                        "action": "How did you manage it?",
                        "result": "What was achieved?"
                    }
                },
                {
                    "question": "Tell me about a time you failed and what you learned",
                    "category": "Growth Mindset",
                    "difficulty": "Hard",
                    "key_points": ["Be honest", "Focus on learning", "Show how you've improved"],
                    "red_flags": ["Don't blame others", "Don't minimize the failure"]
                },
                {
                    "question": "How do you handle conflicts with team members?",
                    "category": "Teamwork",
                    "difficulty": "Medium",
                    "key_points": ["Show empathy", "Demonstrate communication", "Focus on resolution"]
                }
            ],
            "experience_based_questions": [
                {
                    "question": f"What was your role and contribution as {current_title}?",
                    "category": "Experience Verification",
                    "difficulty": "Medium",
                    "key_points": ["Be specific about your role", "Quantify impact", "Mention team size if applicable"]
                }
            ],
            "company_culture_questions": [
                {
                    "question": "Why do you want to work here?",
                    "category": "Cultural Fit",
                    "difficulty": "Medium",
                    "preparation_tip": "Research company mission, values, and recent news"
                },
                {
                    "question": "Where do you see yourself in 5 years?",
                    "category": "Career Goals",
                    "difficulty": "Easy",
                    "key_points": ["Show ambition", "Align with company growth", "Be realistic"]
                }
            ],
            "questions_to_ask_interviewer": [
                {
                    "question": "What does success look like in this role?",
                    "why_effective": "Shows performance orientation",
                    "category": "Role Clarity"
                },
                {
                    "question": "What are the biggest challenges facing the team?",
                    "why_effective": "Demonstrates problem-solving mindset",
                    "category": "Team Dynamics"
                },
                {
                    "question": "How does the company support professional development?",
                    "why_effective": "Shows commitment to growth",
                    "category": "Career Growth"
                },
                {
                    "question": "What is the team culture like?",
                    "why_effective": "Assesses fit and work environment",
                    "category": "Culture"
                }
            ],
            "overall_strategy": {
                "preparation_priorities": [
                    "Research the company thoroughly",
                    "Review your resume and be ready to discuss any point",
                    "Prepare 2-3 strong examples for STAR method questions",
                    "Practice your 'tell me about yourself' answer",
                    "Prepare thoughtful questions for the interviewer"
                ],
                "company_research_checklist": [
                    "Company website and mission",
                    "Recent news and press releases",
                    "Product or service offerings",
                    "LinkedIn profiles of interviewers",
                    "Glassdoor reviews"
                ]
            }
        }
        
        print("⚠️ Using basic question templates. Enable AI for personalized questions.")
        
        return {
            'success': True,
            'questions': basic_questions,
            'total_questions': self._count_questions(basic_questions),
            'method': 'template_based',
            'personalization_level': 'low',
            'note': 'Configure GEMINI_API_KEY for AI-powered personalized questions'
        }
    
    def _format_experiences(self, experiences):
        """Format experience list for AI prompts"""
        if not experiences:
            return "No experience listed"
        
        formatted = []
        for i, exp in enumerate(experiences[:5], 1):
            formatted.append(f"""
{i}. {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}
   Duration: {exp.get('duration', 'N/A')}
   Description: {exp.get('description', 'N/A')[:300]}
""")
        
        return "\n".join(formatted)
    
    def _format_education(self, education):
        """Format education list for AI prompts"""
        if not education:
            return "No education listed"
        
        formatted = []
        for i, edu in enumerate(education[:3], 1):
            formatted.append(f"{i}. {edu.get('degree', 'N/A')} in {edu.get('field', 'N/A')} from {edu.get('school', 'N/A')}")
        
        return "\n".join(formatted)
    
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
    
    def _count_questions(self, questions_data):
        """Count total number of questions generated"""
        count = 0
        question_categories = ['technical_questions', 'behavioral_questions', 
                             'experience_based_questions', 'company_culture_questions',
                             'situational_questions', 'weakness_questions']
        
        for category in question_categories:
            if category in questions_data:
                count += len(questions_data[category])
        
        return count
