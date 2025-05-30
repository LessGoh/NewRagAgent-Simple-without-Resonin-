import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class Config:
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # LlamaIndex
    LLAMA_INDEX_URL = os.getenv("LLAMA_INDEX_URL")
    LLAMA_INDEX_API_KEY = os.getenv("LLAMA_INDEX_API_KEY")
    
    # App settings
    APP_TITLE = os.getenv("APP_TITLE", "ArXiv Finance Research Assistant")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "AI-powered assistant for financial research papers analysis")
    
    # Model settings
    LLM_MODEL = "gpt-4-1106-preview"
    LLM_TEMPERATURE = 0.1
    
    # Chat settings
    MAX_HISTORY = 50
    SYSTEM_PROMPT = """
    Ты эксперт-аналитик по финансовым рынкам и специалист по научным 
    исследованиям в области финансов из ArXiv.
    
    Твоя задача:
    1. Анализировать научные статьи по финансам
    2. Находить торговые стратегии и подходы
    3. Объяснять сложные концепции простым языком
    4. Предоставлять практические рекомендации
    5. Использовать step-by-step reasoning для глубокого анализа
    
    Всегда:
    - Ссылайся на конкретные исследования
    - Указывай ограничения и риски
    - Предлагай дальнейшие шаги для изучения
    - Используй пошаговое рассуждение для сложных вопросов
    - Отвечай на русском языке, но технические термины можешь оставлять на английском
    """

# Валидация конфигурации
def validate_config():
    if not Config.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY не найден в переменных окружения")
    if not Config.LLAMA_INDEX_URL:
        raise ValueError("LLAMA_INDEX_URL не найден в переменных окружения")
    if not Config.LLAMA_INDEX_API_KEY:
        raise ValueError("LLAMA_INDEX_API_KEY не найден в переменных окружения")
