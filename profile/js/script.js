// Global variable to store portfolio data
let portfolioData = null;

// Load data from JSON file
async function loadPortfolioData() {
    try {
        const response = await fetch('data/data.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        portfolioData = await response.json();
        populateContent();
    } catch (error) {
        console.error('Error loading portfolio data:', error);
        // Fallback content in case of error
        document.getElementById('header-name').textContent = 'Error Loading Data';
        document.getElementById('header-title').textContent = 'Please refresh the page';
    }
}

// Populate HTML content with data from JSON
function populateContent() {
    if (!portfolioData) return;

    // Populate header
    document.getElementById('header-name').textContent = portfolioData.personal.name;
    document.getElementById('header-title').textContent = portfolioData.personal.title;
    
    // Populate contact info with email and social media
    const contactInfo = document.getElementById('contact-info');
    const emailLink = `<a href="mailto:${portfolioData.personal.email}">📧 ${portfolioData.personal.email}</a>`;
    const socialLinks = portfolioData.personal.socialMedia.map(social => 
        `<a href="${social.url}" target="_blank" rel="noopener noreferrer">${social.icon} ${social.platform}</a>`
    ).join('');
    
    contactInfo.innerHTML = emailLink + socialLinks;

    // Populate navigation
    const navigation = document.getElementById('navigation');
    navigation.innerHTML = portfolioData.navigation.map(item => 
        `<li><a href="${item.href}">${item.text}</a></li>`
    ).join('');

    // Populate summary
    document.getElementById('summary-text').textContent = portfolioData.summary;

    // Populate skills
    const skillsGrid = document.getElementById('skills-grid');
    skillsGrid.innerHTML = portfolioData.skills.map(skillCategory => `
        <div class="skill-category">
            <h3>${skillCategory.category}</h3>
            <div class="skill-tags">
                ${skillCategory.items.map(skill => 
                    `<span class="skill-tag">${skill}</span>`
                ).join('')}
            </div>
        </div>
    `).join('');

    // Populate projects
    const projectsGrid = document.getElementById('projects-grid');
    projectsGrid.innerHTML = portfolioData.projects.map(project => `
        <div class="project-card">
            <div class="project-header">
                <div class="project-icon">${project.icon}</div>
                <div class="project-title-section">
                    <h3 class="project-title">${project.title}</h3>
                    <div class="project-status ${project.status.toLowerCase()}">${project.status}</div>
                </div>
            </div>
            <p class="project-description">${project.description}</p>
            <div class="project-technologies">
                ${project.technologies.map(tech => 
                    `<span class="tech-tag">${tech}</span>`
                ).join('')}
            </div>
            <div class="project-highlights">
                <h4>Key Features:</h4>
                <ul>
                    ${project.highlights.map(highlight => 
                        `<li>${highlight}</li>`
                    ).join('')}
                </ul>
            </div>
            <div class="project-actions">
                <a href="${project.url}" target="_blank" rel="noopener noreferrer" class="project-link">
                    🔗 Visit Project
                </a>
            </div>
        </div>
    `).join('');

    // Populate experience
    const experienceTimeline = document.getElementById('experience-timeline');
    experienceTimeline.innerHTML = portfolioData.experience.map(job => `
        <div class="job">
            <div class="job-header">
                <div class="job-title">${job.title}</div>
                <div class="company">${job.company}</div>
                <div class="job-meta">${job.period} | ${job.location}</div>
            </div>
            <div class="job-description">
                <p>${job.description}</p>
                <ul>
                    ${job.responsibilities.map(responsibility => 
                        `<li>${responsibility}</li>`
                    ).join('')}
                </ul>
            </div>
        </div>
    `).join('');

    // Populate education
    const educationGrid = document.getElementById('education-grid');
    educationGrid.innerHTML = portfolioData.education.map(edu => `
        <div class="education-item">
            <div class="degree">${edu.degree}</div>
            <div class="university">${edu.university}</div>
        </div>
    `).join('');

    // Populate AI Contents with break lines between platforms
    const aiContentsSection = document.getElementById('ai-contents-section');
    const platformLinks = portfolioData.aiContents.platforms.map((platform, index) => {
        const link = `
            <a href="${platform.url}" target="_blank" rel="noopener noreferrer" class="ai-platform-link">
                <span class="platform-icon">${platform.icon}</span>
                <span class="platform-name">${platform.platform}</span>
                <span class="platform-handle">Command & Code</span>
            </a>
        `;
        
        // Add break line after each platform except the last one
        return index < portfolioData.aiContents.platforms.length - 1 
            ? link + '<div class="platform-break"></div>' 
            : link;
    }).join('');

    aiContentsSection.innerHTML = `
        <div class="ai-contents-content">
            <p class="ai-description">${portfolioData.aiContents.description}</p>
            <div class="ai-platforms">
                ${platformLinks}
            </div>
        </div>
    `;

    // Populate footer
    document.getElementById('footer-text').textContent = portfolioData.footer.copyright;

    // Initialize animations and interactions after content is loaded
    initializeInteractions();
}

// Initialize all interactions after content is loaded
function initializeInteractions() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Smooth scrolling for CTA button
    document.querySelector('.cta-btn').addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });

    // Add scroll effect to navigation
    window.addEventListener('scroll', function() {
        const nav = document.querySelector('.main-nav');
        if (window.scrollY > 100) {
            nav.style.background = 'rgba(255,255,255,0.98)';
            nav.style.backdropFilter = 'blur(20px)';
        } else {
            nav.style.background = '#fff';
            nav.style.backdropFilter = 'none';
        }
    });

    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all animatable elements
    document.querySelectorAll('.skill-category, .job, .education-item, .project-card, .ai-platform-link').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Load portfolio data when the page loads
document.addEventListener('DOMContentLoaded', function() {
    loadPortfolioData();
});