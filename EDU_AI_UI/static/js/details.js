document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const newsId = urlParams.get('id'); // Get the news ID from the URL

    if (newsId) {
        // Fetch the full article based on the newsId
        fetchArticle(newsId);
    }
});

// Function to fetch the full article using the newsId
async function fetchArticle(newsId) {
    try {
        const response = await fetch(`/api/news/${newsId}`); // Fetch full article details from the backend
        const article = await response.json();

        // Log the article to check the data structure
        console.log(article);

        // Display the full article in the HTML
        if (article) {
            document.querySelector('#article-title').textContent = article.title || 'No title available';
            document.querySelector('#article-date').textContent = new Date(article.date_of_published).toLocaleDateString('en-GB') || 'No date available';
            document.querySelector('#article-content').textContent = article.content || 'No content available';
            
            // Set the breadcrumb article title dynamically
            document.querySelector('#breadcrumb-article-title').textContent = article.title || 'No title available';

            // Set the image if available
            const articleImage = document.querySelector('#article-image');
            if (article.image_link) {
                articleImage.src = article.image_link;
            } else {
                articleImage.style.display = 'none'; // Hide image if there's no image link
            }
        } else {
            console.error('Article data is missing or incorrect');
        }

    } catch (error) {
        console.error('Error fetching article details:', error);
    }
}
