from typing import Optional
import os

# Проверяем, доступен ли LlamaIndex клиент
try:
    from utils.llama_client import LlamaIndexClient
    LLAMA_AVAILABLE = True
except ImportError:
    LLAMA_AVAILABLE = False

class ResearchTools:
    """Простые инструменты для поиска научных статей"""
    
    def __init__(self):
        if LLAMA_AVAILABLE and os.getenv("LLAMA_INDEX_URL"):
            try:
                self.llama_client = LlamaIndexClient()
                self.use_llamaindex = True
                print("✅ LlamaIndex подключен успешно")
            except Exception as e:
                print(f"❌ Ошибка подключения к LlamaIndex: {e}")
                self.use_llamaindex = False
        else:
            print("❌ LlamaIndex не доступен")
            self.use_llamaindex = False
    
    def search_research(self, topic: str, detail_level: str = "detailed") -> str:
        """
        Поиск научных исследований по любой финансовой теме.
        
        Args:
            topic: Тема исследования (например: "стохастическая волатильность", "машинное обучение в трейдинге")
            detail_level: Уровень детализации ("basic", "detailed", "comprehensive")
        
        Returns:
            Детальная информация из научных статей простым языком
        """
        
        if not self.use_llamaindex:
            return f"""
🔍 **Поиск по теме: {topic}** (Тестовый режим)

⚠️ **База знаний не подключена**
Для получения реальных данных из ArXiv статей настройте переменные окружения.

Для тестирования вашего вопроса подключите базу знаний с финансовыми статьями.
"""
        
        try:
            # Определяем количество источников в зависимости от уровня детализации
            top_k_map = {
                "basic": 10,
                "detailed": 20, 
                "comprehensive": 30
            }
            top_k = top_k_map.get(detail_level, 20)
            
            # Многоэтапный поиск для максимального покрытия
            queries = [
                f"{topic} исследование анализ",
                f"{topic} методология подход",
                f"{topic} результаты выводы практика",
                f"{topic} модель формула алгоритм",
                f"{topic} применение реализация"
            ]
            
            all_results = []
            all_sources = []
            
            for query in queries:
                result = self.llama_client.query(query, top_k=top_k//len(queries) + 5)
                
                if result.get("response") and not result.get("error"):
                    all_results.append(result["response"])
                    all_sources.extend(result.get("source_nodes", []))
            
            if not all_results:
                return f"❌ По теме '{topic}' информация в базе знаний не найдена. Попробуйте другие ключевые слова."
            
            # Убираем дубликаты источников
            unique_sources = []
            seen_titles = set()
            for source in all_sources:
                if hasattr(source, 'metadata'):
                    title = source.metadata.get('title', '')
                    if title and title not in seen_titles and len(title) > 10:
                        unique_sources.append(source)
                        seen_titles.add(title)
            
            # Формируем ответ
            combined_info = "\n\n".join(all_results)
            
            response = f"""
📚 **Исследования по теме: {topic.title()}**

## 🔍 Что говорят научные статьи:

{combined_info}

## 📖 Источники из базы знаний ({len(unique_sources)} статей):
"""
            
            for i, source in enumerate(unique_sources[:15], 1):
                title = source.metadata.get('title', 'Неизвестная статья')
                authors = source.metadata.get('authors', '')
                year = source.metadata.get('year', '')
                
                source_line = f"{i}. **{title}**"
                if authors:
                    source_line += f" - {authors}"
                if year:
                    source_line += f" ({year})"
                    
                response += f"\n{source_line}"
            
            response += f"\n\n💡 **Всего найдено {len(unique_sources)} релевантных исследований в базе знаний ArXiv**"
            
            return response
            
        except Exception as e:
            return f"❌ Ошибка при поиске в базе знаний: {str(e)}"
    
    def get_tools(self):
        """Возвращает единственный инструмент для поиска"""
        try:
            from llama_index.core.tools import FunctionTool
            return [FunctionTool.from_defaults(self.search_research)]
        except Exception as e:
            print(f"Ошибка создания инструментов: {e}")
            return []
