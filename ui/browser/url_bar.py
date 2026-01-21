# ui/browser/url_bar.py
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QLineEdit, 
                               QPushButton, QStyle)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from simple_translation import translation


class UrlBar(QWidget):
    """Виджет адресной строки браузера"""
    
    url_entered = Signal(str)
    back_requested = Signal()
    forward_requested = Signal()
    reload_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Кнопка "Назад"
        self.back_btn = QPushButton("←")
        self.back_btn.setToolTip(translation.t("browser.back", "Назад"))
        self.back_btn.setFixedSize(30, 30)
        
        # Кнопка "Вперед"
        self.forward_btn = QPushButton("→")
        self.forward_btn.setToolTip(translation.t("browser.forward", "Вперед"))
        self.forward_btn.setFixedSize(30, 30)
        
        # Кнопка "Обновить"
        self.reload_btn = QPushButton("↻")
        self.reload_btn.setToolTip(translation.t("browser.reload", "Обновить"))
        self.reload_btn.setFixedSize(30, 30)
        
        # Поле ввода URL
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText(
            translation.t("browser.url_placeholder", "Введите URL (app.cyb://...)")
        )
        self.url_edit.returnPressed.connect(self.on_url_entered)
        
        # Кнопка "Перейти"
        self.go_btn = QPushButton("→")
        self.go_btn.setToolTip(translation.t("browser.go", "Перейти"))
        self.go_btn.setFixedSize(40, 30)
        self.go_btn.clicked.connect(self.on_url_entered)
        
        # Добавляем виджеты в лейаут
        layout.addWidget(self.back_btn)
        layout.addWidget(self.forward_btn)
        layout.addWidget(self.reload_btn)
        layout.addWidget(self.url_edit, 1)
        layout.addWidget(self.go_btn)
        
        # Применяем стили
        self.apply_styles()
        
    def apply_styles(self):
        """Применить стили"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
            }
            QPushButton {
                background-color: #2a2a3e;
                color: #cccccc;
                border: 2px solid #00bfff;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3a3a4e;
                border-color: #00ffff;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #1a1a2e;
            }
            QPushButton:disabled {
                background-color: #1a1a1a;
                border-color: #555555;
                color: #777777;
            }
            QLineEdit {
                background-color: #000000;
                color: #00ffff;
                border: 2px solid #0088cc;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Source Code Pro';
                font-size: 13px;
                selection-background-color: #0088cc;
            }
            QLineEdit:focus {
                border: 2px solid #00ffff;
                background-color: #001122;
            }
        """)
        
    def setup_connections(self):
        """Настройка соединений"""
        self.back_btn.clicked.connect(self.back_requested.emit)
        self.forward_btn.clicked.connect(self.forward_requested.emit)
        self.reload_btn.clicked.connect(self.reload_requested.emit)
        
    def on_url_entered(self):
        """Обработчик ввода URL"""
        url = self.url_edit.text().strip()
        if url:
            self.url_entered.emit(url)
            
    def set_url(self, url: str):
        """Установить URL в адресную строку"""
        self.url_edit.setText(url)
        
    def get_url(self) -> str:
        """Получить текущий URL из адресной строки"""
        return self.url_edit.text().strip()
        
    def set_focus(self):
        """Установить фокус на адресную строку"""
        self.url_edit.setFocus()
        self.url_edit.selectAll()
        
    def clear(self):
        """Очистить адресную строку"""
        self.url_edit.clear()