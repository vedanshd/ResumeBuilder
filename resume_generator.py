from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
import os


class ResumeGenerator:
    """Generate PDF resumes from LinkedIn profile data"""
    
    def __init__(self):
        self.output_folder = 'generated_resumes'
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def create_resume(self, profile_data, template='modern'):
        """
        Create a PDF resume from profile data
        
        Args:
            profile_data (dict): Scraped LinkedIn profile data
            template (str): Template style - 'modern', 'classic', 'executive', 'creative'
            
        Returns:
            str: Path to generated PDF file
        """
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"resume_{template}_{timestamp}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              rightMargin=0.75*inch, leftMargin=0.75*inch,
                              topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        # Container for PDF elements
        story = []
        
        # Select template and build resume
        if template == 'classic':
            story = self._build_classic_template(profile_data)
        elif template == 'executive':
            story = self._build_executive_template(profile_data)
        elif template == 'creative':
            story = self._build_creative_template(profile_data)
        else:  # Default to modern
            story = self._build_modern_template(profile_data)
        
        # Build PDF
        doc.build(story)
        
        return filename
    
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
        
        headline_style = ParagraphStyle(
            'HeadlineStyle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#666666'),
            spaceAfter=12,
            alignment=TA_CENTER
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
        
        # Build content
        story.append(Paragraph(profile_data.get('name', 'Name Not Available'), name_style))
        
        if profile_data.get('headline'):
            story.append(Paragraph(profile_data['headline'], headline_style))
        
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
        
        # Summary
        if profile_data.get('about'):
            story.append(Paragraph('SUMMARY', section_title_style))
            story.append(Paragraph(profile_data['about'], body_style))
            story.append(Spacer(1, 0.15*inch))
        
        # Experience
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
                    # Format description with bullet points if it's long
                    desc = exp['description']
                    if len(desc) > 150:
                        # Split into sentences and create bullet points
                        sentences = [s.strip() for s in desc.replace('. ', '.|').split('|') if s.strip()]
                        for sentence in sentences[:5]:  # Limit to 5 bullets
                            if sentence:
                                bullet_style = ParagraphStyle('Bullet', parent=body_style, leftIndent=15, firstLineIndent=-10)
                                story.append(Paragraph(f"• {sentence}", bullet_style))
                    else:
                        story.append(Paragraph(exp['description'], body_style))
                
                story.append(Spacer(1, 0.1*inch))
        
        # Education
        education = profile_data.get('education', [])
        if education:
            story.append(Paragraph('EDUCATION', section_title_style))
            for edu in education:
                school_text = f"<b>{edu.get('school', '')}</b>"
                story.append(Paragraph(school_text, body_style))
                
                degree_parts = []
                if edu.get('degree'):
                    degree_parts.append(edu['degree'])
                if edu.get('field'):
                    degree_parts.append(edu['field'])
                
                if degree_parts:
                    degree_text = ' - '.join(degree_parts)
                    story.append(Paragraph(degree_text, body_style))
                
                if edu.get('dates'):
                    dates_text = f"<i>{edu['dates']}</i>"
                    story.append(Paragraph(dates_text, body_style))
                
                story.append(Spacer(1, 0.1*inch))
        
        # Skills
        skills = profile_data.get('skills', [])
        if skills:
            story.append(Paragraph('SKILLS', section_title_style))
            skills_text = ' • '.join(skills)
            story.append(Paragraph(skills_text, body_style))
        
        return story
    
    def _build_classic_template(self, profile_data):
        """Build classic template resume - Traditional black and white"""
        story = []
        styles = getSampleStyleSheet()
        
        # Classic styles - formal and traditional
        name_style = ParagraphStyle(
            'NameStyle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.black,
            spaceAfter=4,
            alignment=TA_CENTER,
            fontName='Times-Bold'
        )
        
        headline_style = ParagraphStyle(
            'HeadlineStyle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.black,
            spaceAfter=8,
            alignment=TA_CENTER,
            fontName='Times-Italic'
        )
        
        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.black,
            spaceAfter=6,
            spaceBefore=10,
            fontName='Times-Bold',
            borderWidth=0,
            borderPadding=0,
            underlineWidth=1,
            underlineOffset=-2
        )
        
        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=4,
            fontName='Times-Roman'
        )
        
        # Build content
        story.append(Paragraph(profile_data.get('name', 'Name Not Available').upper(), name_style))
        
        if profile_data.get('headline'):
            story.append(Paragraph(profile_data['headline'], headline_style))
        
        contact = profile_data.get('contact', {})
        contact_info = []
        if contact.get('location'):
            contact_info.append(contact['location'])
        if contact.get('email'):
            contact_info.append(contact['email'])
        if contact.get('phone'):
            contact_info.append(contact['phone'])
        
        if contact_info:
            story.append(Paragraph(' • '.join(contact_info), headline_style))
        
        story.append(Spacer(1, 0.15*inch))
        
        # Summary
        if profile_data.get('about'):
            story.append(Paragraph('<u>PROFESSIONAL SUMMARY</u>', section_title_style))
            story.append(Paragraph(profile_data['about'], body_style))
            story.append(Spacer(1, 0.1*inch))
        
        # Experience
        experiences = profile_data.get('experience', [])
        if experiences:
            story.append(Paragraph('<u>WORK EXPERIENCE</u>', section_title_style))
            for exp in experiences:
                title_text = f"<b>{exp.get('title', '')}</b>, {exp.get('company', '')}"
                story.append(Paragraph(title_text, body_style))
                
                if exp.get('duration'):
                    duration_text = f"<i>{exp['duration']}</i>"
                    story.append(Paragraph(duration_text, body_style))
                
                if exp.get('description'):
                    # Format description with bullet points if it's long
                    desc = exp['description']
                    if len(desc) > 150:
                        # Split into sentences and create bullet points
                        sentences = [s.strip() for s in desc.replace('. ', '.|').split('|') if s.strip()]
                        for sentence in sentences[:5]:  # Limit to 5 bullets
                            if sentence:
                                bullet_style = ParagraphStyle('Bullet', parent=body_style, leftIndent=15, firstLineIndent=-10)
                                story.append(Paragraph(f"• {sentence}", bullet_style))
                    else:
                        story.append(Paragraph(exp['description'], body_style))
                
                story.append(Spacer(1, 0.08*inch))
        
        # Education
        education = profile_data.get('education', [])
        if education:
            story.append(Paragraph('<u>EDUCATION</u>', section_title_style))
            for edu in education:
                school_text = f"<b>{edu.get('school', '')}</b>"
                story.append(Paragraph(school_text, body_style))
                
                degree_parts = []
                if edu.get('degree'):
                    degree_parts.append(edu['degree'])
                if edu.get('field'):
                    degree_parts.append(edu['field'])
                
                if degree_parts:
                    degree_text = ', '.join(degree_parts)
                    story.append(Paragraph(degree_text, body_style))
                
                if edu.get('dates'):
                    dates_text = f"{edu['dates']}"
                    story.append(Paragraph(dates_text, body_style))
                
                story.append(Spacer(1, 0.08*inch))
        
        # Skills
        skills = profile_data.get('skills', [])
        if skills:
            story.append(Paragraph('<u>SKILLS</u>', section_title_style))
            skills_text = ', '.join(skills)
            story.append(Paragraph(skills_text, body_style))
        
        return story
    
    def _build_executive_template(self, profile_data):
        """Build executive template resume - Professional with sidebar accent"""
        story = []
        styles = getSampleStyleSheet()
        
        # Executive styles - sophisticated dark theme
        name_style = ParagraphStyle(
            'NameStyle',
            parent=styles['Heading1'],
            fontSize=26,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=4,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            letterSpacing=1
        )
        
        headline_style = ParagraphStyle(
            'HeadlineStyle',
            parent=styles['Normal'],
            fontSize=13,
            textColor=colors.HexColor('#555555'),
            spaceAfter=10,
            alignment=TA_LEFT,
            fontName='Helvetica'
        )
        
        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=0,
            leftIndent=0,
            backColor=colors.HexColor('#f8f9fa'),
            borderPadding=6
        )
        
        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            spaceAfter=5,
            fontName='Helvetica',
            alignment=TA_LEFT
        )
        
        contact_style = ParagraphStyle(
            'ContactStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            spaceAfter=8,
            alignment=TA_LEFT
        )
        
        # Build content
        story.append(Paragraph(profile_data.get('name', 'Name Not Available'), name_style))
        
        if profile_data.get('headline'):
            story.append(Paragraph(profile_data['headline'], headline_style))
        
        contact = profile_data.get('contact', {})
        contact_parts = []
        if contact.get('email'):
            contact_parts.append(f"Email: {contact['email']}")
        if contact.get('phone'):
            contact_parts.append(f"Phone: {contact['phone']}")
        if contact.get('location'):
            contact_parts.append(f"Location: {contact['location']}")
        
        if contact_parts:
            story.append(Paragraph(' | '.join(contact_parts), contact_style))
        
        story.append(Spacer(1, 0.15*inch))
        
        # Summary
        if profile_data.get('about'):
            story.append(Paragraph('EXECUTIVE SUMMARY', section_title_style))
            story.append(Spacer(1, 0.05*inch))
            story.append(Paragraph(profile_data['about'], body_style))
            story.append(Spacer(1, 0.1*inch))
        
        # Experience
        experiences = profile_data.get('experience', [])
        if experiences:
            story.append(Paragraph('PROFESSIONAL EXPERIENCE', section_title_style))
            story.append(Spacer(1, 0.05*inch))
            for exp in experiences:
                title_text = f"<b>{exp.get('title', '')}</b>"
                story.append(Paragraph(title_text, body_style))
                
                company_text = f"{exp.get('company', '')}"
                if exp.get('duration'):
                    company_text += f" | {exp['duration']}"
                story.append(Paragraph(company_text, contact_style))
                
                if exp.get('description'):
                    # Format description with bullet points if it's long
                    desc = exp['description']
                    if len(desc) > 150:
                        # Split into sentences and create bullet points
                        sentences = [s.strip() for s in desc.replace('. ', '.|').split('|') if s.strip()]
                        for sentence in sentences[:5]:  # Limit to 5 bullets
                            if sentence:
                                bullet_style = ParagraphStyle('Bullet', parent=body_style, leftIndent=15, firstLineIndent=-10)
                                story.append(Paragraph(f"• {sentence}", bullet_style))
                    else:
                        story.append(Paragraph(exp['description'], body_style))
                
                story.append(Spacer(1, 0.12*inch))
        
        # Education
        education = profile_data.get('education', [])
        if education:
            story.append(Paragraph('EDUCATION', section_title_style))
            story.append(Spacer(1, 0.05*inch))
            for edu in education:
                school_text = f"<b>{edu.get('school', '')}</b>"
                story.append(Paragraph(school_text, body_style))
                
                degree_parts = []
                if edu.get('degree'):
                    degree_parts.append(edu['degree'])
                if edu.get('field'):
                    degree_parts.append(edu['field'])
                if edu.get('dates'):
                    degree_parts.append(edu['dates'])
                
                if degree_parts:
                    degree_text = ' | '.join(degree_parts)
                    story.append(Paragraph(degree_text, contact_style))
                
                story.append(Spacer(1, 0.08*inch))
        
        # Skills
        skills = profile_data.get('skills', [])
        if skills:
            story.append(Paragraph('CORE COMPETENCIES', section_title_style))
            story.append(Spacer(1, 0.05*inch))
            skills_text = ' • '.join(skills)
            story.append(Paragraph(skills_text, body_style))
        
        return story
    
    def _build_creative_template(self, profile_data):
        """Build creative template resume - Colorful and modern"""
        story = []
        styles = getSampleStyleSheet()
        
        # Creative styles - vibrant colors
        name_style = ParagraphStyle(
            'NameStyle',
            parent=styles['Heading1'],
            fontSize=32,
            textColor=colors.HexColor('#6366F1'),
            spaceAfter=8,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        headline_style = ParagraphStyle(
            'HeadlineStyle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#8B5CF6'),
            spaceAfter=12,
            alignment=TA_LEFT,
            fontName='Helvetica-Oblique'
        )
        
        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#EC4899'),
            spaceAfter=10,
            spaceBefore=14,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#374151'),
            spaceAfter=6,
            fontName='Helvetica'
        )
        
        contact_style = ParagraphStyle(
            'ContactStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=10,
            alignment=TA_LEFT
        )
        
        # Build content
        story.append(Paragraph(profile_data.get('name', 'Name Not Available'), name_style))
        
        if profile_data.get('headline'):
            story.append(Paragraph(profile_data['headline'], headline_style))
        
        contact = profile_data.get('contact', {})
        contact_info = []
        if contact.get('email'):
            contact_info.append(f"✉️ {contact['email']}")
        if contact.get('phone'):
            contact_info.append(f"📱 {contact['phone']}")
        if contact.get('location'):
            contact_info.append(f"📍 {contact['location']}")
        
        if contact_info:
            story.append(Paragraph(' • '.join(contact_info), contact_style))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Summary
        if profile_data.get('about'):
            story.append(Paragraph('💡 About Me', section_title_style))
            story.append(Paragraph(profile_data['about'], body_style))
            story.append(Spacer(1, 0.12*inch))
        
        # Experience
        experiences = profile_data.get('experience', [])
        if experiences:
            story.append(Paragraph('💼 Experience', section_title_style))
            for exp in experiences:
                title_text = f"<b>{exp.get('title', '')}</b> @ {exp.get('company', '')}"
                story.append(Paragraph(title_text, body_style))
                
                if exp.get('duration'):
                    duration_text = f"<i>⏰ {exp['duration']}</i>"
                    story.append(Paragraph(duration_text, contact_style))
                
                if exp.get('description'):
                    # Format description with bullet points if it's long
                    desc = exp['description']
                    if len(desc) > 150:
                        # Split into sentences and create bullet points
                        sentences = [s.strip() for s in desc.replace('. ', '.|').split('|') if s.strip()]
                        for sentence in sentences[:5]:  # Limit to 5 bullets
                            if sentence:
                                bullet_style = ParagraphStyle('Bullet', parent=body_style, leftIndent=15, firstLineIndent=-10)
                                story.append(Paragraph(f"🔹 {sentence}", bullet_style))
                    else:
                        story.append(Paragraph(exp['description'], body_style))
                
                story.append(Spacer(1, 0.1*inch))
        
        # Education
        education = profile_data.get('education', [])
        if education:
            story.append(Paragraph('🎓 Education', section_title_style))
            for edu in education:
                school_text = f"<b>{edu.get('school', '')}</b>"
                story.append(Paragraph(school_text, body_style))
                
                degree_parts = []
                if edu.get('degree'):
                    degree_parts.append(edu['degree'])
                if edu.get('field'):
                    degree_parts.append(edu['field'])
                
                if degree_parts:
                    degree_text = ' - '.join(degree_parts)
                    story.append(Paragraph(degree_text, body_style))
                
                if edu.get('dates'):
                    dates_text = f"<i>{edu['dates']}</i>"
                    story.append(Paragraph(dates_text, contact_style))
                
                story.append(Spacer(1, 0.08*inch))
        
        # Skills
        skills = profile_data.get('skills', [])
        if skills:
            story.append(Paragraph('⚡ Skills', section_title_style))
            skills_text = ' 🔹 '.join(skills)
            story.append(Paragraph(skills_text, body_style))
        
        return story
