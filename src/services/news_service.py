import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from collections import Counter
import spacy
import re
from urllib.parse import urljoin, quote_plus
import time

class NewsService:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.nlp = spacy.load("en_core_web_sm")
        # Using more accessible news sources
        self.news_sources = [
            {
                'url': 'https://news.google.com/rss/search?q=',
                'type': 'rss'
            },
            {
                'url': 'https://www.marketwatch.com/search?q=',
                'type': 'html'
            },
            {
                'url': 'https://www.techradar.com/search?searchTerm=',
                'type': 'html'
            }
        ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
    
    def extract_keywords(self, text):
        """
        Extract meaningful keywords using spaCy.
        """
        doc = self.nlp(text)
        keywords = []

        # Extract named entities (e.g., ORG, PERSON, GPE)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PERSON", "GPE", "PRODUCT", "EVENT"]:
                keywords.append(ent.text)

        # Extract noun phrases
        for chunk in doc.noun_chunks:
            keywords.append(chunk.text)

        # Return the most common keywords
        return [keyword for keyword, _ in Counter(keywords).most_common(10)]

    def extract_topics(self, text):
        doc = self.nlp(text)
        # Extract named entities and noun phrases
        entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'EVENT', 'TECH']]
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        
        # Combine and get most common topics
        all_topics = entities + noun_phrases
        return [topic for topic, _ in Counter(all_topics).most_common(5)]

    def process_article(self, title, full_text):
        # Clean and prepare text
        cleaned_text = self.clean_text(f"{title}. {full_text}")
        
        # Generate summary
        summary = self.summarize_text(cleaned_text)
        
        # Extract topics
        topics = self.extract_topics(cleaned_text)
        
        return {
            'summary': summary,
            'topics': topics
        }

    def fetch_rss_feed(self, url, company_name):
        try:
            full_url = f"{url}{quote_plus(company_name)}"
            response = requests.get(full_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            
            articles = []
            for item in items[:5]:
                title = item.title.text if item.title else ''
                description = item.description.text if item.description else ''
                link = item.link.text if item.link else ''
                
                if title and description:
                    articles.append({
                        'title': self.clean_text(title),
                        'full_summary': self.clean_text(description),
                        'link': link,
                        'source': 'Google News'
                    })
            return articles
        except Exception as e:
            print(f"Error fetching RSS feed: {e}")
            return []

    def fetch_html_page(self, source, company_name):
        try:
            full_url = f"{source['url']}{quote_plus(company_name)}"
            response = requests.get(full_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            if 'marketwatch.com' in source['url']:
                items = soup.find_all('div', class_='article__content')
                base_url = 'https://www.marketwatch.com'
            elif 'techradar.com' in source['url']:
                items = soup.find_all('div', class_='article-card')
                base_url = 'https://www.techradar.com'
            else:
                items = []
                base_url = ''

            for item in items[:5]:
                try:
                    title = item.find('h3').get_text(strip=True) if item.find('h3') else ''
                    summary = item.find('p').get_text(strip=True) if item.find('p') else ''
                    link_elem = item.find('a')
                    link = urljoin(base_url, link_elem['href']) if link_elem and 'href' in link_elem.attrs else ''
                    
                    if title and (summary or link):
                        articles.append({
                            'title': self.clean_text(title),
                            'full_summary': self.clean_text(summary),
                            'link': link,
                            'source': base_url
                        })
                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue
                    
            return articles
        except Exception as e:
            print(f"Error fetching HTML page: {e}")
            return []

    def clean_text(self, text):
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text

    def summarize_text(self, text):
        try:
            if not text or len(text.strip()) < 50:
                return text
            
            # Calculate appropriate max_length based on input length
            input_length = len(text.split())
            max_length = min(int(input_length * 0.4), 130)  # 40% of input length, max 130 tokens
            min_length = min(int(max_length * 0.6), 30)     # 60% of max_length, max 30 tokens
            
            # Ensure text isn't too long for the model
            max_chars = 1024
            if len(text) > max_chars:
                text = text[:max_chars]
            
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True
            )
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Error in summarization: {e}")
            return text[:100] + "..."

    def fetch_news(self, company_name):
        all_articles = []
        source_summaries = {}

        for source in self.news_sources:
            articles = []
            try:
                if source['type'] == 'rss':
                    articles = self.fetch_rss_feed(source['url'], company_name)
                else:
                    articles = self.fetch_html_page(source, company_name)
                
                for article in articles:
                    processed = self.process_article(article['title'], article['full_summary'])
                    article.update({
                        'summary': processed['summary'],
                        'topics': processed['topics'],
                        'source_type': source['type']
                    })
                    all_articles.append(article)
                
                # Store summaries by source for comparison
                source_name = source['url'].split('/')[2]
                source_summaries[source_name] = {
                    'article_count': len(articles),
                    'topics': self.extract_topics(' '.join([a['full_summary'] for a in articles]))
                }

            except Exception as e:
                print(f"Error processing source {source['url']}: {e}")
                continue

        return {
            'articles': sorted(all_articles, key=lambda x: len(x['topics']), reverse=True)[:10],
            'comparative_analysis': source_summaries
        }