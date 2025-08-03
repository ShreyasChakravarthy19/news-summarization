from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from sentence_transformers import SentenceTransformer, util
from langchain.memory import ConversationBufferMemory
from transformers import AutoTokenizer, AutoModelForCausalLM

class NewsController:
    def __init__(self, news_service, sentiment_service, tts_service):
        self.news_service = news_service
        self.sentiment_service = sentiment_service
        self.tts_service = tts_service
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')  # For semantic similarity
        self.memory = ConversationBufferMemory(memory_key="chat_history", output_key="output", return_messages=True)

        # Load LLaMA 2 or similar model
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", use_auth_token=True)  # Replace with LLaMA 3 if available
        self.model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf", device_map="auto")
        self.summarizer = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, use_auth_token=True, device_map="auto")

    def generate_one_line_summary(self, articles):
        """
        Generate a concise summary that highlights the key takeaway from all articles using LLaMA 2 or similar models.
        """
        # Combine all article summaries into one text      
        combined_text = " ".join([article['summary'] for article in articles])

        # Ensure the text is not too long for the model
        max_chars = 1024
        if len(combined_text) > max_chars:
            combined_text = combined_text[:max_chars]

        # Generate summary using LLaMA 2 or similar model
        try:
            prompt = f"Summarize the following news articles into one concise sentence: {combined_text}"
            response = self.summarizer(prompt, max_length=50, num_return_sequences=1, do_sample=False)
            return response[0]['generated_text']
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Unable to generate summary at this time."

    def get_news(self, company_name):
        """
        Fetch news articles for the given company name using the news service.
        """
        return self.news_service.fetch_news(company_name)

    def analyze_sentiment(self, articles):
        """
        Analyze the sentiment of the given articles using the sentiment service.
        """
        return self.sentiment_service.analyze_sentiment(articles)

    def calculate_overall_sentiment(self, sentiment_results):
        """
        Calculate the overall sentiment based on individual sentiment results.
        """
        if not sentiment_results:
            return 'Neutral'
        
        # Calculate total sentiment score
        total_scores = {
            'positive': 0.0,
            'negative': 0.0,
            'neutral': 0.0
        }
        
        for result in sentiment_results:
            scores = result['scores']
            for sentiment in total_scores:
                total_scores[sentiment] += scores[sentiment]
        
        # Calculate total weight
        total_weight = sum(total_scores.values())
        if total_weight > 0:
            # Normalize scores
            normalized_scores = {
                k: v / total_weight for k, v in total_scores.items()
            }
            
            # Apply thresholds for classification
            if normalized_scores['positive'] > 0.45:
                return 'Positive'
            elif normalized_scores['negative'] > 0.45:
                return 'Negative'
            elif abs(normalized_scores['positive'] - normalized_scores['negative']) > 0.15:
                return 'Positive' if normalized_scores['positive'] > normalized_scores['negative'] else 'Negative'
        
        return 'Neutral'

    def compare_articles(self, articles):
        """
        Compare articles using semantic similarity.
        """
        comparisons = []
        summaries = [article['summary'] for article in articles]
        embeddings = self.semantic_model.encode(summaries, convert_to_tensor=True)

        for i in range(len(articles)):
            for j in range(i + 1, len(articles)):
                similarity = util.pytorch_cos_sim(embeddings[i], embeddings[j]).item()
                comparison = {
                    'Article 1': articles[i]['title'],
                    'Article 2': articles[j]['title'],
                    'Similarity': round(similarity, 2),
                    'Impact': f"Article 1 discusses {articles[i]['title']}, while Article 2 focuses on {articles[j]['title']}."
                }
                comparisons.append(comparison)

        # Sort comparisons by similarity (descending)
        comparisons.sort(key=lambda x: x['Similarity'], reverse=True)
        return comparisons

    def extract_common_topics(self, articles):
        """
        Extract common topics from the given articles.
        """
        all_topics = [topic for article in articles for topic in article['topics']]
        common_topics = [topic for topic, count in Counter(all_topics).items() if count > 1]
        return common_topics

    def convert_text_to_speech(self, text):
        """
        Convert the given text to speech using the TTS service.
        """
        return self.tts_service.convert_text_to_speech(text)