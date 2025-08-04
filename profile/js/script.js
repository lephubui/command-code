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
    
    // Populate contact info
    const contactInfo = document.getElementById('contact-info');
    contactInfo.innerHTML = `
        <a href="mailto:${portfolioData.personal.email}">📧 ${portfolioData.personal.email}</a>
        <a href="${portfolioData.personal.linkedin}" target="_blank">💼 LinkedIn</a>
    `;

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

    // Add scroll effect to navigation
    window.addEventListener('scroll', function() {
        const nav = document.querySelector('nav');
        if (window.scrollY > 100) {
            nav.style.background = 'rgba(255,255,255,0.98)';
        } else {
            nav.style.background = 'rgba(255,255,255,0.95)';
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

    // Observe all skill categories and job items
    document.querySelectorAll('.skill-category, .job, .education-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Add typing effect to the header
    const headerText = document.querySelector('.header-content h1');
    if (headerText) {
        headerText.style.overflow = 'hidden';
        headerText.style.borderRight = '3px solid rgba(255,255,255,0.7)';
        headerText.style.whiteSpace = 'nowrap';
        headerText.style.animation = 'typing 3s steps(40, end), blink-caret 0.75s step-end infinite';
        
        // Remove typing effect after animation completes
        setTimeout(() => {
            headerText.style.borderRight = 'none';
            headerText.style.animation = 'none';
        }, 4000);
    }
}

// Load portfolio data when the page loads
document.addEventListener('DOMContentLoaded', function() {
    loadPortfolioData();
});

// Optional: Add smooth scroll behavior for better UX
function smoothScrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}