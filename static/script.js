// Store profile data for cover letter generation
let profileData = null;

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const themeSlider = document.querySelector('.theme-toggle-slider');
const htmlElement = document.documentElement;

// Check for saved theme preference or default to 'light' mode
const currentTheme = localStorage.getItem('theme') || 'light';
htmlElement.setAttribute('data-theme', currentTheme);
updateThemeIcon(currentTheme);

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const currentTheme = htmlElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
}

function updateThemeIcon(theme) {
    if (themeSlider) {
        themeSlider.textContent = theme === 'light' ? '🌙' : '☀️';
    }
}

// Update step indicators
function updateStep(stepNumber) {
    document.querySelectorAll('.step').forEach((step, index) => {
        if (index < stepNumber) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    });
}

document.getElementById('resumeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const selectedTemplate = document.querySelector('input[name="template"]:checked').value;
    const selectedMethod = document.querySelector('input[name="input_method"]:checked').value;
    const generateBtn = document.getElementById('generateBtn');
    const btnText = generateBtn.querySelector('.btn-text');
    const spinner = generateBtn.querySelector('.spinner');
    const messageDiv = document.getElementById('message');
    const downloadSection = document.getElementById('downloadSection');
    const coverLetterSection = document.getElementById('coverLetterSection');
    
    // Reset UI
    messageDiv.style.display = 'none';
    downloadSection.style.display = 'none';
    coverLetterSection.style.display = 'none';
    
    // Show loading state
    generateBtn.disabled = true;
    btnText.textContent = 'Generating...';
    spinner.style.display = 'inline-block';
    
    try {
        let linkedinText = '';
        
        // Handle different input methods
        if (selectedMethod === 'paste') {
            linkedinText = document.getElementById('linkedin_text').value;
            if (!linkedinText || linkedinText.trim().length < 50) {
                throw new Error('Please paste your LinkedIn profile content');
            }
        } else if (selectedMethod === 'manual') {
            // Handle manual entry - we'll create the profile data directly
            throw new Error('Manual entry not yet implemented - coming soon!');
        }
        
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                linkedin_text: linkedinText,
                template: selectedTemplate
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store profile data for cover letter generation
            profileData = data.profile_data;
            
            // Update step indicator
            updateStep(2);
            
            // Show success message
            messageDiv.textContent = data.message;
            messageDiv.className = 'message success';
            messageDiv.style.display = 'flex';
            
            // Fetch ATS score
            fetchATSScore(profileData);
            
            // Show PDF preview
            const resumeViewer = document.getElementById('resumeViewer');
            const previewContainer = resumeViewer.closest('.pdf-preview-container');
            resumeViewer.src = `/download/${data.pdf_path}#toolbar=0`;
            
            // Wait for iframe to load before showing
            resumeViewer.onload = function() {
                previewContainer.classList.add('show');
            };
            
            // Show download section
            const downloadBtn = document.getElementById('downloadBtn');
            downloadBtn.href = `/download/${data.pdf_path}`;
            downloadSection.style.display = 'block';
            
            // Smooth scroll to result
            downloadSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            throw new Error(data.error || 'Failed to generate resume');
        }
    } catch (error) {
        messageDiv.textContent = `Error: ${error.message}`;
        messageDiv.className = 'message error';
        messageDiv.style.display = 'flex';
    } finally {
        // Reset button state
        generateBtn.disabled = false;
        btnText.textContent = 'Generate Resume';
        spinner.style.display = 'none';
    }
});

// Show cover letter form
document.getElementById('showCoverLetterBtn').addEventListener('click', () => {
    const coverLetterSection = document.getElementById('coverLetterSection');
    updateStep(3);
    coverLetterSection.style.display = 'block';
    coverLetterSection.scrollIntoView({ behavior: 'smooth' });
});

// Generate cover letter
document.getElementById('coverLetterForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!profileData) {
        alert('Please generate a resume first!');
        return;
    }
    
    const jobDescription = document.getElementById('job_description').value;
    const generateBtn = document.getElementById('generateCoverLetterBtn');
    const btnText = generateBtn.querySelector('.btn-text');
    const spinner = generateBtn.querySelector('.spinner');
    const messageDiv = document.getElementById('coverLetterMessage');
    const downloadSection = document.getElementById('downloadCoverLetterSection');
    
    // Reset UI
    messageDiv.style.display = 'none';
    downloadSection.style.display = 'none';
    
    // Show loading state
    generateBtn.disabled = true;
    btnText.textContent = 'Generating...';
    spinner.style.display = 'inline-block';
    
    try {
        const response = await fetch('/generate-cover-letter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                profile_data: profileData,
                job_description: jobDescription 
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show success message
            messageDiv.textContent = data.message;
            messageDiv.className = 'message success';
            messageDiv.style.display = 'flex';
            
            // Show PDF preview
            const coverLetterViewer = document.getElementById('coverLetterViewer');
            const previewContainer = coverLetterViewer.closest('.pdf-preview-container');
            coverLetterViewer.src = `/download/${data.pdf_path}#toolbar=0`;
            
            // Wait for iframe to load before showing
            coverLetterViewer.onload = function() {
                previewContainer.classList.add('show');
            };
            
            // Show download section
            const downloadBtn = document.getElementById('downloadCoverLetterBtn');
            downloadBtn.href = `/download/${data.pdf_path}`;
            downloadSection.style.display = 'block';
            
            // Smooth scroll to result
            downloadSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            throw new Error(data.error || 'Failed to generate cover letter');
        }
    } catch (error) {
        messageDiv.textContent = `Error: ${error.message}`;
        messageDiv.className = 'message error';
        messageDiv.style.display = 'flex';
    } finally {
        // Reset button state
        generateBtn.disabled = false;
        btnText.textContent = 'Generate Cover Letter';
        spinner.style.display = 'none';
    }
});

// ATS Score Functions
async function fetchATSScore(profileData, jobDescription = null) {
    const loadingState = document.getElementById('atsLoadingState');
    const scoreContent = document.getElementById('atsScoreContent');
    const atsContainer = document.getElementById('atsScoreContainer');
    
    // Show container and loading state
    atsContainer.style.display = 'block';
    loadingState.style.display = 'block';
    scoreContent.style.display = 'none';
    
    try {
        const response = await fetch('/analyze-ats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                profile_data: profileData,
                job_description: jobDescription 
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayATSScore(data.analysis);
        } else {
            throw new Error(data.error || 'Failed to analyze ATS score');
        }
    } catch (error) {
        console.error('ATS Analysis Error:', error);
        loadingState.innerHTML = `<p style="color: var(--text-gray);">Unable to analyze ATS score. ${error.message}</p>`;
    }
}

function displayATSScore(analysis) {
    const loadingState = document.getElementById('atsLoadingState');
    const scoreContent = document.getElementById('atsScoreContent');
    
    // Hide loading, show content
    loadingState.style.display = 'none';
    scoreContent.style.display = 'block';
    
    // Animate overall score
    const scoreValue = document.getElementById('atsScoreValue');
    const scoreRing = document.getElementById('scoreRingProgress');
    const rating = document.getElementById('atsRating');
    
    animateScore(scoreValue, 0, analysis.overall_score, 1500);
    
    // Calculate stroke-dashoffset for circle (circumference = 2 * π * r = 314)
    const circumference = 314;
    const offset = circumference - (analysis.overall_score / 100) * circumference;
    scoreRing.style.strokeDashoffset = offset;
    
    // Set score color based on value
    if (analysis.overall_score >= 80) {
        scoreRing.style.stroke = '#10B981'; // Green
    } else if (analysis.overall_score >= 60) {
        scoreRing.style.stroke = '#3B82F6'; // Blue
    } else if (analysis.overall_score >= 40) {
        scoreRing.style.stroke = '#FB923C'; // Orange
    } else {
        scoreRing.style.stroke = '#EF4444'; // Red
    }
    
    // Set rating
    const ratingText = analysis.ats_friendly_rating || 'Good';
    rating.textContent = ratingText;
    rating.className = 'ats-rating ' + ratingText.toLowerCase();
    
    // Display category scores
    const categories = ['formatting', 'keywords', 'experience', 'skills', 'education'];
    categories.forEach(category => {
        const score = analysis.category_scores[category] || 0;
        const bar = document.getElementById(`${category}Bar`);
        const scoreEl = document.getElementById(`${category}Score`);
        
        setTimeout(() => {
            bar.style.width = score + '%';
            scoreEl.textContent = score;
        }, 300);
    });
    
    // Display strengths
    const strengthsList = document.getElementById('atsStrengthsList');
    strengthsList.innerHTML = '';
    (analysis.strengths || []).forEach(strength => {
        const li = document.createElement('li');
        li.textContent = strength;
        strengthsList.appendChild(li);
    });
    
    // Display improvements
    const improvementsList = document.getElementById('atsImprovementsList');
    improvementsList.innerHTML = '';
    (analysis.improvements || []).forEach(improvement => {
        const li = document.createElement('li');
        li.textContent = improvement;
        improvementsList.appendChild(li);
    });
}

function animateScore(element, start, end, duration) {
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function (ease-out)
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(start + (end - start) * easeOut);
        
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Refresh ATS Score button
document.getElementById('refreshAtsBtn')?.addEventListener('click', () => {
    if (profileData) {
        fetchATSScore(profileData);
    }
});

// Show skill gap form
document.getElementById('showSkillGapBtn')?.addEventListener('click', () => {
    const skillGapSection = document.getElementById('skillGapSection');
    skillGapSection.style.display = 'block';
    skillGapSection.scrollIntoView({ behavior: 'smooth' });
});

// Skill Gap Analysis
document.getElementById('skillGapForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!profileData) {
        alert('Please generate a resume first!');
        return;
    }
    
    const jobDescription = document.getElementById('skill_gap_job_description').value;
    const generateBtn = document.getElementById('analyzeSkillGapBtn');
    const btnText = generateBtn.querySelector('.btn-text');
    const spinner = generateBtn.querySelector('.spinner');
    const messageDiv = document.getElementById('skillGapMessage');
    const resultsSection = document.getElementById('skillGapResults');
    
    // Reset UI
    messageDiv.style.display = 'none';
    resultsSection.style.display = 'none';
    
    // Show loading state
    generateBtn.disabled = true;
    btnText.textContent = 'Analyzing...';
    spinner.style.display = 'inline-block';
    
    try {
        const response = await fetch('/analyze-skill-gap', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                profile_data: profileData,
                job_description: jobDescription 
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displaySkillGapResults(data.analysis);
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            throw new Error(data.error || 'Failed to analyze skill gap');
        }
    } catch (error) {
        messageDiv.textContent = `Error: ${error.message}`;
        messageDiv.className = 'message error';
        messageDiv.style.display = 'flex';
    } finally {
        generateBtn.disabled = false;
        btnText.textContent = 'Analyze Skill Gap';
        spinner.style.display = 'none';
    }
});

function displaySkillGapResults(analysis) {
    // Display score with animation
    const scoreElement = document.getElementById('skillGapScore');
    const ringProgress = document.getElementById('skillRingProgress');
    const score = analysis.skill_gap_score || 0;
    
    animateScore(scoreElement, 0, score, 1500);
    
    // Animate circular progress
    const circumference = 2 * Math.PI * 50;
    const offset = circumference - (score / 100) * circumference;
    ringProgress.style.strokeDashoffset = offset;
    
    // Display summary
    const summaryEl = document.getElementById('skillGapSummary');
    summaryEl.textContent = analysis.summary || 'Analysis complete';
    
    // Display matching skills
    const matchingSkillsEl = document.getElementById('matchingSkills');
    matchingSkillsEl.innerHTML = '';
    (analysis.matching_skills || []).forEach(skill => {
        const tag = document.createElement('span');
        tag.className = 'skill-tag';
        tag.textContent = skill;
        matchingSkillsEl.appendChild(tag);
    });
    
    // Display missing skills
    const missingSkillsEl = document.getElementById('missingSkills');
    missingSkillsEl.innerHTML = '';
    (analysis.missing_skills || []).forEach(skill => {
        const tag = document.createElement('span');
        tag.className = 'skill-tag';
        tag.textContent = skill;
        missingSkillsEl.appendChild(tag);
    });
    
    // Display partial skills
    const partialSkillsEl = document.getElementById('partialSkills');
    partialSkillsEl.innerHTML = '';
    (analysis.partially_matched_skills || []).forEach(skill => {
        const tag = document.createElement('span');
        tag.className = 'skill-tag';
        tag.textContent = skill;
        partialSkillsEl.appendChild(tag);
    });
    
    // Display recommendations
    const recommendationsEl = document.getElementById('recommendationsList');
    recommendationsEl.innerHTML = '';
    (analysis.recommendations || []).forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recommendationsEl.appendChild(li);
    });
    
    // Display learning resources
    if (analysis.learning_resources && analysis.learning_resources.length > 0) {
        const resourcesSection = document.getElementById('learningResourcesSection');
        const resourcesList = document.getElementById('learningResourcesList');
        resourcesList.innerHTML = '';
        
        analysis.learning_resources.forEach(resource => {
            const card = document.createElement('div');
            card.className = 'resource-card';
            card.innerHTML = `
                <div class="resource-header">
                    <h5>${resource.skill}</h5>
                    <span class="priority-badge priority-${resource.priority}">${resource.priority}</span>
                </div>
                <ul class="resource-list">
                    ${resource.resources.map(r => `<li>${r}</li>`).join('')}
                </ul>
            `;
            resourcesList.appendChild(card);
        });
        
        resourcesSection.style.display = 'block';
    }
    
    // Display experience gap
    if (analysis.experience_gap) {
        const expGap = analysis.experience_gap;
        const expGapContent = document.getElementById('experienceGapContent');
        expGapContent.innerHTML = `
            <p><strong>Required:</strong> ${expGap.years_required} years</p>
            <p><strong>You have:</strong> ${expGap.years_you_have} years</p>
            <p><strong>Gap:</strong> ${expGap.gap}</p>
            <p class="advice"><em>${expGap.advice}</em></p>
        `;
    }
}


// Input Method Radio Button Handling
document.addEventListener('DOMContentLoaded', () => {
    const methodRadios = document.querySelectorAll('input[name="input_method"]');
    const pasteFields = document.getElementById('pasteFields');
    const manualFields = document.getElementById('manualFields');
    
    // Initialize: Show only paste fields by default
    if (pasteFields) pasteFields.style.display = 'block';
    if (manualFields) manualFields.style.display = 'none';
    
    // Add event listeners to radio buttons
    methodRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            const selectedMethod = radio.value;
            
            // Hide all field containers
            if (pasteFields) pasteFields.style.display = 'none';
            if (manualFields) manualFields.style.display = 'none';
            
            // Show selected field container
            if (selectedMethod === 'paste' && pasteFields) {
                pasteFields.style.display = 'block';
            } else if (selectedMethod === 'manual' && manualFields) {
                manualFields.style.display = 'block';
            }
        });
    });
    
    // Add Experience Entry
    const addExperienceBtn = document.getElementById('addExperienceBtn');
    const experienceContainer = document.getElementById('experienceContainer');
    let experienceCount = 1;
    
    if (addExperienceBtn) {
        addExperienceBtn.addEventListener('click', () => {
            experienceCount++;
            const newEntry = document.createElement('div');
            newEntry.className = 'experience-entry';
            newEntry.innerHTML = `
                <button type="button" class="btn-remove-entry" onclick="removeEntry(this)">×</button>
                <div class="form-group">
                    <label for="exp_title_${experienceCount}">Job Title *</label>
                    <input type="text" id="exp_title_${experienceCount}" name="experience[][title]" placeholder="e.g., Senior Software Engineer" required>
                </div>
                <div class="form-group">
                    <label for="exp_company_${experienceCount}">Company *</label>
                    <input type="text" id="exp_company_${experienceCount}" name="experience[][company]" placeholder="e.g., Tech Corp" required>
                </div>
                <div class="form-group">
                    <label for="exp_duration_${experienceCount}">Duration *</label>
                    <input type="text" id="exp_duration_${experienceCount}" name="experience[][duration]" placeholder="e.g., Jan 2020 - Present" required>
                </div>
                <div class="form-group">
                    <label for="exp_description_${experienceCount}">Description</label>
                    <textarea id="exp_description_${experienceCount}" name="experience[][description]" rows="3" placeholder="Describe your key responsibilities and achievements..."></textarea>
                </div>
            `;
            experienceContainer.appendChild(newEntry);
        });
    }
    
    // Add Education Entry
    const addEducationBtn = document.getElementById('addEducationBtn');
    const educationContainer = document.getElementById('educationContainer');
    let educationCount = 1;
    
    if (addEducationBtn) {
        addEducationBtn.addEventListener('click', () => {
            educationCount++;
            const newEntry = document.createElement('div');
            newEntry.className = 'education-entry';
            newEntry.innerHTML = `
                <button type="button" class="btn-remove-entry" onclick="removeEntry(this)">×</button>
                <div class="form-group">
                    <label for="edu_degree_${educationCount}">Degree *</label>
                    <input type="text" id="edu_degree_${educationCount}" name="education[][degree]" placeholder="e.g., B.S. Computer Science" required>
                </div>
                <div class="form-group">
                    <label for="edu_institution_${educationCount}">Institution *</label>
                    <input type="text" id="edu_institution_${educationCount}" name="education[][institution]" placeholder="e.g., University of California" required>
                </div>
                <div class="form-group">
                    <label for="edu_year_${educationCount}">Year *</label>
                    <input type="text" id="edu_year_${educationCount}" name="education[][year]" placeholder="e.g., 2016 - 2020" required>
                </div>
            `;
            educationContainer.appendChild(newEntry);
        });
    }
});

// Remove entry function (for dynamic experience/education fields)
function removeEntry(button) {
    const entry = button.closest('.experience-entry, .education-entry');
    if (entry) {
        entry.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => entry.remove(), 300);
    }
}

// Handle LinkedIn URL scraping
async function scrapeLinkedInURL() {
    const urlInput = document.getElementById('linkedin_url');
    const linkedinURL = urlInput.value.trim();
    const messageDiv = document.getElementById('message');
    
    // Show loading state
    messageDiv.textContent = 'Scraping LinkedIn profile... This may take 30-60 seconds';
    messageDiv.className = 'message info';
    messageDiv.style.display = 'flex';
    
    try {
        const response = await fetch('/scrape-linkedin-url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                linkedin_url: linkedinURL 
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store scraped data in the paste field and switch to paste method
            const linkedinTextArea = document.getElementById('linkedin_text');
            linkedinTextArea.value = data.profile_text;
            
            // Show success message
            messageDiv.textContent = 'Profile scraped successfully! Ready to generate resume.';
            messageDiv.className = 'message success';
            messageDiv.style.display = 'flex';
            
            // Auto-switch to paste method to show the data
            document.getElementById('method_paste').checked = true;
            document.getElementById('pasteFields').style.display = 'block';
            document.getElementById('urlFields').style.display = 'none';
            
            // Scroll to the paste section
            linkedinTextArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            throw new Error(data.error || 'Failed to scrape LinkedIn profile');
        }
    } catch (error) {
        messageDiv.textContent = `Error: ${error.message}`;
        messageDiv.className = 'message error';
        messageDiv.style.display = 'flex';
    }
}

// Show career path form
document.getElementById('showCareerPathBtn')?.addEventListener('click', () => {
    const careerPathSection = document.getElementById('careerPathSection');
    careerPathSection.style.display = 'block';
    careerPathSection.scrollIntoView({ behavior: 'smooth' });
});

// Show interview questions form
document.getElementById('showInterviewQuestionsBtn')?.addEventListener('click', () => {
    const interviewSection = document.getElementById('interviewQuestionsSection');
    interviewSection.style.display = 'block';
    interviewSection.scrollIntoView({ behavior: 'smooth' });
});

// Career Path Analysis
document.getElementById('careerPathForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!profileData) {
        alert('Please generate a resume first!');
        return;
    }
    
    const targetRole = document.getElementById('target_role').value;
    const yearsAhead = parseInt(document.getElementById('years_ahead').value);
    const analyzeBtn = document.getElementById('analyzeCareerPathBtn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const spinner = analyzeBtn.querySelector('.spinner');
    const messageDiv = document.getElementById('careerPathMessage');
    const resultsSection = document.getElementById('careerPathResults');
    
    // Reset UI
    messageDiv.style.display = 'none';
    resultsSection.style.display = 'none';
    
    // Show loading state
    analyzeBtn.disabled = true;
    btnText.textContent = 'Analyzing...';
    spinner.style.display = 'inline-block';
    
    try {
        const response = await fetch('/analyze-career-path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                profile_data: profileData,
                target_role: targetRole || null,
                years_ahead: yearsAhead
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayCareerPathResults(data.analysis);
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            throw new Error(data.error || 'Failed to analyze career path');
        }
    } catch (error) {
        messageDiv.textContent = `Error: ${error.message}`;
        messageDiv.className = 'message error';
        messageDiv.style.display = 'flex';
    } finally {
        analyzeBtn.disabled = false;
        btnText.textContent = 'Analyze Career Path';
        spinner.style.display = 'none';
    }
});

function displayCareerPathResults(analysis) {
    // Display current level
    const currentLevelEl = document.getElementById('currentLevel');
    currentLevelEl.textContent = analysis.current_level || 'Not determined';
    
    // Display next role suggestions
    const nextRolesList = document.getElementById('nextRolesList');
    nextRolesList.innerHTML = '';
    (analysis.next_role_suggestions || []).forEach(role => {
        const card = document.createElement('div');
        card.className = 'next-role-card';
        card.innerHTML = `
            <h5>${role.title}</h5>
            <div class="role-meta">
                <span class="timeframe">⏱️ ${role.timeframe}</span>
                <span class="difficulty difficulty-${role.difficulty.toLowerCase()}">${role.difficulty}</span>
            </div>
            <div class="readiness-score">
                <div class="score-label">Readiness: ${role.readiness_score}%</div>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${role.readiness_score}%"></div>
                </div>
            </div>
            <p class="rationale">${role.rationale}</p>
            <div class="required-skills">
                <strong>Required Skills:</strong>
                ${role.required_skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
            </div>
        `;
        nextRolesList.appendChild(card);
    });
    
    // Display skill roadmap
    const roadmap = analysis.skill_roadmap || {};
    displaySkillRoadmapPhase('skillRoadmapImmediate', roadmap.immediate_focus || []);
    displaySkillRoadmapPhase('skillRoadmapShort', roadmap.short_term || []);
    displaySkillRoadmapPhase('skillRoadmapLong', roadmap.long_term || []);
    
    // Display industry trends
    const trendsEl = document.getElementById('industryTrends');
    const trends = analysis.industry_trends || {};
    trendsEl.innerHTML = `
        <div class="trend-card">
            <h5>🔥 Emerging Skills</h5>
            <div class="skill-list">
                ${(trends.emerging_skills || []).map(skill => `<span class="skill-tag emerging">${skill}</span>`).join('')}
            </div>
        </div>
        <div class="trend-card">
            <h5>📉 Declining Skills</h5>
            <div class="skill-list">
                ${(trends.declining_skills || []).map(skill => `<span class="skill-tag declining">${skill}</span>`).join('')}
            </div>
        </div>
        <div class="trend-card">
            <h5>💼 Hot Areas</h5>
            <div class="skill-list">
                ${(trends.hot_areas || []).map(area => `<span class="skill-tag hot">${area}</span>`).join('')}
            </div>
        </div>
        <div class="trend-card">
            <h5>📊 Market Insights</h5>
            <p><strong>Demand:</strong> ${trends.market_demand || 'N/A'}</p>
            <p><strong>Salary Trend:</strong> ${trends.salary_trends || 'N/A'}</p>
            <p class="recommendations">${trends.recommendations || ''}</p>
        </div>
    `;
    
    // Display career timeline
    const timelineEl = document.getElementById('careerTimeline');
    const timeline = analysis.career_timeline || {};
    timelineEl.innerHTML = '';
    Object.keys(timeline).sort().forEach(year => {
        const yearData = timeline[year];
        const yearNum = year.replace('year_', '');
        const timelineItem = document.createElement('div');
        timelineItem.className = 'timeline-item';
        timelineItem.innerHTML = `
            <div class="timeline-marker">${yearNum}</div>
            <div class="timeline-content">
                <h5>Year ${yearNum}: ${yearData.target_position}</h5>
                <p><strong>Focus:</strong> ${yearData.focus}</p>
                <div class="milestones">
                    <strong>Key Milestones:</strong>
                    <ul>
                        ${(yearData.key_milestones || []).map(m => `<li>${m}</li>`).join('')}
                    </ul>
                </div>
                <div class="timeline-skills">
                    <strong>Skills to Develop:</strong>
                    ${(yearData.skills_to_develop || []).map(s => `<span class="skill-tag">${s}</span>`).join('')}
                </div>
                ${yearData.expected_salary_range ? `<p class="salary-range">💰 ${yearData.expected_salary_range}</p>` : ''}
            </div>
        `;
        timelineEl.appendChild(timelineItem);
    });
    
    // Display alternative paths
    const altPathsEl = document.getElementById('alternativePaths');
    altPathsEl.innerHTML = '';
    (analysis.alternative_paths || []).forEach(path => {
        const pathCard = document.createElement('div');
        pathCard.className = 'alternative-path-card';
        pathCard.innerHTML = `
            <h5>${path.path}</h5>
            <p>${path.description}</p>
            <div class="path-difficulty">Difficulty: <span class="difficulty-badge">${path.transition_difficulty}</span></div>
            <div class="pros-cons">
                <div class="pros">
                    <strong>✅ Pros:</strong>
                    <ul>${path.pros.map(p => `<li>${p}</li>`).join('')}</ul>
                </div>
                <div class="cons">
                    <strong>⚠️ Cons:</strong>
                    <ul>${path.cons.map(c => `<li>${c}</li>`).join('')}</ul>
                </div>
            </div>
        `;
        altPathsEl.appendChild(pathCard);
    });
    
    // Display certifications
    const certsEl = document.getElementById('certificationsList');
    certsEl.innerHTML = '';
    (analysis.certifications || []).forEach(cert => {
        const certCard = document.createElement('div');
        certCard.className = 'certification-card';
        certCard.innerHTML = `
            <h5>${cert.name}</h5>
            <p><strong>Provider:</strong> ${cert.provider}</p>
            <div class="cert-meta">
                <span class="cert-value value-${cert.value.toLowerCase()}">${cert.value} Value</span>
                <span class="cert-timeframe">📅 ${cert.timeframe}</span>
            </div>
            <p><strong>Cost:</strong> ${cert.cost_estimate}</p>
            <p class="roi">${cert.roi}</p>
        `;
        certsEl.appendChild(certCard);
    });
    
    // Display networking strategy
    const networkingEl = document.getElementById('networkingStrategy');
    const networking = analysis.networking_strategy || {};
    networkingEl.innerHTML = `
        <div class="networking-item">
            <h5>🎯 Target Connections</h5>
            <p>${networking.target_connections || 'N/A'}</p>
        </div>
        <div class="networking-item">
            <h5>💻 Platforms</h5>
            <div class="platform-list">
                ${(networking.platforms || []).map(p => `<span class="platform-tag">${p}</span>`).join('')}
            </div>
        </div>
        <div class="networking-item">
            <h5>🎪 Events & Conferences</h5>
            <p>${networking.events || 'N/A'}</p>
        </div>
        <div class="networking-item">
            <h5>👥 Communities</h5>
            <p>${networking.communities || 'N/A'}</p>
        </div>
    `;
}

function displaySkillRoadmapPhase(elementId, skills) {
    const container = document.getElementById(elementId);
    container.innerHTML = '';
    skills.forEach(skillData => {
        const skillCard = document.createElement('div');
        skillCard.className = 'skill-roadmap-card';
        skillCard.innerHTML = `
            <div class="skill-header">
                <h5>${skillData.skill}</h5>
                <span class="priority-badge priority-${skillData.priority?.toLowerCase().replace('/', '-')}">${skillData.priority}</span>
            </div>
            <p class="skill-reason">${skillData.reason}</p>
            <p class="skill-time">⏱️ ${skillData.estimated_time}</p>
            <div class="learning-resources">
                <strong>Resources:</strong>
                <ul>${skillData.learning_resources.map(r => `<li>${r}</li>`).join('')}</ul>
            </div>
        `;
        container.appendChild(skillCard);
    });
}

// Roadmap tabs functionality
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('roadmap-tab')) {
        // Remove active from all tabs and contents
        document.querySelectorAll('.roadmap-tab').forEach(tab => tab.classList.remove('active'));
        document.querySelectorAll('.roadmap-content').forEach(content => content.classList.remove('active'));
        
        // Add active to clicked tab
        e.target.classList.add('active');
        
        // Show corresponding content
        const phase = e.target.dataset.phase;
        const contentMap = {
            'immediate': 'skillRoadmapImmediate',
            'short': 'skillRoadmapShort',
            'long': 'skillRoadmapLong'
        };
        document.getElementById(contentMap[phase]).classList.add('active');
    }
});


// ==========================================
// INTERVIEW QUESTIONS GENERATOR
// ==========================================

// Handle interview questions form submission
document.getElementById('interviewQuestionsForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!profileData) {
        showInterviewMessage('Please generate a resume first to analyze your profile', 'error');
        return;
    }
    
    const jobDescription = document.getElementById('interview_job_description').value.trim();
    const questionCount = parseInt(document.getElementById('question_count').value);
    const generateBtn = document.getElementById('generateQuestionsBtn');
    const btnText = generateBtn.querySelector('.btn-text');
    const spinner = generateBtn.querySelector('.spinner');
    
    // Show loading state
    btnText.style.display = 'none';
    spinner.style.display = 'inline-block';
    generateBtn.disabled = true;
    
    showInterviewMessage('Generating personalized interview questions...', 'info');
    
    try {
        const response = await fetch('/generate-interview-questions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                profile_data: profileData,
                job_description: jobDescription || null,
                question_count: questionCount
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showInterviewMessage(data.message, 'success');
            displayInterviewQuestions(data);
            
            // Scroll to results
            setTimeout(() => {
                document.getElementById('interviewQuestionsResults').scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }, 300);
        } else {
            showInterviewMessage(data.error || 'Failed to generate interview questions', 'error');
        }
    } catch (error) {
        showInterviewMessage('Error generating questions: ' + error.message, 'error');
    } finally {
        // Reset button state
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
        generateBtn.disabled = false;
    }
});

function showInterviewMessage(message, type) {
    const messageDiv = document.getElementById('interviewMessage');
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
}

function displayInterviewQuestions(data) {
    const container = document.getElementById('interviewQuestionsResults');
    const questions = data.questions;
    
    let html = `
        <div class="interview-summary">
            <div class="summary-stat">
                <div class="stat-value">${data.total_questions}</div>
                <div class="stat-label">Total Questions</div>
            </div>
            <div class="summary-stat">
                <div class="stat-value">${data.personalization_level === 'high' ? '🎯' : '📝'}</div>
                <div class="stat-label">${data.personalization_level === 'high' ? 'Highly Personalized' : 'Template Based'}</div>
            </div>
            <div class="summary-stat">
                <div class="stat-value">${data.method === 'ai_powered' ? '🤖' : '📋'}</div>
                <div class="stat-label">${data.method === 'ai_powered' ? 'AI Generated' : 'Template'}</div>
            </div>
        </div>
    `;
    
    // Technical Questions
    if (questions.technical_questions && questions.technical_questions.length > 0) {
        html += generateQuestionCategory(
            '💻 Technical Questions', 
            questions.technical_questions,
            'Technical knowledge and problem-solving skills'
        );
    }
    
    // Behavioral Questions
    if (questions.behavioral_questions && questions.behavioral_questions.length > 0) {
        html += generateQuestionCategory(
            '🤝 Behavioral Questions', 
            questions.behavioral_questions,
            'Past experiences and soft skills'
        );
    }
    
    // Experience-Based Questions
    if (questions.experience_based_questions && questions.experience_based_questions.length > 0) {
        html += generateQuestionCategory(
            '💼 Experience-Based Questions', 
            questions.experience_based_questions,
            'Verify your resume claims'
        );
    }
    
    // Situational Questions
    if (questions.situational_questions && questions.situational_questions.length > 0) {
        html += generateQuestionCategory(
            '🎯 Situational Questions', 
            questions.situational_questions,
            'How you handle hypothetical scenarios'
        );
    }
    
    // Company Culture Questions
    if (questions.company_culture_questions && questions.company_culture_questions.length > 0) {
        html += generateQuestionCategory(
            '🏢 Company & Culture Fit', 
            questions.company_culture_questions,
            'Cultural alignment and motivations'
        );
    }
    
    // Weakness/Gap Questions
    if (questions.weakness_questions && questions.weakness_questions.length > 0) {
        html += generateQuestionCategory(
            '⚠️ Addressing Weaknesses & Gaps', 
            questions.weakness_questions,
            'Potential concerns from your resume'
        );
    }
    
    // Questions to Ask Interviewer
    if (questions.questions_to_ask_interviewer && questions.questions_to_ask_interviewer.length > 0) {
        html += generateAskInterviewerSection(questions.questions_to_ask_interviewer);
    }
    
    // Overall Strategy
    if (questions.overall_strategy) {
        html += generateOverallStrategy(questions.overall_strategy);
    }
    
    // Mock Interview Scorecard
    if (questions.mock_interview_scorecard) {
        html += generateMockScorecard(questions.mock_interview_scorecard);
    }
    
    container.innerHTML = html;
    container.style.display = 'block';
    
    // Add click handlers for expandable cards
    addQuestionCardHandlers();
}

function generateQuestionCategory(title, questions, description) {
    let html = `
        <div class="question-category">
            <div class="category-header">
                <div class="category-title">
                    ${title}
                    <span class="category-count">${questions.length}</span>
                </div>
            </div>
            <p style="color: var(--text-light); margin-bottom: 20px; font-style: italic;">${description}</p>
    `;
    
    questions.forEach((q, index) => {
        html += `
            <div class="question-card collapsed" data-question-id="${index}">
                <div class="question-header">
                    <div class="question-text">${index + 1}. ${q.question}</div>
                    <div class="question-badges">
                        ${q.difficulty ? `<span class="difficulty-badge ${q.difficulty.toLowerCase()}">${q.difficulty}</span>` : ''}
                        ${q.category ? `<span class="category-badge">${q.category}</span>` : ''}
                        <span class="expand-indicator">▼</span>
                    </div>
                </div>
                
                <div class="question-details">
                    ${q.why_asking ? `
                        <div class="question-section">
                            <div class="question-section-title">🎯 Why They're Asking This</div>
                            <div class="question-section-content">${q.why_asking}</div>
                        </div>
                    ` : ''}
                    
                    ${q.key_points && q.key_points.length > 0 ? `
                        <div class="question-section">
                            <div class="question-section-title">✅ Key Points to Cover</div>
                            <ul class="key-points-list">
                                ${q.key_points.map(point => `<li>${point}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${q.star_template ? generateStarTemplate(q.star_template) : ''}
                    
                    ${q.preparation_tip ? `
                        <div class="question-section">
                            <div class="question-section-title">💡 Preparation Tip</div>
                            <div class="question-section-content">${q.preparation_tip}</div>
                        </div>
                    ` : ''}
                    
                    ${q.good_answer_example ? `
                        <div class="question-section">
                            <div class="question-section-title">✨ Good Answer Approach</div>
                            <div class="question-section-content">${q.good_answer_example}</div>
                        </div>
                    ` : ''}
                    
                    ${q.good_approach ? `
                        <div class="question-section">
                            <div class="question-section-title">✨ Approach Framework</div>
                            <div class="question-section-content">${q.good_approach}</div>
                        </div>
                    ` : ''}
                    
                    ${q.red_flags && q.red_flags.length > 0 ? `
                        <div class="question-section">
                            <div class="question-section-title">🚫 Red Flags to Avoid</div>
                            <ul class="red-flags-list">
                                ${q.red_flags.map(flag => `<li>${flag}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${q.avoid && q.avoid.length > 0 ? `
                        <div class="question-section">
                            <div class="question-section-title">🚫 What to Avoid</div>
                            <ul class="red-flags-list">
                                ${q.avoid.map(item => `<li>${item}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${q.follow_up_questions && q.follow_up_questions.length > 0 ? `
                        <div class="question-section">
                            <div class="question-section-title">➡️ Likely Follow-Up Questions</div>
                            <ul class="follow-up-list">
                                ${q.follow_up_questions.map(fq => `<li>${fq}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${q.likely_follow_ups && q.likely_follow_ups.length > 0 ? `
                        <div class="question-section">
                            <div class="question-section-title">➡️ Likely Follow-Ups</div>
                            <ul class="follow-up-list">
                                ${q.likely_follow_ups.map(fq => `<li>${fq}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    });
    
    html += `</div>`;
    return html;
}

function generateStarTemplate(star) {
    return `
        <div class="star-template">
            <div class="star-template-title">⭐ STAR Method Framework</div>
            ${star.situation ? `
                <div class="star-item">
                    <span class="star-label">Situation:</span>
                    <span class="star-description">${star.situation}</span>
                </div>
            ` : ''}
            ${star.task ? `
                <div class="star-item">
                    <span class="star-label">Task:</span>
                    <span class="star-description">${star.task}</span>
                </div>
            ` : ''}
            ${star.action ? `
                <div class="star-item">
                    <span class="star-label">Action:</span>
                    <span class="star-description">${star.action}</span>
                </div>
            ` : ''}
            ${star.result ? `
                <div class="star-item">
                    <span class="star-label">Result:</span>
                    <span class="star-description">${star.result}</span>
                </div>
            ` : ''}
        </div>
    `;
}

function generateAskInterviewerSection(questions) {
    let html = `
        <div class="ask-interviewer-section">
            <h3 style="margin-bottom: 8px;">❓ Smart Questions to Ask the Interviewer</h3>
            <p style="opacity: 0.9; margin-bottom: 16px;">Asking thoughtful questions shows engagement and helps you evaluate the opportunity</p>
            <div class="ask-questions-grid">
    `;
    
    questions.forEach(q => {
        html += `
            <div class="ask-question-card">
                <div class="ask-question-text">${q.question}</div>
                ${q.why_effective ? `
                    <div class="ask-question-why">${q.why_effective}</div>
                ` : ''}
                ${q.category ? `
                    <div style="margin-top: 8px;">
                        <span class="category-badge" style="background: rgba(255,255,255,0.2); color: white;">${q.category}</span>
                    </div>
                ` : ''}
            </div>
        `;
    });
    
    html += `
            </div>
        </div>
    `;
    
    return html;
}

function generateOverallStrategy(strategy) {
    let html = `
        <div class="overall-strategy-section">
            <h3 style="margin-bottom: 8px;">🎯 Overall Interview Strategy</h3>
            <p style="opacity: 0.9; margin-bottom: 20px;">Comprehensive preparation checklist and strategic guidance</p>
            <div class="strategy-grid">
    `;
    
    if (strategy.strengths_to_highlight && strategy.strengths_to_highlight.length > 0) {
        html += `
            <div class="strategy-card">
                <h4>💪 Your Key Strengths</h4>
                <ul>
                    ${strategy.strengths_to_highlight.map(s => `<li>${s}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (strategy.potential_concerns && strategy.potential_concerns.length > 0) {
        html += `
            <div class="strategy-card">
                <h4>⚡ Potential Concerns to Address</h4>
                <ul>
                    ${strategy.potential_concerns.map(c => `<li>${c}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (strategy.preparation_priorities && strategy.preparation_priorities.length > 0) {
        html += `
            <div class="strategy-card">
                <h4>📋 Preparation Priorities</h4>
                <ul>
                    ${strategy.preparation_priorities.map(p => `<li>${p}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (strategy.company_research_checklist && strategy.company_research_checklist.length > 0) {
        html += `
            <div class="strategy-card">
                <h4>🔍 Company Research Checklist</h4>
                <ul>
                    ${strategy.company_research_checklist.map(c => `<li>${c}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    html += `
            </div>
        </div>
    `;
    
    return html;
}

function generateMockScorecard(scorecard) {
    if (!scorecard.criteria || scorecard.criteria.length === 0) return '';
    
    let html = `
        <div class="scorecard-section">
            <div class="scorecard-title">📊 Mock Interview Evaluation Scorecard</div>
            <p style="color: var(--text-light); margin-bottom: 20px;">
                Use this to practice and self-evaluate your interview performance
            </p>
            <div class="scorecard-criteria">
    `;
    
    scorecard.criteria.forEach(criterion => {
        html += `
            <div class="criteria-item">
                <div class="criteria-header">
                    <span class="criteria-name">${criterion.area}</span>
                    <span class="criteria-weight">${criterion.weight}%</span>
                </div>
                ${criterion.evaluation_points && criterion.evaluation_points.length > 0 ? `
                    <ul class="criteria-points">
                        ${criterion.evaluation_points.map(point => `<li>${point}</li>`).join('')}
                    </ul>
                ` : ''}
            </div>
        `;
    });
    
    html += `
            </div>
        </div>
    `;
    
    return html;
}

function addQuestionCardHandlers() {
    document.querySelectorAll('.question-card').forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't toggle if clicking on a link or button
            if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') return;
            
            this.classList.toggle('collapsed');
            this.classList.toggle('expanded');
        });
    });
}
