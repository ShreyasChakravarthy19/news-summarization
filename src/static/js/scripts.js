// This file contains JavaScript code for client-side interactivity, handling user input and API calls to the backend.

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('news-form');
    const resultContainer = document.getElementById('result-container');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        const companyName = document.getElementById('company-name').value;

        try {
            const response = await fetch(`/api/news?company=${encodeURIComponent(companyName)}`);
            const data = await response.json();

            if (response.ok) {
                displayResults(data);
            } else {
                resultContainer.innerHTML = `<p>Error: ${data.message}</p>`;
            }
        } catch (error) {
            resultContainer.innerHTML = `<p>Error: ${error.message}</p>`;
        }
    });

    function displayResults(data) {
        resultContainer.innerHTML = '';
        data.articles.forEach(article => {
            const articleElement = document.createElement('div');
            articleElement.classList.add('article');
            articleElement.innerHTML = `
                <h3>${article.title}</h3>
                <p>${article.summary}</p>
                <a href="${article.link}" target="_blank">Read more</a>
            `;
            resultContainer.appendChild(articleElement);
        });

        const sentimentElement = document.createElement('div');
        sentimentElement.innerHTML = `<h4>Sentiment Analysis</h4><p>${data.sentiment}</p>`;
        resultContainer.appendChild(sentimentElement);
    }
});