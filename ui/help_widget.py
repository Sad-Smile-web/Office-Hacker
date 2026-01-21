# ui/help_widget.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QFrame, QTextBrowser, 
                               QTabWidget, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from simple_translation import translation

class HelpWidget(QWidget):
    back_clicked = Signal()  # Изменено на back_clicked для совместимости
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.translation = translation
        # Подписываемся на смену языка
        translation.on_language_changed(self.update_texts)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Заголовок
        self.title = QLabel(translation.t("help.helping"))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00bfff;
            text-shadow: 0 0 10px #00bfff, 0 0 20px rgba(0, 191, 255, 0.5);
            margin-bottom: 20px;
        """)
        
        # Создаем вкладки
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #00bfff;
                background-color: #0a0a0a;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #002244;
                color: #00bfff;
                padding: 10px 20px;
                border: 1px solid #00bfff;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #004488;
                color: #ffffff;
                border-bottom: none;
            }
            QTabBar::tab:hover {
                background-color: #003366;
            }
        """)
        
        # Вкладка "Основы"
        self.basics_tab = QWidget()
        basics_layout = QVBoxLayout()
        
        self.basics_browser = QTextBrowser()
        self.basics_browser.setOpenExternalLinks(True)
        self.basics_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #0a0a0a;
                border: 1px solid #333;
                border-radius: 5px;
                padding: 15px;
                color: #cccccc;
                font-family: 'Arial', sans-serif;
                font-size: 14px;
            }
            QScrollBar:vertical {
                background: #001122;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #00bfff;
                min-height: 20px;
                border-radius: 6px;
            }
        """)
        basics_layout.addWidget(self.basics_browser)
        self.basics_tab.setLayout(basics_layout)
        
        # Вкладка "Терминал"
        self.terminal_tab = QWidget()
        terminal_layout = QVBoxLayout()
        
        self.terminal_browser = QTextBrowser()
        self.terminal_browser.setStyleSheet(self.basics_browser.styleSheet())
        terminal_layout.addWidget(self.terminal_browser)
        self.terminal_tab.setLayout(terminal_layout)
        
        # Вкладка "Управление"
        self.controls_tab = QWidget()
        controls_layout = QVBoxLayout()
        
        self.controls_browser = QTextBrowser()
        self.controls_browser.setStyleSheet(self.basics_browser.styleSheet())
        controls_layout.addWidget(self.controls_browser)
        self.controls_tab.setLayout(controls_layout)
        
        # Вкладка "Навыки"
        self.skills_tab = QWidget()
        skills_layout = QVBoxLayout()
        
        self.skills_browser = QTextBrowser()
        self.skills_browser.setStyleSheet(self.basics_browser.styleSheet())
        skills_layout.addWidget(self.skills_browser)
        self.skills_tab.setLayout(skills_layout)
        
        # Добавляем вкладки с переведенными заголовками
        self.tabs.addTab(self.basics_tab, translation.t("help.tab_basics"))
        self.tabs.addTab(self.terminal_tab, translation.t("help.tab_terminal"))
        self.tabs.addTab(self.controls_tab, translation.t("help.tab_controls"))
        self.tabs.addTab(self.skills_tab, translation.t("help.tab_skills"))
        
        # Кнопка возврата
        self.back_btn = QPushButton(translation.t("help.back_button"))
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setMinimumHeight(45)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #006600, stop:0.5 #004400, stop:1 #002200);
                color: #00ff00;
                border: 2px solid #00ff00;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                min-height: 45px;
                border-radius: 8px;
                text-align: center;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #008800, stop:0.5 #006600, stop:1 #004400);
                border-color: #ffff00;
                color: #ffff00;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #002200, stop:0.5 #001100, stop:1 #000000);
            }
        """)
        
        layout.addWidget(self.title)
        layout.addWidget(self.tabs, 1)
        layout.addWidget(self.back_btn)
        
        self.setLayout(layout)
        
        # Загружаем тексты после создания всех виджетов
        self.update_texts()
        
    def update_texts(self):
        """Обновляет все тексты при смене языка"""
        # Обновляем заголовок
        self.title.setText(translation.t("help.helping"))
        
        # Обновляем заголовки вкладок
        self.tabs.setTabText(0, translation.t("help.tab_basics"))
        self.tabs.setTabText(1, translation.t("help.tab_terminal"))
        self.tabs.setTabText(2, translation.t("help.tab_controls"))
        self.tabs.setTabText(3, translation.t("help.tab_skills"))
        
        # Обновляем содержимое вкладок
        self.basics_browser.setHtml(translation.t("help.basics_tab"))
        self.terminal_browser.setHtml(translation.t("help.terminal_tab"))
        self.controls_browser.setHtml(translation.t("help.controls_tab"))
        self.skills_browser.setHtml(translation.t("help.skills_tab"))
        
        # Обновляем кнопку
        self.back_btn.setText(translation.t("help.back_button"))
        
    def go_back(self):
        """Вернуться в меню - испускаем сигнал"""
        self.back_clicked.emit()  # Изменено на back_clicked