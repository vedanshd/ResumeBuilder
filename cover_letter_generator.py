import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class CoverLetterGenerator:
    """Generate cover letters using Gemini AI"""
    
    def __init__(self):
        """Initialize the CoverLetterGenerator with Gemini AI"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
            print("⚠️  Warning: GEMINI_API_KEY not found. Using basic template.")
        
        self.output_folder = 'generated_resumes'
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
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
                f"- {exp.get('title', '')} at {exp.get('company', '')} ({exp.get('duration', '')})"
                for exp in profile_data.get('experience', [])[:3]
            ])
            
            education_summary = "\n".join([
                f"- {edu.get('degree', '')} from {edu.get('school', '')}"
                for edu in profile_data.get('education', [])[:2]
            ])
            
            skills = ", ".join(profile_data.get('skills', [])[:8])
            
            prompt = f"""
You are a professional career coach and cover letter writer. Write a compelling, personalized cover letter based on the candidate's profile and the job description.

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
3. Start with a strong opening that shows genuine enthusiasm for THIS specific role
4. Highlight 2-3 MOST RELEVANT experiences/achievements that directly match the job requirements
5. Use SPECIFIC examples and metrics when possible (e.g., "increased efficiency by 30%")
6. Demonstrate understanding of the company's needs from the job description
7. Explain WHY you're excited about THIS role and company specifically
8. Include 1-2 key technical skills or tools mentioned in the job description
9. End with a confident call to action (e.g., "I look forward to discussing how my experience can contribute to your team")
10. Sign off with "Sincerely," followed by the candidate's name
11. Use professional but warm and authentic tone
12. Make it personalized to THIS job - NOT a generic template
13. DO NOT use placeholders like [Your Name], [Company Name] - use actual information or omit
14. Keep paragraphs short (3-4 sentences each) for readability
15. Focus on VALUE you bring, not just what you want

Write ONLY the cover letter text (no subject line, no additional commentary).
"""
            
            response = model.generate_content(prompt)
            
            if response and response.text:
                cover_letter = response.text.strip()
                
                # Clean up any remaining placeholders
                cover_letter = cover_letter.replace('[Your Name]', profile_data.get('name', ''))
                cover_letter = cover_letter.replace('[Company Name]', 'the company')
                
                return cover_letter
            
        except Exception as e:
            print(f"Error generating cover letter with Gemini: {str(e)}")
            # Fallback to basic template
            return self._generate_basic_cover_letter(profile_data, job_description)
        
        return None
    
    def _generate_basic_cover_letter(self, profile_data, job_description):
        """Fallback basic cover letter template"""
        name = profile_data.get('name', 'Candidate')
        headline = profile_data.get('headline', 'Professional')
        
        # Extract company name from job description if possible
        company = 'your organization'
        
        # Try to find role/position in job description
        role = 'the position'
        jd_lower = job_description.lower()
        if 'looking for' in jd_lower or 'seeking' in jd_lower:
            # Basic extraction attempt
            pass
        
        # Get first experience
        recent_exp = profile_data.get('experience', [{}])[0] if profile_data.get('experience') else {}
        exp_title = recent_exp.get('title', 'my previous role')
        exp_company = recent_exp.get('company', 'my previous company')
        
        # Get top skills
        skills = profile_data.get('skills', [])
        skill_text = ', '.join(skills[:5]) if skills else 'various technical skills'
        
        cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in {role} at {company}. As a {headline}, I am excited about the opportunity to bring my expertise to your team and contribute to your organization's success.

In my role as {exp_title} at {exp_company}, I developed strong capabilities in {skill_text}. I have consistently delivered results by leveraging my technical knowledge and collaborative approach to solve complex challenges. My experience aligns well with the requirements outlined in your job description.

What particularly excites me about this opportunity is the chance to work with a team that values innovation and excellence. I am confident that my background in {headline.lower()}, combined with my passion for continuous learning, would enable me to make meaningful contributions from day one.

I would welcome the opportunity to discuss how my skills and experience can benefit your team. Thank you for considering my application. I look forward to the possibility of contributing to {company}'s continued success.

Sincerely,
{name}"""
        
        return cover_letter
    
    def create_cover_letter_pdf(self, profile_data, job_description):
        """
        Create a PDF cover letter
        
        Args:
            profile_data (dict): Resume/profile data
            job_description (str): Job description
            
        Returns:
            str: Path to generated PDF file
        """
        # Generate cover letter content with Gemini
        cover_letter_text = self.generate_cover_letter_content(profile_data, job_description)
        
        if not cover_letter_text:
            return None
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"cover_letter_{timestamp}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              rightMargin=0.75*inch, leftMargin=0.75*inch,
                              topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        # Container for PDF elements
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Header style (name and contact)
        name_style = ParagraphStyle(
            'NameStyle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        
        contact_style = ParagraphStyle(
            'ContactStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            spaceAfter=20,
            alignment=TA_LEFT
        )
        
        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            leading=16
        )
        
        # Add header with contact info
        story.append(Paragraph(profile_data.get('name', 'Candidate'), name_style))
        
        contact = profile_data.get('contact', {})
        contact_info = []
        if contact.get('email'):
            contact_info.append(contact['email'])
        if contact.get('phone'):
            contact_info.append(contact['phone'])
        if contact.get('location'):
            contact_info.append(contact['location'])
        
        if contact_info:
            story.append(Paragraph(' | '.join(contact_info), contact_style))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Add date
        date_str = datetime.now().strftime('%B %d, %Y')
        story.append(Paragraph(date_str, body_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Add cover letter content (split by paragraphs)
        paragraphs = cover_letter_text.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), body_style))
        
        # Build PDF
        doc.build(story)
        
        return filename
