from llama_index.llms.openai import OpenAI
import os
from agents.tools import ResearchTools
from typing import List, Dict, Any

class SimpleResearchAgent:
    """Простой агент для поиска и объяснения научных статей"""
    
    def __init__(self):
        self.tools = ResearchTools()
        self.chat_history = []
        
        # Проверяем OpenAI ключ
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.llm = OpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.1,
                api_key=openai_key
            )
            self.use_llm = True
        else:
            self.use_llm = False
            print("❌ OpenAI API ключ не найден")
    
    def chat(self, message: str) -> str:
        """Основной метод для исследовательских запросов"""
        
        try:
            # Добавляем в историю
            self.chat_history.append({"role": "user", "content": message})
            
            # Ищем в базе знаний
            search_result = self.tools.search_research(message, detail_level="detailed")
            
            # Если есть LLM, улучшаем ответ
            if self.use_llm and "❌" not in search_result and "Тестовый режим" not in search_result:
                
                enhanced_prompt = f"""
Ты эксперт по финансовым исследованиям. Твоя задача - объяснить сложную научную информацию простым и понятным языком, сохраняя все важные детали.

ИСХОДНЫЙ ЗАПРОС ПОЛЬЗОВАТЕЛЯ: {message}

ИНФОРМАЦИЯ ИЗ НАУЧНЫХ СТАТЕЙ:
{search_result}

ЗАДАЧА:
1. Объясни ключевые концепции простым языком
2. Сохрани все важные детали, формулы, методы
3. Покажи практическое применение
4. Структурируй информацию логично
5. Используй примеры для сложных понятий

Отвечай подробно, но доступно. Не теряй научную точность, но делай информацию понятной для практического применения.
"""
                
                try:
                    enhanced_response = self.llm.complete(enhanced_prompt)
                    final_response = str(enhanced_response)
                except Exception as e:
                    final_response = f"📚 {search_result}\n\n⚠️ Улучшение ответа недоступно: {str(e)}"
            else:
                final_response = search_result
            
            # Добавляем в историю
            self.chat_history.append({"role": "assistant", "content": final_response})
            
            # Ограничиваем историю
            if len(self.chat_history) > 20:
                self.chat_history = self.chat_history[-20:]
            
            return final_response
            
        except Exception as e:
            error_message = f"❌ Произошла ошибка: {str(e)}"
            self.chat_history.append({"role": "assistant", "content": error_message})
            return error_message
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Получение истории чата"""
        return self.chat_history
    
    def clear_history(self):
        """Очистка истории чата"""
        self.chat_history = []
        
    def get_suggestions(self) -> List[str]:
        """Предложения тем для исследования"""
        return [
            "Стохастическое приближение волатильности для тиковой ценовой модели",
            "Машинное обучение в прогнозировании финансовых рынков",
            "Алгоритмы высокочастотной торговли и микроструктура рынка",
            "Behavioral finance и поведенческие аномалии рынка",
            "Risk management и современные подходы к управлению рисками",
            "Портфельная оптимизация с использованием альтернативных данных",
            "Криптовалютные рынки и их математические модели",
            "Эконометрический анализ временных рядов в финансах"
        ]
