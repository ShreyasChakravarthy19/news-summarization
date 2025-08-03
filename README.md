# News Summarization and Text-to-Speech Application

This project is a web-based application that extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts comparative analysis, and generates text-to-speech output in Hindi.

## Project Structure

```
news-summarization-app
├── src
│   ├── app.py                     # Main entry point of the application
│   ├── controllers
│   │   └── news_controller.py      # Handles requests related to news articles
│   ├── services
│   │   ├── news_service.py         # Fetches news articles from the web
│   │   ├── sentiment_analysis.py    # Performs sentiment analysis on articles
│   │   └── text_to_speech.py       # Converts summarized content into Hindi speech
│   ├── templates
│   │   └── index.html              # HTML template for the web interface
│   ├── static
│   │   ├── css
│   │   │   └── styles.css          # CSS styles for the web application
│   │   └── js
│   │       └── scripts.js          # JavaScript for client-side interactivity
│   └── types
│       └── index.py                # Custom types and data structures
├── requirements.txt                # Lists project dependencies
├── README.md                       # Documentation for the project
└── config.py                       # Configuration settings for the application
```

## Features

- **News Extraction**: Fetches the latest news articles related to a specified company.
- **Sentiment Analysis**: Analyzes the sentiment of the articles and categorizes them as positive, negative, or neutral.
- **Comparative Analysis**: Compares sentiments across multiple articles to provide insights.
- **Text-to-Speech**: Generates audio output of the summarized content in Hindi.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd news-summarization-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the application settings in `config.py`.

## Usage

1. Run the application:
   ```
   python src/app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000` to access the application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.