# ui/browser/cyb_protocol_handler.py
import re
from typing import Optional
from simple_translation import translation


class CybProtocolHandler:
    """Обработчик протокола app.cyb://"""
    
    @staticmethod
    def parse_cyb_url(url: str) -> Optional[dict]:
        """
        Разобрать URL протокола app.cyb
        
        Args:
            url: URL вида app.cyb://domain/path
        
        Returns:
            Словарь с компонентами URL или None если URL некорректен
        """
        if not url.startswith("app.cyb://"):
            return None
            
        # Удаляем протокол
        url_without_protocol = url[10:]  # "app.cyb://" имеет длину 10
        
        # Разделяем домен и путь
        if "/" in url_without_protocol:
            domain, path = url_without_protocol.split("/", 1)
            path = "/" + path
        else:
            domain = url_without_protocol
            path = "/"
            
        # Валидация домена
        if not domain or "." not in domain:
            return None
            
        return {
            "protocol": "app.cyb",
            "domain": domain,
            "path": path,
            "full_url": url
        }
        
    @staticmethod
    def is_valid_cyb_url(url: str) -> bool:
        """Проверить валидность URL протокола app.cyb"""
        return CybProtocolHandler.parse_cyb_url(url) is not None
        
    @staticmethod
    def get_url_type(url: str) -> str:
        """Определить тип URL"""
        parsed = CybProtocolHandler.parse_cyb_url(url)
        if not parsed:
            return "invalid"
            
        domain = parsed["domain"]
        
        # Определяем тип по домену
        if "market" in domain or "sale" in domain:
            return "marketplace"
        elif "film" in domain or "cinema" in domain:
            return "entertainment"
        elif "career" in domain or "job" in domain:
            return "career"
        elif "horoscope" in domain:
            return "entertainment"
        elif "invest" in domain or "crypto" in domain:
            return "finance"
        elif "security" in domain or "cyber" in domain or "computer" in domain:
            return "security"
        elif "payment" in domain or "bank" in domain:
            return "finance"
        elif "social" in domain or "communication" in domain:
            return "social"
        elif "dating" in domain:
            return "social"
        else:
            return "unknown"
            
    @staticmethod
    def extract_links_from_text(text: str) -> list:
        """Извлечь все ссылки app.cyb из текста"""
        # Регулярное выражение для поиска ссылок app.cyb
        pattern = r'app\.cyb://[^\s<>"\'()]+'
        return re.findall(pattern, text)