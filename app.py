from flask import Flask, render_template, request, send_file, jsonify
import os
from resume_generator import ResumeGenerator
from linkedin_parser import LinkedInParser
from cover_letter_generator import CoverLetterGenerator
from ats_analyzer import ATSAnalyzer
from skill_gap_analyzer import SkillGapAnalyzer
from linkedin_url_scraper import LinkedInURLScraper
from career_path_advisor import CareerPathAdvisor
from interview_question_generator import InterviewQuestionGenerator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'generated_resumes'

# Create the folder for generated resumes if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/')
def landing():
    """Render the landing page"""
    return render_template('landing.html')


@app.route('/dashboard')
def dashboard():
    """Render the resume generator dashboard"""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_resume():
    """Generate resume from pasted LinkedIn text"""
    try:
        data = request.get_json()
        linkedin_text = data.get('linkedin_text', '')
        template = data.get('template', 'modern')  # Get template selection
        
        if not linkedin_text or len(linkedin_text.strip()) < 50:
            return jsonify({'error': 'Please paste your LinkedIn profile content (Ctrl+A on your profile page, then Ctrl+C to copy)'}), 400
        
        # Parse the pasted LinkedIn content
        parser = LinkedInParser()
        profile_data = parser.parse_linkedin_text(linkedin_text)
        
        if not profile_data:
            return jsonify({'error': 'Failed to extract data from the pasted content. Make sure you copied from your LinkedIn profile page.'}), 500
        
        # Generate resume PDF with selected template
        generator = ResumeGenerator()
        pdf_path = generator.create_resume(profile_data, template=template)
        
        return jsonify({
            'success': True,
            'pdf_path': pdf_path,
            'profile_data': profile_data,  # Include profile data for cover letter generation
            'message': f'Resume generated successfully with {template.capitalize()} template!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    """Generate cover letter from profile data and job description"""
    try:
        data = request.get_json()
        profile_data = data.get('profile_data', {})
        job_description = data.get('job_description', '')
        
        if not profile_data:
            return jsonify({'error': 'Profile data is required'}), 400
        
        if not job_description or len(job_description.strip()) < 50:
            return jsonify({'error': 'Please provide a detailed job description (minimum 50 characters)'}), 400
        
        # Generate cover letter
        cl_generator = CoverLetterGenerator()
        pdf_path = cl_generator.create_cover_letter_pdf(profile_data, job_description)
        
        return jsonify({
            'success': True,
            'pdf_path': pdf_path,
            'message': 'Cover letter generated successfully!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_resume(filename):
    """Download the generated resume"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return send_file(file_path, as_attachment=True, download_name='resume.pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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


@app.route('/analyze-skill-gap', methods=['POST'])
def analyze_skill_gap():
    """Analyze skill gaps between profile and job requirements"""
    try:
        data = request.get_json()
        profile_data = data.get('profile_data', {})
        job_description = data.get('job_description', '')
        
        if not profile_data:
            return jsonify({'error': 'Profile data is required'}), 400
        
        if not job_description or len(job_description.strip()) < 50:
            return jsonify({'error': 'Please provide a detailed job description for skill gap analysis'}), 400
        
        # Analyze skill gaps
        analyzer = SkillGapAnalyzer()
        gap_analysis = analyzer.analyze_skill_gap(profile_data, job_description)
        
        return jsonify({
            'success': True,
            'analysis': gap_analysis['analysis'],
            'method': gap_analysis.get('method', 'basic'),
            'message': 'Skill gap analysis completed!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/scrape-linkedin-url', methods=['POST'])
def scrape_linkedin_url():
    """Scrape LinkedIn profile from URL"""
    try:
        data = request.get_json()
        profile_url = data.get('profile_url', '')
        email = data.get('email', None)  # Optional: user can provide their own credentials
        password = data.get('password', None)
        
        if not profile_url or 'linkedin.com/in/' not in profile_url:
            return jsonify({'error': 'Please provide a valid LinkedIn profile URL (e.g., https://www.linkedin.com/in/username/)'}), 400
        
        # Initialize scraper
        scraper = LinkedInURLScraper()
        
        # Scrape profile
        print(f"🔍 Starting scrape for: {profile_url}")
        profile_data = scraper.scrape_profile(profile_url, login_required=True, email=email, password=password)
        
        # Close browser
        scraper.close()
        
        if not profile_data:
            return jsonify({'error': 'Failed to scrape profile. Make sure the URL is public or you have valid LinkedIn credentials.'}), 500
        
        return jsonify({
            'success': True,
            'profile_data': profile_data,
            'message': 'LinkedIn profile scraped successfully!'
        })
        
    except Exception as e:
        return jsonify({'error': f'Scraping failed: {str(e)}'}), 500


@app.route('/analyze-career-path', methods=['POST'])
def analyze_career_path():
    """Generate career path recommendations"""
    try:
        data = request.get_json()
        profile_data = data.get('profile_data')
        target_role = data.get('target_role', None)
        years_ahead = data.get('years_ahead', 5)
        
        if not profile_data:
            return jsonify({'error': 'No profile data provided'}), 400
        
        # Initialize career advisor
        advisor = CareerPathAdvisor()
        
        # Analyze career path
        result = advisor.analyze_career_path(profile_data, target_role, years_ahead)
        
        if result['success']:
            return jsonify({
                'success': True,
                'analysis': result['analysis'],
                'method': result.get('method', 'ai')
            })
        else:
            return jsonify({'error': 'Career path analysis failed'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Career analysis failed: {str(e)}'}), 500


@app.route('/generate-interview-questions', methods=['POST'])
def generate_interview_questions():
    """Generate personalized interview questions"""
    try:
        data = request.get_json()
        profile_data = data.get('profile_data')
        job_description = data.get('job_description', None)
        question_count = data.get('question_count', 25)
        
        if not profile_data:
            return jsonify({'error': 'Profile data is required'}), 400
        
        # Validate question count
        try:
            question_count = int(question_count)
            if question_count < 10 or question_count > 50:
                question_count = 25
        except:
            question_count = 25
        
        # Generate interview questions
        generator = InterviewQuestionGenerator()
        result = generator.generate_questions(profile_data, job_description, question_count)
        
        if result['success']:
            return jsonify({
                'success': True,
                'questions': result['questions'],
                'total_questions': result['total_questions'],
                'method': result.get('method', 'ai_powered'),
                'personalization_level': result.get('personalization_level', 'high'),
                'message': f'Generated {result["total_questions"]} personalized interview questions!'
            })
        else:
            return jsonify({'error': 'Question generation failed'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Interview question generation failed: {str(e)}'}), 500


# Vercel serverless function handler
app_handler = app

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
