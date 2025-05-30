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
    """
    
    if not self.use_llamaindex:
        return f"""
🔍 **Поиск по теме: {topic}** (Тестовый режим)

⚠️ **База знаний не подключена**
Для получения реальных данных из ArXiv статей настройте переменные окружения.
"""
    
    try:
        # Определяем количество источников
        top_k_map = {
            "basic": 10,
            "detailed": 20, 
            "comprehensive": 30
        }
        top_k = top_k_map.get(detail_level, 20)
        
        # Многоэтапный поиск
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
        
        # Обработка источников с external_file_id
        unique_sources = []
        seen_files = set()
        
        for source in all_sources:
            if hasattr(source, 'metadata'):
                # Получаем external_file_id
                file_id = source.metadata.get('external_file_id', 
                         source.metadata.get('file_id', 
                         source.metadata.get('document_id', 'unknown')))
                
                title = source.metadata.get('title', 'Неизвестная статья')
                
                # Убираем дубликаты по file_id
                if file_id not in seen_files and len(title) > 10:
                    unique_sources.append({
                        'title': title,
                        'authors': source.metadata.get('authors', ''),
                        'year': source.metadata.get('year', ''),
                        'file_id': file_id,
                        'metadata': source.metadata  # Сохраняем все метаданные
                    })
                    seen_files.add(file_id)
        
        # Формируем ответ
        combined_info = "\n\n".join(all_results)
        
        response = f"""
📚 **Исследования по теме: {topic.title()}**

## 🔍 Что говорят научные статьи:

{combined_info}

## 📖 Источники из базы знаний ({len(unique_sources)} статей):

"""
        
        # Добавляем источники с external_file_id
        for i, source in enumerate(unique_sources[:15], 1):
            title = source['title']
            authors = source['authors']
            year = source['year']
            file_id = source['file_id']
            
            source_line = f"{i}. **{title}**"
            
            if authors:
                source_line += f"\n   📝 Авторы: {authors}"
            if year:
                source_line += f"\n   📅 Год: {year}"
                
            source_line += f"\n   🆔 **File ID:** `{file_id}`"
            source_line += "\n"
            
            response += f"\n{source_line}"
        
        response += f"\n\n💡 **Всего найдено {len(unique_sources)} уникальных исследований в базе знаний ArXiv**"
        response += f"\n\n📋 **Как использовать File ID:** Используйте указанные File ID для прямого обращения к конкретным статьям в вашей базе данных"
        
        return response
        
    except Exception as e:
        return f"❌ Ошибка при поиске в базе знаний: {str(e)}"
