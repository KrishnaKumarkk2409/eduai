async function fetchNews() {
    try {
        const response = await fetch('/api/news'); // Fetch data from the API
        const newsData = await response.json();
        const newsSlider = document.getElementById('news-slider');
        newsSlider.innerHTML = ''; // Clear existing content

        // Loop through the news data and create HTML elements
        newsData.forEach(news => {
            const slide = document.createElement('div');
            slide.className = 'swiper-slide';
            slide.innerHTML = `
                <div class="news-card">
                    <img src="${news.image_link}" alt="${news.title}" class="news-image">
                    <button class="like-button" onclick="toggleLike(event)">
                        <img src="static/images/unlike.svg" alt="Heart" class="heart-icon">
                    </button>
                    <div class="news-content">
                        <div class="news-date">${new Date(news.date_of_published).toLocaleDateString()}</div>
                        <h3 class="news-title">${news.title}</h3>
                        <p class="news-author">${news.summary}</p>
                    </div>
                </div>
            `;
            newsSlider.appendChild(slide);
        });

        // Initialize Swiper after populating the slides
        const swiper = new Swiper('.swiper-container', {
            loop: true, // Enable infinite looping
            simulateTouch: true, // Enable mouse drag/swipe
            spaceBetween: 30, // Space between slides
            slidesPerView: 1, // Number of slides visible at a time
            breakpoints: {
                768: {
                    slidesPerView: 2, // Show 2 slides on medium screens
                },
                1024: {
                    slidesPerView: 3, // Show 3 slides on large screens
                },
            },
        });
    } catch (error) {
        console.error('Error fetching news:', error);
    }
}

function toggleLike(event) {
    const button = event.currentTarget; // Use currentTarget to ensure we get the button element
    const heartImage = button.querySelector('img'); // Find the image inside the button

    // Toggle between the two heart SVG images
    if (heartImage.src.includes("unlike.svg")) {
        heartImage.src = "static/images/like.svg"; // Change to filled heart
    } else {
        heartImage.src = "static/images/unlike.svg"; // Change to unfilled heart
    }
}


// Call the fetchNews function when the page loads
window.onload = fetchNews;

document.addEventListener('DOMContentLoaded', function () {
    const dots = document.querySelectorAll('.dot');
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;

    // Function to update the active dot and slide
    function updateSlider() {
        // Reset all dots and slides to inactive
        dots.forEach(dot => dot.classList.remove('active'));
        slides.forEach(slide => slide.classList.remove('active'));

        // Set the current dot and slide to active
        dots[currentSlide].classList.add('active');
        slides[currentSlide].classList.add('active');
    }

    // Add click events to dots
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            updateSlider();
        });
    });

    // Auto-advance slides (dots and images)
    function nextSlide() {
        currentSlide = (currentSlide + 1) % dots.length;
        updateSlider();
    }

    // Start auto-advance timer (every 5 seconds)
    setInterval(nextSlide, 5000);

    // Initialize the first dot and slide to be active
    updateSlider();
});


async function fetchLocation() {
    let url = "https://ipinfo.io/124.253.250.142?token=f2ba83e357b614"; 
    let response = await fetch(url);
    let data = await response.json();
    
    // Extract the city and region (state) from the response
    const city = data.city || "Unknown City";
    // const region = data.region || "Unknown Region";
    
    // Update the location span with city and state
    document.getElementById("user-location").textContent = `${city}`;
}

fetchLocation();



function openGeneralKnowledgePage() {
    window.location.href = "/general_knowledge";  
}


