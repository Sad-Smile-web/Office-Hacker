# ui/browser/__init__.py
"""
Модуль встроенного браузера для приложения SIBERIA-SOFTWARE

Компоненты:
- BrowserWindow: Главное окно браузера
- BrowserEngine: Движок обработки URL
- BrowserView: Виджет отображения контента
- UrlBar: Адресная строка с навигацией
- MockWebsites: Генератор вымышленных сайтов
- CybProtocolHandler: Обработчик протокола app.cyb://
- BrowserHistory: История посещений
"""

from .browser_window import BrowserWindow
from .browser_engine import BrowserEngine
from .browser_view import BrowserView
from .url_bar import UrlBar
from .mock_websites import MockWebsites
from .cyb_protocol_handler import CybProtocolHandler
from .browser_history import BrowserHistory

__all__ = [
    'BrowserWindow',
    'BrowserEngine', 
    'BrowserView',
    'UrlBar',
    'MockWebsites',
    'CybProtocolHandler',
    'BrowserHistory'
]