# 🤖 ArXiv Finance Research Assistant

AI-powered chatbot for analyzing financial research papers from ArXiv using LlamaIndex and OpenAI.

## 🚀 Features

- **Smart Reasoning**: ReActAgent with step-by-step analysis
- **Technical Analysis**: Search strategies for RSI, MACD, Bollinger Bands, etc.
- **Strategy Comparison**: Compare different trading approaches
- **Research Discovery**: Find relevant academic papers
- **Market Analysis**: Analyze strategies for different market conditions

## 🛠️ Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/arxiv-finance-chatbot.git
cd arxiv-finance-chatbot

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Environment Configuration
Create .env file:
cp .env.example .env

Fill in your API keys:
- OPENAI_API_KEY: Your OpenAI API key
- LLAMA_INDEX_URL: Your LlamaIndex endpoint URL
- LLAMA_INDEX_API_KEY: Your LlamaIndex API key

### 4. Run Application
streamlit run app.py

## 🌐 Deployment
### Streamlit Cloud

1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add environment variables in Streamlit Cloud settings
4. Deploy!

### Heroku
1. Add runtime.txt with Python version
2. Create Procfile:
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
3. Deploy to Heroku

## 📊 Usage Examples
- "Покажи мне стратегии связанные с RSI"
- "Сравни MACD и Bollinger Bands для volatile markets"
- "Найди исследования по algorithmic trading за 2023 год"
- "Анализ momentum стратегий для trending рынка"

## 🔧 Configuration
- Edit config.py to customize:
- Model parameters
- System prompts
- Chat history limits
- API timeouts

## 📝 License
MIT License - see LICENSE file for details.