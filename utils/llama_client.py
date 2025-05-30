import requests
import json
from typing import Dict, Any, Optional
import os

class LlamaIndexClient:
    """Клиент для работы с LlamaIndex API"""
    
    def __init__(self):
        self.base_url = os.getenv("LLAMA_INDEX_URL")
        self.api_key = os.getenv("LLAMA_INDEX_API_KEY")
        
        if not self.base_url:
            raise ValueError("LLAMA_INDEX_URL не найден в переменных окружения")
        if not self.api_key:
            raise ValueError("LLAMA_INDEX_API_KEY не найден в переменных окружения")
            
        self.base_url = self.base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def query(self, query: str, top_k: int = 30, similarity_threshold: float = 0.6) -> Dict[str, Any]:
        """Выполнение запроса к LlamaIndex"""
        try:
            payload = {
                "query": query,
                "top_k": top_k
            }
            
            # Попробуйте разные endpoint пути
            endpoints_to_try = [
                f"{self.base_url}/query",
                f"{self.base_url}/chat", 
                f"{self.base_url}/v1/query",
                f"{self.base_url}"
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    response = requests.post(
                        endpoint,
                        headers=self.headers,
                        json=payload,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        return {
                            "response": response.json().get("response", response.text),
                            "source_nodes": response.json().get("source_nodes", []),
                            "endpoint_used": endpoint
                        }
                        
                except requests.exceptions.RequestException:
                    continue
            
            return {
                "error": f"Не удалось подключиться к LlamaIndex API. Проверьте URL: {self.base_url}",
                "response": None,
                "source_nodes": []
            }
            
        except Exception as e:
            return {
                "error": f"Ошибка API запроса: {str(e)}",
                "response": None,
                "source_nodes": []
            }
