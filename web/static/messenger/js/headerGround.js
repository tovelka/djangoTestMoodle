let lastScroll = 0;
const header = document.getElementsByClassName('header')[0];

function updateHeader() {
    const currentScroll = window.scrollY;
    
    if (currentScroll > 200) {
        if (currentScroll > 150){
            header.classList.add('scrolled'); 
        }
    }
    else {
        header.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
}

// Оптимизация с помощью requestAnimationFrame
let isScrolling;
window.addEventListener('scroll', function() {
    window.cancelAnimationFrame(isScrolling);
    isScrolling = window.requestAnimationFrame(updateHeader);
});