# ui/browser/browser_history.py
from typing import List, Optional
from datetime import datetime


class BrowserHistory:
    """История посещений браузера"""
    
    def __init__(self, max_size: int = 50):
        self.history: List[dict] = []
        self.current_index = -1
        self.max_size = max_size
        
    def add_entry(self, url: str, title: str = ""):
        """Добавить запись в историю"""
        # Если мы не в конце истории, обрезаем ее
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
            
        entry = {
            "url": url,
            "title": title,
            "timestamp": datetime.now().isoformat(),
            "visit_count": 1
        }
        
        # Проверяем, есть ли уже такой URL в истории
        for i, item in enumerate(self.history):
            if item["url"] == url:
                self.history[i]["visit_count"] += 1
                self.history[i]["timestamp"] = entry["timestamp"]
                self.current_index = i
                return
                
        # Добавляем новую запись
        self.history.append(entry)
        self.current_index = len(self.history) - 1
        
        # Ограничиваем размер истории
        if len(self.history) > self.max_size:
            self.history.pop(0)
            self.current_index -= 1
            
    def can_go_back(self) -> bool:
        """Можно ли перейти назад?"""
        return self.current_index > 0
        
    def can_go_forward(self) -> bool:
        """Можно ли перейти вперед?"""
        return self.current_index < len(self.history) - 1
        
    def go_back(self) -> Optional[dict]:
        """Перейти назад в истории"""
        if self.can_go_back():
            self.current_index -= 1
            return self.history[self.current_index]
        return None
        
    def go_forward(self) -> Optional[dict]:
        """Перейти вперед в истории"""
        if self.can_go_forward():
            self.current_index += 1
            return self.history[self.current_index]
        return None
        
    def get_current(self) -> Optional[dict]:
        """Получить текущую запись"""
        if 0 <= self.current_index < len(self.history):
            return self.history[self.current_index]
        return None
        
    def clear(self):
        """Очистить историю"""
        self.history.clear()
        self.current_index = -1
        
    def get_all(self) -> List[dict]:
        """Получить всю историю"""
        return self.history.copy()
        
    def search(self, query: str) -> List[dict]:
        """Поиск в истории"""
        query = query.lower()
        results = []
        
        for entry in self.history:
            if (query in entry["url"].lower() or 
                query in entry.get("title", "").lower()):
                results.append(entry)
                
        return results