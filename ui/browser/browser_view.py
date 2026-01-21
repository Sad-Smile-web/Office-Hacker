# ui/browser/browser_view.py
from PySide6.QtWidgets import QTextBrowser
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
import re


class BrowserView(QTextBrowser):
    """Виджет для отображения веб-контента"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setOpenLinks(False)  # Отключаем стандартную обработку ссылок
        self.setOpenExternalLinks(False)
        
        # Применяем стили
        self.setStyleSheet("""
            QTextBrowser {
                background-color: #000000;
                color: #ffffff;
                border: none;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QScrollBar:vertical {
                background: #1a1a2e;
                width: 14px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: #00bfff;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background: #00ffff;
            }
        """)
        
    def setup_connections(self):
        """Настройка соединений"""
        # Перехватываем клики по ссылкам
        self.anchorClicked.connect(self.on_anchor_clicked)
        
    def set_content(self, html_content: str):
        """Установить HTML контент"""
        # Добавляем базовый HTML если его нет
        if not html_content.strip().startswith("<!DOCTYPE"):
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background: #000000; color: #ffffff; padding: 20px; }}
                    a {{ color: #00ffff; text-decoration: none; }}
                    a:hover {{ color: #ffff00; text-decoration: underline; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
        
        self.setHtml(html_content)
        
    def on_anchor_clicked(self, url: QUrl):
        """Обработчик клика по ссылке"""
        url_str = url.toString()
        
        # Если ссылка начинается с app.cyb://, обрабатываем сами
        if url_str.startswith("app.cyb://"):
            # Отправляем сигнал родителю (BrowserWindow)
            if hasattr(self.parent(), 'load_url'):
                self.parent().load_url(url_str)
        else:
            # Для других ссылок используем стандартную обработку
            QDesktopServices.openUrl(url)
            
    def contextMenuEvent(self, event):
        """Переопределяем контекстное меню"""
        # Можно кастомизировать контекстное меню
        # Пока используем стандартное
        super().contextMenuEvent(event)