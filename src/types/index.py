from typing import List, Dict

class Article:
    def __init__(self, title: str, summary: str, link: str):
        self.title = title
        self.summary = summary
        self.link = link

class SentimentResult:
    def __init__(self, article: Article, sentiment: str):
        self.article = article
        self.sentiment = sentiment

class ComparativeAnalysis:
    def __init__(self, articles: List[Article]):
        self.articles = articles

    def compare_sentiments(self) -> Dict[str, int]:
        sentiment_count = {'positive': 0, 'negative': 0, 'neutral': 0}
        # Logic for comparing sentiments would go here
        return sentiment_count