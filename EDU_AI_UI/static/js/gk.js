// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    fetchNews(); // Call the fetchNews function once the page is loaded
});

async function fetchNews() {
    try {
        const response = await fetch('/api/news'); // Fetch data from the API
        const newsData = await response.json();
        const contentContainer = document.querySelector('.content-container');
        contentContainer.innerHTML = ''; // Clear existing content

        // Loop through the news data and create HTML elements
        newsData.forEach(news => {
            // Format the date to display as Friday, 14 February, 2025
            const date = new Date(news.date_of_published);
            const formattedDate = date.toLocaleDateString('en-GB', {
                weekday: 'long',  // Day of the week (e.g., "Friday")
                day: '2-digit',   // Day of the month (e.g., "14")
                month: 'long',    // Month (e.g., "February")
                year: 'numeric'   // Year (e.g., "2025")
            });

            const contentItem = document.createElement('div');
            contentItem.className = 'content-item';
            contentItem.innerHTML = `
                <div class="content-text">
                    <h2>${news.title}</h2>
                    <h4>${formattedDate}</h4> 
                    <p>${news.summary}</p>
                    <button class="read-more" data-id="${news.id}">Read More</button>
                </div>
                <div class="content-image">
                    <img src="${news.image_link}" alt="${news.title}" />
                </div>
            `;
            contentContainer.appendChild(contentItem);
        });

        // Add event listeners to each "Read More" button
        const readMoreButtons = document.querySelectorAll('.read-more');
        readMoreButtons.forEach(button => {
            button.addEventListener('click', function () {
                const newsId = button.getAttribute('data-id');
                // Redirect to the details page with the newsId as a query parameter
                window.location.href = `/details?id=${newsId}`;
            });
        });

    } catch (error) {
        console.error('Error fetching news:', error);
    }
}
