import streamlit as st
from typing import List, Dict
import plotly.express as px
import pandas as pd

class StreamlitUtils:
    """Утилиты для улучшения интерфейса Streamlit"""
    
    @staticmethod
    def init_session_state():
        """Инициализация состояния сессии"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "agent" not in st.session_state:
            st.session_state.agent = None
    
    @staticmethod
    def display_message(message: Dict[str, str]):
        """Отображение сообщения в чате"""
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    @staticmethod
    def create_sidebar():
        """Создание боковой панели с настройками"""
        with st.sidebar:
            st.markdown("## 🎛️ Настройки")
            
            # Информация о системе
            with st.expander("ℹ️ О системе"):
                st.markdown("""
                **ArXiv LlamaIndex Research Assistant** - это агент для анализа
                научных статей по финансам из индекса ламы ArXiv.
                
                **Что может агент:**
                - Поиск торговых стратегий
                - Анализ технических индикаторов  
                - Сравнение подходов
                - Исследование научных работ
                """)
            
            # Быстрые команды
            st.markdown("### 🚀 Быстрые команды")
            
            suggestions = [
                "вилкой в глаз или в жопу раз",
                "куда сам сядеш а куда мать посадиш", 
                "нормально делай нормально будет",
                "искали искали и нашли"
            ]
            
            for suggestion in suggestions:
                if st.button(suggestion, key=f"btn_{suggestion}"):
                    return suggestion
            
            # Очистка истории
            if st.button("🗑️ Очистить историю"):
                st.session_state.messages = []
                if st.session_state.agent:
                    st.session_state.agent.clear_history()
                st.rerun()
            
            # Статистика
            with st.expander("📊 Статистика сессии"):
                msg_count = len(st.session_state.messages)
                st.metric("Сообщений в сессии", msg_count)
        
        return None
    
    @staticmethod
    def show_welcome():
        """Показ приветственного сообщения"""
        st.markdown("""
        ## 👋 Добро пожаловать бедолага!
        
        Я ваш AI-агент Смит для анализа архива. 
        
        ### 💡 Примеры вопросов:
        """)
        
        examples = [
            "Расскажи о волатильности для тиковой ценовой модели со взаимодействием среднего поля",
            "Расскажи о прогнозирования волатильности с помошью ИИ",
            "Расскажи о оптимизации производительности портфеля с помощью кластеризации и оптимизации на основе коэффициента Шарпа",
            "Расскажи о динамической инвестиционной структуре для улучшения управления портфелем на волатильных рынках"
        ]
        
        for example in examples:
            st.markdown(f"- *{example}*")
    
    @staticmethod 
    def display_typing_indicator():
        """Индикатор печатания"""
        with st.chat_message("assistant"):
            with st.empty():
                st.markdown("🙊 Анализирую...")
    
    @staticmethod
    def format_agent_response(response: str) -> str:
        """Форматирование ответа агента"""
        # Добавляем эмодзи для лучшего восприятия
        if "стратег" in response.lower():
            response = "📈 " + response
        elif "исследован" in response.lower():
            response = "🔬 " + response  
        elif "сравнен" in response.lower():
            response = "⚖️ " + response
        elif "ошибка" in response.lower():
            response = "❌ " + response
        
        return response
