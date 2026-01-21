# ui/browser/browser_window.py
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTextBrowser, QStatusBar,
                               QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QKeySequence, QShortcut

from .browser_engine import BrowserEngine
from .url_bar import UrlBar
from .browser_view import BrowserView
from simple_translation import translation


class BrowserWindow(QMainWindow):
    """Главное окно встроенного браузера"""
    
    def __init__(self, parent=None, initial_url=None):
        super().__init__(parent)
        
        self.browser_engine = BrowserEngine()
        self.init_ui()
        self.setup_shortcuts()
        
        # Если передан начальный URL, загружаем его
        if initial_url:
            self.load_url(initial_url)
        
        print(f"[BrowserWindow] Браузер инициализирован. Начальный URL: {initial_url}")
        
    def init_ui(self):
        """Инициализация интерфейса"""
        # Настройка окна
        self.setWindowTitle(translation.t("browser.title", "Браузер SIBERIA"))
        self.setGeometry(100, 100, 1000, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной лейаут
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Панель URL
        self.url_bar = UrlBar()
        self.url_bar.url_entered.connect(self.load_url)
        self.url_bar.back_requested.connect(self.go_back)
        self.url_bar.forward_requested.connect(self.go_forward)
        self.url_bar.reload_requested.connect(self.reload_page)
        main_layout.addWidget(self.url_bar)
        
        # Область просмотра
        self.browser_view = BrowserView()
        main_layout.addWidget(self.browser_view, 1)
        
        # Статус бар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(translation.t("browser.ready", "Готов"))
        
        # Подключаем сигналы движка
        self.browser_engine.page_loaded.connect(self.on_page_loaded)
        self.browser_engine.error_occurred.connect(self.on_error_occurred)
        
        # Применяем стили
        self.apply_styles()
        
    def apply_styles(self):
        """Применить стили к окну браузера"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a1a;
                border: 3px solid #00bfff;
                border-radius: 10px;
            }
            QStatusBar {
                background-color: #1a1a2e;
                color: #00ffff;
                font-family: 'Source Code Pro';
                font-size: 11px;
            }
        """)
        
    def setup_shortcuts(self):
        """Настройка горячих клавиш"""
        # Ctrl+L - фокус на адресную строку
        focus_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        focus_shortcut.activated.connect(self.url_bar.set_focus)
        
        # F5 - обновить
        reload_shortcut = QShortcut(QKeySequence("F5"), self)
        reload_shortcut.activated.connect(self.reload_page)
        
        # Ctrl+R - обновить
        reload_shortcut2 = QShortcut(QKeySequence("Ctrl+R"), self)
        reload_shortcut2.activated.connect(self.reload_page)
        
        # Alt+Left - назад
        back_shortcut = QShortcut(QKeySequence("Alt+Left"), self)
        back_shortcut.activated.connect(self.go_back)
        
        # Alt+Right - вперед
        forward_shortcut = QShortcut(QKeySequence("Alt+Right"), self)
        forward_shortcut.activated.connect(self.go_forward)
        
        # Ctrl+W - закрыть
        close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_shortcut.activated.connect(self.close)
        
        # Esc - закрыть
        esc_shortcut = QShortcut(QKeySequence("Escape"), self)
        esc_shortcut.activated.connect(self.close)
        
    def load_url(self, url: str):
        """Загрузить URL"""
        url = url.strip()
        
        # Если URL не содержит протокол, добавляем app.cyb://
        if "://" not in url:
            if "." in url:  # Это похоже на домен
                url = f"app.cyb://{url}"
            else:  # Просто текст
                self.status_bar.showMessage(
                    translation.t("browser.error.invalid_url_format", "Некорректный формат URL"),
                    3000
                )
                return
        
        # Обновляем адресную строку
        self.url_bar.set_url(url)
        
        # Показываем статус загрузки
        self.status_bar.showMessage(
            translation.t("browser.loading", "Загрузка {url}...").format(url=url),
            2000
        )
        
        # Загружаем через движок
        self.browser_engine.navigate(url)
        
    def on_page_loaded(self, url: str, content: str):
        """Обработчик загрузки страницы"""
        # Обновляем заголовок окна
        page_title = self.browser_engine.get_current_page_title(url)
        self.setWindowTitle(f"{page_title} - Браузер SIBERIA")
        
        # Отображаем контент
        self.browser_view.set_content(content)
        
        # Обновляем статус
        self.status_bar.showMessage(
            translation.t("browser.loaded", "Загружено: {url}").format(url=url),
            3000
        )
        
        # Обновляем URL в адресной строке (на случай редиректов)
        self.url_bar.set_url(url)
        
    def on_error_occurred(self, error_message: str):
        """Обработчик ошибки"""
        # Показываем ошибку в статус баре
        self.status_bar.showMessage(error_message, 5000)
        
        # Показываем сообщение об ошибке
        QMessageBox.warning(
            self,
            translation.t("browser.error.title", "Ошибка браузера"),
            error_message
        )
        
    def go_back(self):
        """Перейти назад"""
        previous_url = self.browser_engine.go_back()
        if previous_url:
            self.load_url(previous_url)
            
    def go_forward(self):
        """Перейти вперед"""
        # В этой простой реализации вперед не реализовано
        self.status_bar.showMessage(
            translation.t("browser.no_forward", "История вперед недоступна"),
            2000
        )
        
    def reload_page(self):
        """Обновить текущую страницу"""
        if self.browser_engine.current_url:
            self.load_url(self.browser_engine.current_url)
        else:
            self.status_bar.showMessage(
                translation.t("browser.no_page_to_reload", "Нет страницы для обновления"),
                2000
            )
            
    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        # Можно добавить сохранение истории и т.д.
        print("[BrowserWindow] Браузер закрывается")
        event.accept()