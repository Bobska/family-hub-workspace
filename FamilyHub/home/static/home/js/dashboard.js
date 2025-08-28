// Dashboard specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard loaded successfully');
    
    // Add smooth hover effects for app cards
    const appCards = document.querySelectorAll('.app-card');
    appCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add click analytics (placeholder)
    appCards.forEach(card => {
        card.addEventListener('click', function() {
            const appName = this.querySelector('.card-title').textContent;
            console.log(`Clicked on ${appName} app`);
            // Add analytics tracking here if needed
        });
    });
});
