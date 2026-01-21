# ui/browser/browser_engine.py
import re
from typing import Dict, Optional, Tuple
from PySide6.QtCore import QObject, Signal
from simple_translation import translation


class BrowserEngine(QObject):
    """Движок браузера для обработки вымышленных URL"""
    
    page_loaded = Signal(str, str)  # url, content
    error_occurred = Signal(str)  # error_message
    
    def __init__(self):
        super().__init__()
        self.current_url = ""
        self.history = []
        
    def parse_url(self, url: str) -> Tuple[str, str, str]:
        """
        Разобрать URL на компоненты
        
        Args:
            url: Полный URL (например, app.cyb://market.sale/fresh-products)
        
        Returns:
            Tuple (protocol, domain, path)
        """
        if not url:
            return ("", "", "")
            
        # Удаляем пробелы
        url = url.strip()
        
        # Проверяем протокол
        if "://" not in url:
            return ("", "", url)
            
        protocol, rest = url.split("://", 1)
        
        # Разделяем домен и путь
        if "/" in rest:
            domain, path = rest.split("/", 1)
            path = "/" + path
        else:
            domain = rest
            path = "/"
            
        return (protocol, domain, path)
        
    def is_valid_url(self, url: str) -> bool:
        """Проверить валидность URL"""
        if not url:
            return False
            
        url = url.strip()
        
        # Простой URL должен содержать протокол и домен
        if "://" not in url:
            return False
            
        protocol, rest = url.split("://", 1)
        
        # Поддерживаем только протокол app.cyb
        if protocol != "app.cyb":
            return False
            
        # Должен быть домен
        if not rest or "." not in rest:
            return False
            
        return True
        
    def navigate(self, url: str):
        """Перейти по URL"""
        if not self.is_valid_url(url):
            self.error_occurred.emit(
                translation.t("browser.error.invalid_url", "Некорректный URL: {url}").format(url=url)
            )
            return
            
        try:
            self.current_url = url
            self.history.append(url)
            
            # Генерируем контент для URL
            content = self.generate_content(url)
            self.page_loaded.emit(url, content)
            
        except Exception as e:
            self.error_occurred.emit(
                translation.t("browser.error.load_failed", "Ошибка загрузки страницы: {error}").format(error=str(e))
            )
            
    def generate_content(self, url: str) -> str:
        """Сгенерировать контент для указанного URL"""
        protocol, domain, path = self.parse_url(url)
        
        # Загружаем генератор сайтов
        from .mock_websites import MockWebsites
        
        # Получаем контент
        content_generator = MockWebsites()
        content = content_generator.get_website_content(domain, path)
        
        return content
        
    def go_back(self) -> Optional[str]:
        """Вернуться назад в истории"""
        if len(self.history) > 1:
            self.history.pop()  # Убираем текущий URL
            previous_url = self.history.pop()  # Берем предыдущий
            return previous_url
        return None
        
    def get_current_page_title(self, url: str) -> str:
        """Получить заголовок страницы по URL"""
        protocol, domain, path = self.parse_url(url)
        
        # Заголовки для популярных сайтов
        titles = {
            "market.sale": "МегаМаркет - Скидки 50%",
            "film.distribution.sale": "Онлайн-Кинотеатр Premium",
            "career.consultant": "Карьера Pro - Вакансии",
            "horoscope": "Астрологический Портал",
            "investor.deposits.profit": "Крипто-Инвестиции",
            "computer.wizard": "КиберБезопасность Pro",
            "payments.security": "Безопасность Платежей",
            "SIBERIA.communication": "Социальная Сеть SIBERIA"
        }
        
        # Ищем заголовок по домену
        for key, title in titles.items():
            if key in domain or key in url:
                return title
                
        # Если не нашли, используем домен
        return domain
        
    def get_favicon(self, url: str) -> str:
        """Получить иконку для сайта (символ)"""
        protocol, domain, path = self.parse_url(url)
        
        # Иконки для разных типов сайтов
        if "market" in domain or "sale" in domain:
            return "🛒"
        elif "film" in domain or "cinema" in domain:
            return "🎬"
        elif "career" in domain or "job" in domain:
            return "💼"
        elif "horoscope" in domain:
            return "🔮"
        elif "invest" in domain or "crypto" in domain:
            return "💰"
        elif "security" in domain or "cyber" in domain:
            return "🔒"
        elif "social" in domain or "communication" in domain:
            return "👥"
        elif "bank" in domain or "payment" in domain:
            return "🏦"
        elif "dating" in domain:
            return "❤️"
            
        return "🌐"