import streamlit as st
import os
from config import Config, validate_config
from agents.finance_agent import FinanceAnalysisAgent
from utils.streamlit_utils import StreamlitUtils

# Конфигурация страницы
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Основная функция приложения"""
    
    # Заголовок приложения
    st.title("🤖 " + Config.APP_TITLE)
    st.markdown(f"*{Config.APP_DESCRIPTION}*")
    
    # Инициализация утилит
    utils = StreamlitUtils()
    utils.init_session_state()
    
    # Проверка конфигурации
    try:
        validate_config()
    except ValueError as e:
        st.error(f"❌ Ошибка конфигурации: {e}")
        st.info("Убедитесь, что все переменные окружения настроены правильно.")
        st.stop()
    
    # Инициализация агента
    if st.session_state.agent is None:
        with st.spinner("🚀 Инициализация AI-ассистента..."):
            try:
                st.session_state.agent = FinanceAnalysisAgent()
                st.success("✅ AI-ассистент готов к работе!")
            except Exception as e:
                st.error(f"❌ Ошибка инициализации: {e}")
                st.stop()
    
    # Боковая панель
    quick_command = utils.create_sidebar()
    
    # В функции main() добавьте проверку
    if st.button("🔍 Тест подключения к базе знаний"):
        try:
            from utils.llama_client import LlamaIndexClient
            client = LlamaIndexClient()
            result = client.query("test query", top_k=1)
            
            if result.get("error"):
                st.error(f"❌ Ошибка: {result['error']}")
            else:
                st.success("✅ Подключение к базе знаний работает!")
                st.json(result)
        except Exception as e:
            st.error(f"❌ Ошибка подключения: {e}")
    
    # Основной интерфейс чата
    if not st.session_state.messages:
        utils.show_welcome()
    else:
        # Отображение истории сообщений
        for message in st.session_state.messages:
            utils.display_message(message)
    
    # Обработка быстрой команды из sidebar
    if quick_command:
        st.session_state.messages.append({"role": "user", "content": quick_command})
        utils.display_message({"role": "user", "content": quick_command})
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Анализирую..."):
                response = st.session_state.agent.chat(quick_command)
                formatted_response = utils.format_agent_response(response)
                st.markdown(formatted_response)
        
        st.session_state.messages.append({"role": "assistant", "content": formatted_response})
        st.rerun()
    
    # Поле ввода для пользователя
    if prompt := st.chat_input("Введите ваш вопрос..."):
        # Добавление сообщения пользователя
        st.session_state.messages.append({"role": "user", "content": prompt})
        utils.display_message({"role": "user", "content": prompt})
        
        # Генерация ответа
        with st.chat_message("assistant"):
            with st.spinner("🤔 Анализирую исследования..."):
                try:
                    response = st.session_state.agent.chat(prompt)
                    formatted_response = utils.format_agent_response(response)
                    st.markdown(formatted_response)
                except Exception as e:
                    error_msg = f"❌ Произошла ошибка: {str(e)}"
                    st.error(error_msg)
                    formatted_response = error_msg
        
        # Добавление ответа в историю
        st.session_state.messages.append({"role": "assistant", "content": formatted_response})

if __name__ == "__main__":
    main()
