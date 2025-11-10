import re
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Try to import Gemini, fallback to manual parsing if not available
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    
    # Configure Gemini
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
    else:
        GEMINI_AVAILABLE = False
except ImportError:
    GEMINI_AVAILABLE = False


class LinkedInParser:
    """Parse LinkedIn profile data from copy-pasted text"""
    
    def parse_linkedin_text(self, text):
        """
        Parse LinkedIn profile text and extract structured data
        Uses Gemini AI if available, falls back to regex parsing
        
        Args:
            text (str): Full text copied from LinkedIn profile page
            
        Returns:
            dict: Structured profile data
        """
        if not text:
            return None
        
        # Try Gemini AI first
        if GEMINI_AVAILABLE and os.getenv('GEMINI_API_KEY'):
            print("Using Gemini AI for parsing...")
            gemini_result = self._parse_with_gemini(text)
            if gemini_result:
                return gemini_result
            print("Gemini parsing failed, falling back to regex...")
        
        # Fallback to manual parsing
        print("Using manual regex parsing...")
        profile_data = {
            'name': self._extract_name(text),
            'headline': self._extract_headline(text),
            'about': self._extract_about(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'skills': self._extract_skills(text),
            'contact': self._extract_contact(text)
        }
        
        return profile_data
    
    def _parse_with_gemini(self, text):
        """Use Gemini AI to parse LinkedIn profile text"""
        try:
            # Initialize Gemini model
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            prompt = f"""
You are a LinkedIn profile data extractor. Parse the following LinkedIn profile text and extract structured information.

Return ONLY a valid JSON object (no markdown, no code blocks, no explanations) with this exact structure:
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

Important instructions:
1. Extract the PROFILE OWNER's name, not the viewer's name
2. For experience, include up to 5 most recent positions
3. For education, include up to 3 institutions
4. For skills, include up to 10 relevant skills
5. If a field is not available, use empty string "" or empty array []
6. Make sure dates are in a readable format
7. Clean up any UI artifacts or duplicate text
8. For "about" section: Keep it SHORT - maximum 3 lines (around 250 characters)
9. For each experience "description": Keep it CONCISE - maximum 3 lines (around 250 characters) highlighting key achievements only
10. Return ONLY the JSON object, nothing else

LinkedIn Profile Text:
{text[:8000]}
"""
            
            response = model.generate_content(prompt)
            
            if response and response.text:
                # Clean up the response (remove markdown code blocks if present)
                json_text = response.text.strip()
                
                # Remove markdown code blocks
                if json_text.startswith('```'):
                    json_text = re.sub(r'^```json\s*\n', '', json_text)
                    json_text = re.sub(r'^```\s*\n', '', json_text)
                    json_text = re.sub(r'\n```$', '', json_text)
                    json_text = json_text.strip()
                
                # Parse JSON
                profile_data = json.loads(json_text)
                
                print(f"✅ Successfully parsed with Gemini: {profile_data.get('name', 'Unknown')}")
                return profile_data
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Response text: {response.text[:500] if response and response.text else 'No response'}")
            return None
        except Exception as e:
            print(f"❌ Gemini API error: {str(e)}")
            return None
        
        return None
    
    def _extract_name(self, text):
        """Extract name from the text"""
        # The profile owner's name usually appears after certain keywords
        # and before "Follow" or "Message" buttons
        
        lines = text.split('\n')
        
        # First, try to find the name pattern: appears multiple times near top
        # and is followed by headline/job title
        name_candidates = {}
        
        skip_keywords = ['notifications', 'skip to', 'search', 'home', 'network', 'jobs', 
                        'messaging', 'for business', 'learning', 'more', 'follow', 'message',
                        'degree connection', 'contact info', 'connections', 'vedansh dhawan',
                        'me', 'my network', 'keyboard shortcuts', 'close jump menu']
        
        # Look for name patterns in the first 100 lines
        for i, line in enumerate(lines[:100]):
            line = line.strip()
            
            # Skip empty lines and UI elements
            if not line or len(line) < 3 or len(line) > 50:
                continue
            
            # Skip if it contains skip keywords
            if any(keyword in line.lower() for keyword in skip_keywords):
                continue
            
            # Check if it looks like a name (2-4 words, proper case)
            words = line.split()
            if 2 <= len(words) <= 4:
                # Check if all words start with capital letter (proper name)
                if all(word[0].isupper() for word in words if word and word[0].isalpha()):
                    # Avoid common UI text
                    if line not in ['Show More', 'See More', 'View Profile', 'Contact Info']:
                        # Count how many times this name appears
                        name_candidates[line] = name_candidates.get(line, 0) + 1
        
        # The actual profile name typically appears 2-4 times near the top
        # Return the name that appears most frequently (but not too many times)
        if name_candidates:
            # Filter out names that appear too many times (likely UI elements)
            valid_names = {name: count for name, count in name_candidates.items() 
                          if 2 <= count <= 8}
            
            if valid_names:
                # Return the most frequent name
                return max(valid_names, key=valid_names.get)
            elif name_candidates:
                # If no name appears 2+ times, take the first valid one
                return list(name_candidates.keys())[0]
        
        return "Name Not Found"
    
    def _extract_headline(self, text):
        """Extract headline/title"""
        # Headline usually comes after the name
        # Look for common patterns like "CEO at", "Engineer at", etc.
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            # Look for job title patterns
            if any(word in line for word in [' at ', ' @ ', '|', 'CEO', 'CTO', 'Founder', 
                                             'Engineer', 'Developer', 'Manager', 'Director']):
                if len(line) > 10 and len(line) < 200:
                    return line
        
        return ""
    
    def _extract_about(self, text):
        """Extract about/summary section"""
        # Look for text after "About" section
        about_match = re.search(r'(?:About|ABOUT|Summary)\s*\n(.*?)(?:Experience|EXPERIENCE|Education)', 
                               text, re.DOTALL | re.IGNORECASE)
        
        if about_match:
            about_text = about_match.group(1).strip()
            # Clean up common artifacts
            about_text = re.sub(r'…see more|…more|see less', '', about_text)
            if len(about_text) > 20:
                return about_text[:500]  # Limit length
        
        return ""
    
    def _extract_experience(self, text):
        """Extract work experience"""
        experiences = []
        
        # Find the Experience section
        exp_match = re.search(r'(?:Experience|EXPERIENCE)(.*?)(?:Education|EDUCATION|Skills|$)', 
                             text, re.DOTALL | re.IGNORECASE)
        
        if not exp_match:
            return experiences
        
        exp_text = exp_match.group(1)
        
        # Split by common separators
        # Look for job titles followed by company names and dates
        lines = exp_text.split('\n')
        
        current_exp = {}
        for i, line in enumerate(lines):
            line = line.strip()
            
            if not line or len(line) < 3:
                continue
            
            # Look for date patterns (e.g., "Jul 2014 - Present", "2014 - 2021")
            date_pattern = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}|[\d]{4})\s*[-–]\s*(Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}|[\d]{4})'
            date_match = re.search(date_pattern, line, re.IGNORECASE)
            
            if date_match:
                if current_exp and current_exp.get('title'):
                    experiences.append(current_exp)
                current_exp = {
                    'title': '',
                    'company': '',
                    'duration': date_match.group(0),
                    'description': ''
                }
            elif current_exp and not current_exp.get('title') and len(line) < 100:
                current_exp['title'] = line
            elif current_exp and current_exp.get('title') and not current_exp.get('company') and len(line) < 100:
                current_exp['company'] = line
            elif current_exp and current_exp.get('company'):
                # This might be description
                if len(current_exp.get('description', '')) < 300:
                    current_exp['description'] += ' ' + line
        
        # Add last experience
        if current_exp and current_exp.get('title'):
            experiences.append(current_exp)
        
        return experiences[:5]  # Limit to 5 most recent
    
    def _extract_education(self, text):
        """Extract education information"""
        education = []
        
        # Find the Education section
        edu_match = re.search(r'(?:Education|EDUCATION)(.*?)(?:Skills|SKILLS|Interests|$)', 
                             text, re.DOTALL | re.IGNORECASE)
        
        if not edu_match:
            return education
        
        edu_text = edu_match.group(1)
        lines = edu_text.split('\n')
        
        current_edu = {}
        for line in lines:
            line = line.strip()
            
            if not line or len(line) < 3:
                continue
            
            # Look for year patterns (e.g., "2009 - 2011")
            year_pattern = r'(\d{4})\s*[-–]\s*(\d{4})'
            year_match = re.search(year_pattern, line)
            
            if year_match:
                if current_edu and current_edu.get('school'):
                    education.append(current_edu)
                current_edu = {
                    'school': '',
                    'degree': '',
                    'field': '',
                    'dates': year_match.group(0)
                }
            elif current_edu and not current_edu.get('school') and len(line) < 100:
                # Skip common words
                if not any(word in line.lower() for word in ['activities', 'show all']):
                    current_edu['school'] = line
            elif current_edu and current_edu.get('school') and not current_edu.get('degree'):
                # This might be degree
                if ',' in line:
                    parts = line.split(',')
                    current_edu['degree'] = parts[0].strip()
                    if len(parts) > 1:
                        current_edu['field'] = parts[1].strip()
                else:
                    current_edu['degree'] = line
        
        # Add last education
        if current_edu and current_edu.get('school'):
            education.append(current_edu)
        
        return education[:3]  # Limit to 3
    
    def _extract_skills(self, text):
        """Extract skills"""
        skills = []
        
        # Find the Skills section
        skills_match = re.search(r'(?:Skills|SKILLS)(.*?)(?:Interests|INTERESTS|Endorsements|$)', 
                                text, re.DOTALL | re.IGNORECASE)
        
        if not skills_match:
            return skills
        
        skills_text = skills_match.group(1)
        lines = skills_text.split('\n')
        
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip()
            # Skip endorsement counts and common UI elements
            if line and len(line) > 2 and len(line) < 50:
                if not any(word in line.lower() for word in ['endorsement', 'show all', 'endorsed by']):
                    if not line.isdigit():
                        skills.append(line)
        
        return skills[:10]  # Limit to 10 skills
    
    def _extract_contact(self, text):
        """Extract contact information"""
        contact = {
            'email': '',
            'phone': '',
            'location': ''
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Extract location (usually appears near the top)
        lines = text.split('\n')
        for line in lines[:50]:
            line = line.strip()
            # Look for common location patterns
            if 'India' in line or 'United States' in line or 'UK' in line:
                if len(line) < 100:
                    contact['location'] = line
                    break
        
        return contact
