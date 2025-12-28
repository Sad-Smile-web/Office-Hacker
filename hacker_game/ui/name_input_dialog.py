# ui/name_input_dialog.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                               QLabel, QLineEdit, QPushButton, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor, QPalette

from simple_translation import translation


class NameInputDialog(QDialog):
    """Диалог для ввода имени сотрудника"""
    
    names_accepted = Signal(str, str)  # Сигнал с именем и фамилией
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translation.t("game.input_name_title"))
        self.setModal(True)
        self.setFixedSize(500, 350)
        
        self.setup_ui()
        self.setup_styles()
        
        # Подключаем переводы
        translation.on_language_changed(self.retranslate_ui)
    
    def setup_ui(self):
        """Настройка интерфейса"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 20)
        main_layout.setSpacing(20)
        
        # Заголовок
        title_label = QLabel(translation.t("game.input_name_title"))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #00bfff;
            text-shadow: 0 0 10px #00bfff;
            padding: 10px;
        """)
        
        # Инструкция
        instruction_label = QLabel(translation.t("game.input_name_instruction"))
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setWordWrap(True)
        instruction_label.setStyleSheet("""
            font-size: 14px;
            color: #a0a0a0;
            padding: 10px;
            background-color: rgba(16, 16, 16, 0.5);
            border-radius: 5px;
        """)
        
        # Поля ввода
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(32, 32, 48, 0.8);
                border: 1px solid #00bfff;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(15)
        
        # Имя
        self.first_name_label = QLabel(translation.t("game.input_first_name"))
        self.first_name_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #00ffff;
        """)
        
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Иван")
        self.first_name_input.setMaxLength(20)
        self.first_name_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(16, 16, 32, 0.9);
                border: 2px solid #00bfff;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: #ffffff;
                selection-background-color: #00bfff;
            }
            QLineEdit:focus {
                border-color: #00ffff;
                background-color: rgba(16, 16, 32, 1);
            }
            QLineEdit:hover {
                border-color: #00ffff;
            }
        """)
        
        # Фамилия
        self.last_name_label = QLabel(translation.t("game.input_last_name"))
        self.last_name_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #00ffff;
        """)
        
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Иванов")
        self.last_name_input.setMaxLength(20)
        self.last_name_input.setStyleSheet(self.first_name_input.styleSheet())
        
        # Подсказка
        hint_label = QLabel(translation.t("game.input_name_hint"))
        hint_label.setWordWrap(True)
        hint_label.setStyleSheet("""
            font-size: 12px;
            color: #808080;
            font-style: italic;
            margin-top: 5px;
        """)
        
        input_layout.addWidget(self.first_name_label)
        input_layout.addWidget(self.first_name_input)
        input_layout.addWidget(self.last_name_label)
        input_layout.addWidget(self.last_name_input)
        input_layout.addWidget(hint_label)
        
        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        self.ok_button = QPushButton(translation.t("common.ok"))
        self.ok_button.setFixedHeight(50)
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: #0066aa;
                color: #ffffff;
                border: 2px solid #00bfff;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0088cc;
                border-color: #00ffff;
            }
            QPushButton:pressed {
                background-color: #004488;
            }
            QPushButton:disabled {
                background-color: #333344;
                border-color: #666677;
                color: #888888;
            }
        """)
        self.ok_button.clicked.connect(self.accept_input)
        
        self.cancel_button = QPushButton(translation.t("common.cancel"))
        self.cancel_button.setFixedHeight(50)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #aa3300;
                color: #ffffff;
                border: 2px solid #ff6633;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #cc5500;
                border-color: #ff8844;
            }
            QPushButton:pressed {
                background-color: #882200;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        
        # Добавляем всё в основной layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(instruction_label)
        main_layout.addWidget(input_frame)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # Устанавливаем фокус на первое поле
        self.first_name_input.setFocus()
        
        # Подключаем проверку ввода
        self.first_name_input.textChanged.connect(self.validate_input)
        self.last_name_input.textChanged.connect(self.validate_input)
        
        # Изначально кнопка OK отключена
        self.ok_button.setEnabled(False)
    
    def setup_styles(self):
        """Настройка стилей диалога"""
        self.setStyleSheet("""
            QDialog {
                background-color: #0a0a14;
                border: 2px solid #00bfff;
                border-radius: 10px;
            }
        """)
        
        # Устанавливаем тень окна
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        
    def validate_input(self):
        """Проверка введенных данных"""
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        
        # Оба поля должны быть заполнены
        is_valid = bool(first_name and last_name)
        
        # Валидация имени: только буквы и дефисы
        if first_name:
            import re
            if not re.match(r'^[A-Za-zА-Яа-яЁё\- ]+$', first_name):
                self.first_name_input.setStyleSheet("""
                    QLineEdit {
                        background-color: rgba(16, 16, 32, 0.9);
                        border: 2px solid #ff0000;
                        border-radius: 5px;
                        padding: 10px;
                        font-size: 16px;
                        color: #ff6666;
                    }
                """)
                is_valid = False
            else:
                self.first_name_input.setStyleSheet("""
                    QLineEdit {
                        background-color: rgba(16, 16, 32, 0.9);
                        border: 2px solid #00bfff;
                        border-radius: 5px;
                        padding: 10px;
                        font-size: 16px;
                        color: #ffffff;
                    }
                """)
        
        if last_name:
            import re
            if not re.match(r'^[A-Za-zА-Яа-яЁё\- ]+$', last_name):
                self.last_name_input.setStyleSheet("""
                    QLineEdit {
                        background-color: rgba(16, 16, 32, 0.9);
                        border: 2px solid #ff0000;
                        border-radius: 5px;
                        padding: 10px;
                        font-size: 16px;
                        color: #ff6666;
                    }
                """)
                is_valid = False
            else:
                self.last_name_input.setStyleSheet(self.first_name_input.styleSheet())
        
        self.ok_button.setEnabled(is_valid)
        return is_valid
    
    def accept_input(self):
        """Принять введенные данные"""
        if self.validate_input():
            self.names_accepted.emit(
                self.first_name_input.text().strip(),
                self.last_name_input.text().strip()
            )
            self.accept()
    
    def get_names(self):
        """Получить введенные имя и фамилию"""
        return (
            self.first_name_input.text().strip(),
            self.last_name_input.text().strip()
        )
    
    def retranslate_ui(self):
        """Обновить тексты при смене языка"""
        self.setWindowTitle(translation.t("game.input_name_title"))
        
        title = self.findChild(QLabel)
        if title and hasattr(title, 'setText'):
            title.setText(translation.t("game.input_name_title"))
        
        instruction = self.findChildren(QLabel)[1]
        if instruction:
            instruction.setText(translation.t("game.input_name_instruction"))
        
        self.first_name_label.setText(translation.t("game.input_first_name"))
        self.last_name_label.setText(translation.t("game.input_last_name"))
        
        hint = self.findChildren(QLabel)[-1]
        if hint:
            hint.setText(translation.t("game.input_name_hint"))
        
        self.ok_button.setText(translation.t("common.ok"))
        self.cancel_button.setText(translation.t("common.cancel"))