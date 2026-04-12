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
    const socialLinks = portfolioData.personal.socialMedia.map(social => 
        `<a href="${social.url}" target="_blank" rel="noopener noreferrer">${social.platform}</a>`
    ).join('');
    
    contactInfo.innerHTML = socialLinks;

    // Populate navigation
    const navigation = document.getElementById('navigation');
    navigation.innerHTML = portfolioData.navigation.map(item => 
        `<li><a href="${item.href}">${item.text}</a></li>`
    ).join('');

    // Populate summary
    const summary = portfolioData.summary;
    document.getElementById('summary-tagline').textContent = summary.tagline;
    document.getElementById('summary-text').textContent = summary.description;
    const metricsContainer = document.getElementById('summary-metrics');
    metricsContainer.innerHTML = summary.metrics.map(m => `
        <div class="summary-metric">
            <span class="metric-value">${m.value}</span>
            <span class="metric-label">${m.label}</span>
        </div>
    `).join('');

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
            ${project.image ? `
            <div class="project-screenshot">
                <img src="${project.image}" alt="${project.title} screenshot" loading="lazy">
                <div class="screenshot-overlay"></div>
            </div>` : ''}
            <div class="project-body">
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
                        Try It Live →
                    </a>
                </div>
            </div>
        </div>
    `).join('') + `
        <div class="project-card">
            <div class="project-screenshot">
                <img src="public/images/WebFirewall.png" alt="Web Firewall screenshot" loading="lazy">
                <div class="screenshot-overlay"></div>
            </div>
            <div class="project-body">

                <div class="project-header">
                    <div class="project-icon">🛡️</div>
                    <div class="project-title-section">
                        <h3 class="project-title">Web Firewall</h3>
                        <div class="project-status published">Published</div>
                    </div>
                </div>
                <p class="project-description">Advanced Chrome extension that provides real-time protection against XSS, SQL injection, malicious scripts, and tracking — with multi-level security modes and a live telemetry dashboard.</p>
                <div class="project-technologies">
                    <span class="tech-tag">JavaScript</span>
                    <span class="tech-tag">Chrome Extensions API</span>
                    <span class="tech-tag">Manifest V3</span>
                    <span class="tech-tag">Declarative Net Request</span>
                </div>
                <div class="project-highlights">
                    <h4>Key Features:</h4>
                    <ul>
                        <li>Multi-level security: Balanced, Maximum, and Custom rule modes</li>
                        <li>XSS, SQL injection, and malicious script blocking</li>
                        <li>Live telemetry dashboard with export (JSON/CSV)</li>
                        <li>JSON-based custom rules for power users</li>
                    </ul>
                </div>
                <div class="project-actions">
                    <a href="https://chromewebstore.google.com/detail/command-code-web-firewall/mefiifjaoonlidppjkhhchohdgpbbfhn" target="_blank" rel="noopener noreferrer" class="project-link">
                        Get It Free →
                    </a>
                </div>
            </div>
        </div>
    `;

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

    // Populate AI Contents as inline marquee
    const aiContentsSection = document.getElementById('ai-contents-section');
    const platformItems = portfolioData.aiContents.platforms.map(platform =>
        `<a href="${platform.url}" target="_blank" rel="noopener noreferrer" class="ai-platform-link">
            <span class="platform-icon">${platform.icon}</span>
            <span class="platform-name">${platform.platform}</span>
            <span class="platform-handle">Command & Code</span>
        </a>`
    ).join('');

    // Duplicate items to create seamless infinite scroll
    aiContentsSection.innerHTML = `
        <div class="ai-contents-content">
            <p class="ai-description">${portfolioData.aiContents.description}</p>
            <div class="ai-marquee-wrapper">
                <div class="ai-marquee-track">
                    ${platformItems}
                    ${platformItems}
                </div>
            </div>
        </div>
    `;

    // Populate Contact section
    const contactSection = document.getElementById('contact-section');
    const contactSocials = portfolioData.personal.socialMedia.map(social =>
        `<a href="${social.url}" target="_blank" rel="noopener noreferrer">${social.platform}</a>`
    ).join('');
    contactSection.innerHTML = `
        <p class="contact-description">Interested in collaborating or have a question? Feel free to reach out.</p>
        <a href="mailto:${portfolioData.personal.email}" class="contact-email-btn">Get In Touch</a>
        <div class="contact-socials">${contactSocials}</div>
    `;

    // Populate footer
    const footerLinks = document.getElementById('footer-links');
    const navLinks = portfolioData.navigation.map(item =>
        `<a href="${item.href}">${item.text}</a>`
    ).join('');
    footerLinks.innerHTML = navLinks + '<div class="footer-divider"></div>';
    document.getElementById('footer-text').textContent = portfolioData.footer.copyright;

    // Initialize animations and interactions after content is loaded
    initializeInteractions();
}

// Initialize all interactions after content is loaded
function initializeInteractions() {
    // Hamburger menu toggle
    const hamburger = document.getElementById('hamburger');
    const navigation = document.getElementById('navigation');

    hamburger.addEventListener('click', function() {
        this.classList.toggle('active');
        navigation.classList.toggle('open');
        this.setAttribute('aria-expanded', navigation.classList.contains('open'));
    });

    // Close menu when a nav link is clicked (mobile)
    navigation.addEventListener('click', function(e) {
        if (e.target.tagName === 'A') {
            hamburger.classList.remove('active');
            navigation.classList.remove('open');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    });

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
            nav.style.background = 'rgba(12, 12, 20, 0.98)';
            nav.style.backdropFilter = 'blur(20px)';
        } else {
            nav.style.background = 'rgba(12, 12, 20, 0.95)';
            nav.style.backdropFilter = 'blur(20px)';
        }
    });

    // Animate elements on scroll with staggered delays
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Apply reveal class with staggered delays per group
    const revealGroups = [
        '.skill-category',
        '.project-card',
        '.job',
        '.education-item',
        '.summary-metric'
    ];

    revealGroups.forEach(selector => {
        document.querySelectorAll(selector).forEach((el, i) => {
            el.classList.add('reveal');
            el.style.transitionDelay = `${i * 0.1}s`;
            observer.observe(el);
        });
    });

    // Summary tagline and description fade in
    document.querySelectorAll('.summary-tagline, .summary-description').forEach(el => {
        el.classList.add('reveal');
        observer.observe(el);
    });

    // Section titles fade in separately
    document.querySelectorAll('.section-title').forEach(el => {
        el.classList.add('reveal');
        observer.observe(el);
    });
}

// Load portfolio data when the page loads
document.addEventListener('DOMContentLoaded', function() {
    loadPortfolioData();
});