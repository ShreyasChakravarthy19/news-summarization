from flask import Flask, request, jsonify, render_template, url_for
import os
import time
from controllers.news_controller import NewsController
from services.news_service import NewsService
from services.sentiment_analysis import SentimentAnalysisService
from services.text_to_speech import TextToSpeechService

app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'static')
)

# Create necessary directories
os.makedirs(app.template_folder, exist_ok=True)
os.makedirs(app.static_folder, exist_ok=True)

# Add zip to Jinja2 environment
app.jinja_env.globals.update(zip=zip)

# Initialize services
news_service = NewsService()
sentiment_service = SentimentAnalysisService()
tts_service = TextToSpeechService()

news_controller = NewsController(news_service, sentiment_service, tts_service)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_company():
    company_name = request.form.get('company_name')
    if not company_name:
        return jsonify({'error': 'Company name is required'}), 400

    # Fetch news articles
    articles_data = news_controller.get_news(company_name)
    if not articles_data['articles']:
        return render_template('results.html', error="No news articles found")

    # Analyze sentiment
    sentiment_results = news_controller.analyze_sentiment(articles_data['articles'])
    
    # Calculate overall sentiment
    overall_sentiment = news_controller.calculate_overall_sentiment(sentiment_results)
    
    # Compare articles
    coverage_differences = news_controller.compare_articles(articles_data['articles'])
    
    # Extract common topics
    common_topics = news_controller.extract_common_topics(articles_data['articles'])
    
    # Generate a key takeaway
    key_takeaway = news_controller.generate_one_line_summary(articles_data['articles'])
    
    # Combine overall sentiment and key takeaway for TTS
    tts_text = f"The overall sentiment for {company_name} news is {overall_sentiment}. Key insight: {key_takeaway}"
    audio_file = news_controller.convert_text_to_speech(tts_text)

    return render_template(
        'results.html',
        articles=articles_data['articles'],
        sentiment_results=sentiment_results,
        overall_sentiment=overall_sentiment,
        audio_file=audio_file,
        coverage_differences=coverage_differences,
        common_topics=common_topics
    )

os.makedirs(os.path.join(os.path.dirname(__file__), 'static'), exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True)