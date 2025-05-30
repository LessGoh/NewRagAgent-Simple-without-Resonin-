from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from agents.tools import FinanceTools
from config import Config
from typing import List, Dict, Any

class FinanceAnalysisAgent:
    """ReAct агент для анализа финансовых исследований"""
    
    def __init__(self):
        self.tools = FinanceTools()
        self.agent = self._create_agent()
        self.chat_history = []
    
    def _create_agent(self) -> ReActAgent:
        """Создание ReAct агента с финансовыми инструментами"""
        
        # Инициализация LLM
        llm = OpenAI(
            model=Config.LLM_MODEL,
            temperature=Config.LLM_TEMPERATURE,
            api_key=Config.OPENAI_API_KEY
        )
        
        # Получение инструментов
        tools = self.tools.get_tools()
        
        # Создание агента
        agent = ReActAgent.from_tools(
            tools=tools,
            llm=llm,
            verbose=True,
            system_prompt=Config.SYSTEM_PROMPT,
            max_iterations=10,
            react_chat_formatter=None,
            memory=None  # Будем управлять историей вручную
        )
        
        return agent
    
    def chat(self, message: str) -> str:
        """
        Основной метод для общения с ботом
        
        Args:
            message: Сообщение пользователя
            
        Returns:
            Ответ агента
        """
        try:
            # Добавляем сообщение в историю
            self.chat_history.append({"role": "user", "content": message})
            
            # Получаем ответ от агента
            response = self.agent.chat(message)
            
            # Добавляем ответ в историю
            self.chat_history.append({"role": "assistant", "content": str(response)})
            
            # Ограничиваем размер истории
            if len(self.chat_history) > Config.MAX_HISTORY:
                self.chat_history = self.chat_history[-Config.MAX_HISTORY:]
            
            return str(response)
            
        except Exception as e:
            error_message = f"Извините, произошла ошибка: {str(e)}"
            self.chat_history.append({"role": "assistant", "content": error_message})
            return error_message
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Получение истории чата"""
        return self.chat_history
    
    def clear_history(self):
        """Очистка истории чата"""
        self.chat_history = []
        
    def get_suggestions(self) -> List[str]:
        """Получение предложений для начала разговора"""
        return [
            "Покажи мне стратегии связанные с RSI для дневной торговли",
            "Сравни эффективность MACD и RSI в трендовых рынках", 
            "Какие стратегии подходят для волатильного рынка?",
            "Найди исследования по behavioral finance за последние 3 года",
            "Расскажи о стратегиях mean reversion для криптовалют",
            "Какие алгоритмические стратегии показывают лучшие результаты?",
            "Анализ стратегий для sideways рынка с техническим подходом",
            "Сравни momentum и contrarian стратегии"
        ]
