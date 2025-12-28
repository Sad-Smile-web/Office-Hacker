# ui/skills_widget.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QFrame, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor, QLinearGradient


class SkillsWidget(QWidget):
    """Виджет детального отображения навыков"""
    back_to_info = Signal()
    
    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self.game_state = game_state
        self.skill_widgets = {}
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Заголовок
        header = QLabel("🎯 НАВЫКИ СОТРУДНИКА")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #00bfff;
            padding: 10px;
            background-color: rgba(0, 34, 68, 0.7);
            border-radius: 8px;
            margin-bottom: 10px;
        """)
        
        # Кнопка назад
        back_button = QPushButton("← НАЗАД К ИНФОРМАЦИИ")
        back_button.clicked.connect(self.back_to_info.emit)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(42, 42, 62, 0.9);
                color: #cccccc;
                border: 1px solid #00bfff;
                padding: 8px;
                font-weight: bold;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(0, 100, 200, 0.8);
                border-color: #00ffff;
                color: #ffffff;
                border-width: 2px;
            }
            QPushButton:pressed {
                background-color: rgba(0, 50, 100, 0.9);
            }
        """)
        
        # Статистика навыков
        stats_label = QLabel(f"Всего навыков: {len(self.game_state.skills)} | Средний уровень: {self.get_average_level():.1f}/10")
        stats_label.setStyleSheet("""
            color: #cccccc;
            font-size: 13px;
            padding: 5px;
            background-color: rgba(30, 30, 50, 0.5);
            border-radius: 5px;
        """)
        
        # Создаем скроллируемую область для навыков
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #222244;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #00bfff;
                min-height: 30px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #00ffff;
            }
        """)
        
        # Контейнер для навыков
        skills_container = QWidget()
        self.skills_layout = QVBoxLayout()
        self.skills_layout.setSpacing(15)
        self.skills_layout.setContentsMargins(5, 5, 5, 5)
        
        skills_container.setLayout(self.skills_layout)
        scroll_area.setWidget(skills_container)
        
        layout.addWidget(header)
        layout.addWidget(back_button)
        layout.addWidget(stats_label)
        layout.addWidget(scroll_area, 1)
        
        self.setLayout(layout)
        
        # Создаем виджеты навыков
        self.create_skill_widgets()
        
    def get_average_level(self):
        """Получить средний уровень навыков"""
        if not self.game_state.skills:
            return 0
        return sum(self.game_state.skills.values()) / len(self.game_state.skills)
        
    def create_skill_widgets(self):
        """Создать виджеты для каждого навыка"""
        skill_descriptions = {
            "Взлом": {
                "desc": "Способность взламывать компьютерные системы, обходить защиту и находить уязвимости.",
                "color": "#ff5555"
            },
            "Социальная инженерия": {
                "desc": "Манипулирование людьми для получения конфиденциальной информации.",
                "color": "#ffaa55"
            },
            "Программирование": {
                "desc": "Навык написания и понимания кода, создания скриптов и автоматизации задач.",
                "color": "#ffff55"
            },
            "Скрытность": {
                "desc": "Умение оставаться незамеченным в сети и скрывать следы деятельности.",
                "color": "#aaff55"
            },
            "Анализ": {
                "desc": "Способность анализировать данные, выявлять закономерности и принимать решения.",
                "color": "#55ff55"
            },
            "Сетевая безопасность": {
                "desc": "Знание сетевых протоколов, защита сетей и обнаружение вторжений.",
                "color": "#55aaff"
            }
        }
        
        # Сортируем навыки по уровню (от высокого к низкому)
        sorted_skills = sorted(self.game_state.skills.items(), 
                             key=lambda x: x[1], reverse=True)
        
        for skill_name, level in sorted_skills:
            skill_info = skill_descriptions.get(skill_name, {"desc": "", "color": "#888888"})
            skill_widget = self.create_skill_item(skill_name, level, skill_info)
            self.skills_layout.addWidget(skill_widget)
            self.skill_widgets[skill_name] = skill_widget
            
        # Добавляем растягивающий элемент в конец
        self.skills_layout.addStretch()
        
    def create_skill_item(self, skill_name, level, skill_info):
        """Создать виджет отдельного навыка"""
        color = skill_info["color"]
        
        skill_frame = QFrame()
        skill_frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(30, 30, 60, 0.8);
                border: 2px solid {color};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Верхняя строка: название и уровень
        top_layout = QHBoxLayout()
        
        name_label = QLabel(skill_name)
        name_label.setStyleSheet(f"""
            font-weight: bold; 
            color: {color}; 
            font-size: 16px;
            text-shadow: 0 0 5px {color}40;
        """)
        
        level_text = self.get_level_text(level)
        level_label = QLabel(f"Уровень: {level}/10 ({level_text})")
        level_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 14px;")
        
        top_layout.addWidget(name_label)
        top_layout.addStretch()
        top_layout.addWidget(level_label)
        
        # Прогресс-бар
        progress_frame = QFrame()
        progress_frame.setFixedHeight(20)
        progress_frame.setStyleSheet("""
            QFrame {
                background-color: #222244;
                border-radius: 10px;
                border: 1px solid #444477;
            }
        """)
        
        # Заполненная часть прогресс-бара
        fill_width = int((level / 10) * 250)  # Начальная ширина
        fill_widget = QFrame(progress_frame)
        fill_widget.setFixedHeight(16)
        fill_widget.setFixedWidth(fill_width)
        fill_widget.move(2, 2)
        fill_widget.setStyleSheet(f"""
            QFrame {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color},
                    stop:1 {color}80
                );
                border-radius: 8px;
            }}
        """)
        
        # Описание навыка
        desc_label = QLabel(skill_info["desc"])
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #aaaaaa; font-size: 13px; line-height: 1.4;")
        
        # Эффекты от уровня
        effects_label = QLabel(self.get_effects_text(level))
        effects_label.setWordWrap(True)
        effects_label.setStyleSheet(f"color: {color}; font-size: 12px; font-style: italic;")
        
        layout.addLayout(top_layout)
        layout.addWidget(progress_frame)
        layout.addWidget(desc_label)
        layout.addWidget(effects_label)
        
        skill_frame.setLayout(layout)
        
        # Сохраняем ссылки для обновления
        skill_frame.progress_frame = progress_frame
        skill_frame.fill_widget = fill_widget
        skill_frame.level_label = level_label
        
        return skill_frame
        
    def get_level_text(self, level):
        """Получить текстовое описание уровня"""
        if level <= 2:
            return "Новичок"
        elif level <= 4:
            return "Ученик"
        elif level <= 6:
            return "Опытный"
        elif level <= 8:
            return "Эксперт"
        else:
            return "Мастер"
            
    def get_effects_text(self, level):
        """Получить описание эффектов от уровня навыка"""
        if level <= 2:
            return "Эффект: Базовые возможности, медленное выполнение задач"
        elif level <= 4:
            return "Эффект: Стандартная скорость выполнения, доступ к простым заданиям"
        elif level <= 6:
            return "Эффект: Повышенная эффективность, доступ к сложным заданиям"
        elif level <= 8:
            return "Эффект: Высокая скорость выполнения, бонус к наградам"
        else:
            return "Эффект: Максимальная эффективность, доступ к особым заданиям"
            
    def update_ui(self):
        """Обновить отображение навыков"""
        for skill, level in self.game_state.skills.items():
            if skill in self.skill_widgets:
                skill_frame = self.skill_widgets[skill]
                
                # Обновляем уровень
                level_text = self.get_level_text(level)
                skill_frame.level_label.setText(f"Уровень: {level}/10 ({level_text})")
                
                # Обновляем прогресс-бар
                container = skill_frame.progress_frame
                if container.width() > 0:
                    fill_width = int((level / 10) * (container.width() - 4))
                    skill_frame.fill_widget.setFixedWidth(max(0, min(fill_width, container.width() - 4)))
                    
                # Обновляем эффекты
                # (можно добавить, если нужно обновлять и эту часть)
                
    def resizeEvent(self, event):
        """Обработчик изменения размера окна"""
        super().resizeEvent(event)
        self.update_ui()