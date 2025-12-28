# ui/about_widget.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QFrame, QTextBrowser)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDesktopServices
from simple_translation import translation  # Добавляем импорт системы перевода

class AboutWidget(QWidget):
    back_requested = Signal()  # Изменено имя сигнала
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Сохраняем ссылки на виджеты для обновления
        self.title_label = None
        self.version_label = None
        self.text_browser = None
        self.back_btn = None
        
        # Подписываемся на смену языка
        translation.on_language_changed(self.update_translations)
        
        self.init_ui()
        self.update_translations()
        
    def update_translations(self):
        """Обновить все тексты при смене языка"""
        if self.title_label:
            self.title_label.setText(translation.t("about.title", "ОФИСНЫЙ ХАКЕР - Симулятор кибербезопасности"))
        
        if self.version_label:
            self.version_label.setText(translation.t("about.version", "Версия: <b>0.3</b> | Дата сборки: <b>Декабрь 2025</b>"))
        
        if self.text_browser:
            about_html = translation.t("about.html_content", default="""<div style="font-family: 'Arial', sans-serif; line-height: 1.6;">
            <div style="margin: 20px 0; padding: 15px; background: rgba(0, 191, 255, 0.1); border-left: 4px solid #00bfff; border-radius: 3px;">
            <table cellpadding="5">
            <tr>
                <td style="vertical-align: top; padding-right: 10px;">🎮</td>
                <td>
                    <div style="font-size: 16px; font-weight: bold; color: #00bfff; margin-bottom: 5px;">ОПИСАНИЕ</div>
                    <div style="color: #cccccc;">
                        <b>«Офисный Хакер»</b> — это симулятор работы в сфере кибербезопасности. 
                        Вы играете за нового сотрудника компании <b>«СИБИРЬ-СОФТ»</b>, который должен выполнять 
                        ежедневные задания, развивать навыки и продвигаться по карьерной лестнице.
                    </div>
                </td>
            </tr>
            </table>
            </div>
            
            <div style="margin: 20px 0; padding: 15px; background: rgba(255, 215, 0, 0.1); border-left: 4px solid #ffd700; border-radius: 3px;">
            <table cellpadding="5">
            <tr>
                <td style="vertical-align: top; padding-right: 10px;">🌟</td>
                <td>
                    <div style="font-size: 16px; font-weight: bold; color: #ffd700; margin-bottom: 5px;">ОСОБЕННОСТИ</div>
                    <div style="color: #cccccc;">
                        • <span style="color: #00ff00;">Развитие навыков кибербезопасности</span><br>
                        • <span style="color: #00ff00;">Динамическая система заданий</span><br>
                        • <span style="color: #00ff00;">Интерактивное окружение</span><br>
                        • <span style="color: #00ff00;">Система характеристик персонажа</span><br>
                        • <span style="color: #00ff00;">Возможность сохранения прогресса</span>
                    </div>
                </td>
            </tr>
            </table>
            </div>
            
            <div style="margin: 20px 0; padding: 15px; background: rgba(0, 255, 0, 0.1); border-left: 4px solid #00ff00; border-radius: 3px;">
            <table cellpadding="5">
            <tr>
                <td style="vertical-align: top; padding-right: 10px;">👥</td>
                <td>
                    <div style="font-size: 16px; font-weight: bold; color: #00ff00; margin-bottom: 5px;">РАЗРАБОТЧИКИ</div>
                    <div style="color: #cccccc;">
                        • <span style="color: #00bfff;">Программирование:</span> Sad_Smile<br>
                        • <span style="color: #00bfff;">Дизайн:</span> Sad_Smile<br>
                        • <span style="color: #00bfff;">Тестирование:</span> Sad_Smile
                    </div>
                </td>
            </tr>
            </table>
            </div>
            
            <div style="margin: 20px 0; padding: 15px; background: rgba(255, 0, 0, 0.1); border-left: 4px solid #ff5555; border-radius: 3px;">
            <table cellpadding="5">
            <tr>
                <td style="vertical-align: top; padding-right: 10px;">📞</td>
                <td>
                    <div style="font-size: 16px; font-weight: bold; color: #ff5555; margin-bottom: 5px;">КОНТАКТЫ</div>
                    <div style="color: #cccccc;">
                        • <span style="color: #00ffff;">Email:</span> 
                          <a href="mailto:sapportsadsmile@gmail.com" 
                             style="color: #00bfff; text-decoration: none;">
                             sapportsadsmile@gmail.com</a><br>
                        • <span style="color: #00ffff;">Сайт:</span> 
                          <a href="https://sikorsky-support-center.netlify.app/" 
                             style="color: #00bfff; text-decoration: none;">
                             https://sikorsky-support-center.netlify.app/</a><br>
                    </div>
                </td>
            </tr>
            </table>
            </div>
            
            <div style="margin: 20px 0; padding: 15px; background: rgba(255, 255, 0, 0.1); border-left: 4px solid #ffff00; border-radius: 3px;">
            <table cellpadding="5">
            <tr>
                <td style="vertical-align: top; padding-right: 10px;">📄</td>
                <td>
                    <div style="font-size: 16px; font-weight: bold; color: #ffff00; margin-bottom: 5px;">ЛИЦЕНЗИЯ</div>
                    <div style="color: #cccccc;">
                        Данная программа распространяется на условиях лицензии 
                        <span style="color: #ff8800; font-weight: bold;">MIT</span>.<br><br>
                        
                        <span style="font-size: 12px; color: #888888;">
                        Разрешено: коммерческое использование, модификация, распространение, частное использование.<br>
                        Требуется: указание авторства и лицензии.<br>
                        Запрещено: ответственность и гарантии.
                        </span>
                    </div>
                </td>
            </tr>
            </table>
            </div>
            
            <div style="margin-top: 30px; padding: 15px; background: rgba(0, 0, 0, 0.3); border: 1px solid #333; border-radius: 5px; text-align: center;">
                <div style="color: #00bfff; font-size: 18px; font-weight: bold; margin-bottom: 5px;">
                    SIKORSKY'S INCORPORATED
                </div>
                <div style="color: #888888; font-size: 12px;">
                    © 2025 Sikorsky's Incorporated. Все права защищены.<br>
                    <span style="color: #666666;">Siberia-Soft Division</span>
                </div>
            </div>
            
            </div>""")
            self.text_browser.setHtml(about_html)
        
        if self.back_btn:
            self.back_btn.setText(translation.t("about.back_button", "🔙 НАЗАД В МЕНЮ"))
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Заголовок
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00bfff;
            text-shadow: 0 0 10px #00bfff, 0 0 20px rgba(0, 191, 255, 0.5);
            margin-bottom: 10px;
        """)
        
        # Версия с иконкой
        version_frame = QFrame()
        version_layout = QHBoxLayout()
        
        version_icon = QLabel("📦")
        version_icon.setStyleSheet("font-size: 16px;")
        
        self.version_label = QLabel()
        self.version_label.setStyleSheet("font-size: 14px; color: #a0a0a0;")
        
        version_layout.addWidget(version_icon)
        version_layout.addWidget(self.version_label)
        version_layout.addStretch()
        version_frame.setLayout(version_layout)
        
        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #000000, stop:0.3 #00bfff, stop:0.7 #00bfff, stop:1 #000000);
            height: 2px;
            margin: 10px 0;
        """)
        
        # Используем QTextBrowser
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)  # Разрешаем открытие внешних ссылок
        
        # Настраиваем стили
        self.text_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #0a0a0a;
                border: 2px solid #333;
                border-radius: 10px;
                padding: 10px;
                selection-background-color: #003366;
                color: #cccccc;
                font-family: 'Arial', sans-serif;
            }
            QTextBrowser a {
                color: #00bfff;
                text-decoration: none;
            }
            QTextBrowser a:hover {
                color: #00ffff;
                text-decoration: underline;
            }
            QScrollBar:vertical {
                background: #001100;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #00aa00;
                min-height: 20px;
                border-radius: 6px;
            }
        """)
        
        # Устанавливаем высоту текстового поля
        self.text_browser.setMinimumHeight(500)
        
        # Кнопка возврата с иконкой
        self.back_btn = QPushButton()
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
            QPushButton:focus {
                border: 2px solid #00ffff;
                outline: none;
            }
        """)
        
        layout.addWidget(self.title_label)
        layout.addWidget(version_frame)
        layout.addWidget(separator)
        layout.addWidget(self.text_browser, 1)
        layout.addWidget(self.back_btn)
        
        self.setLayout(layout)
        
    def go_back(self):
        """Вернуться в меню - испускаем сигнал"""
        self.back_requested.emit()