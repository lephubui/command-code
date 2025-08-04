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
document.addEventListener('DOMContentLoaded', function() {
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
});

// Add smooth scroll behavior for better UX
function smoothScrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Optional: Add scroll to top functionality
window.addEventListener('scroll', function() {
    // You can add a scroll-to-top button here if needed
});