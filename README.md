
<div align="center">
  <h1>📰 News Summarization & Insights App 🎙️</h1>
  <p>
    <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python">
    <img src="https://img.shields.io/badge/Flask-2.x-green?logo=flask" alt="Flask">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
  </p>
  <p><b>Summarize, analyze, and listen to the latest news about any company—all in one place!</b></p>
</div>

> **Note:** Output audio files (`static/output_*.mp3`) are not tracked in version control and will not be pushed to GitHub.

---

## 🚀 Features

- 🔎 **News Extraction:** Fetches the latest news articles about a company or topic.
- 🧠 **AI Summarization:** Uses advanced language models (LLaMA, BART, GPT, etc.) to generate concise summaries and one-line key insights.
- 📊 **Sentiment Analysis:** Detects and visualizes the sentiment (positive, negative, neutral) of each article.
- 🏷️ **Topic Extraction:** Identifies common topics and trends across articles.
- 🆚 **Comparative Analysis:** Compares coverage and sentiment across sources.
- 🔊 **Text-to-Speech:** Converts key insights into audio (Hindi/English) for accessibility.
- 🌐 **Modern Web UI:** Clean, responsive interface built with Flask, HTML, CSS, and JS.

---

## 🗂️ Project Structure

```text
news-summarization-app/
├── src/
│   ├── app.py                # Main Flask app
│   ├── controllers/
│   │   └── news_controller.py
│   ├── services/
│   │   ├── news_service.py
│   │   ├── sentiment_analysis.py
│   │   └── text_to_speech.py
│   ├── templates/            # HTML templates
│   ├── static/               # CSS, JS, and output audio files
│   └── types/
├── requirements.txt
├── README.md
└── config.py
```

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd news-summarization-app
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure settings:**
   - Edit `config.py` to add your API keys and settings (not tracked in git).

---

## ▶️ Usage

1. **Start the app:**
   ```bash
   python src/app.py
   ```
2. **Open your browser:**
   - Go to [http://localhost:5000](http://localhost:5000)
3. **Enter a company name** and get instant news insights, summaries, and audio!

---

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!<br>
Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.