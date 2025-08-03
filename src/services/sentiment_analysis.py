from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

class SentimentAnalysisService:
    def __init__(self):
        model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()
        self.labels = ['negative', 'neutral', 'positive']

    def get_sentiment_scores(self, text):
        try:
            # Tokenize and encode text
            encoded_input = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
            
            # Get model prediction
            with torch.no_grad():
                output = self.model(**encoded_input)
                scores = torch.nn.functional.softmax(output.logits, dim=1)
            
            # Convert to numpy array
            scores = scores.numpy()[0]
            
            # Create sentiment scores dictionary
            sentiment_scores = {
                'negative': float(scores[0]),
                'neutral': float(scores[1]),
                'positive': float(scores[2])
            }
            
            # Get sentiment with highest score
            sentiment = self.labels[np.argmax(scores)]
            
            return sentiment, sentiment_scores
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return 'neutral', {'positive': 0.33, 'neutral': 0.34, 'negative': 0.33}

    def analyze_sentiment(self, articles):
        sentiment_results = []
        
        for article in articles:
            try:
                # Use summarized text for sentiment analysis
                text = article['summary']
                
                # Get sentiment scores
                sentiment, sentiment_scores = self.get_sentiment_scores(text)
                
                sentiment_results.append({
                    'title': article['title'],
                    'summary': article['summary'],
                    'sentiment': sentiment.capitalize(),
                    'scores': sentiment_scores
                })
                
            except Exception as e:
                print(f"Error in sentiment analysis: {e}")
                sentiment_results.append({
                    'title': article['title'],
                    'summary': article['summary'],
                    'sentiment': 'Neutral',
                    'scores': {'positive': 0.33, 'neutral': 0.34, 'negative': 0.33}
                })
        
        return sentiment_results