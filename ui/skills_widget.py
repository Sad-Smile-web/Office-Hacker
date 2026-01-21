# ui/skills_widget.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QFrame, QScrollArea,
                               QGridLayout, QGraphicsOpacityEffect, QGraphicsDropShadowEffect)
from PySide6.QtCore import (Qt, Signal, QTimer, QPropertyAnimation, 
                           QEasingCurve, QParallelAnimationGroup, 
                           QSequentialAnimationGroup, Property)
from PySide6.QtGui import (QFont, QColor, QLinearGradient, QRadialGradient,
                          QPainter, QPen, QBrush, QPainterPath, QFontMetrics)
import math
import time
import random

from simple_translation import translation


def tr(key, default=None, **kwargs):
    """Вспомогательная функция для перевода"""
    if default is None:
        default = key
    return translation.t(key, default=default, **kwargs)


class CyberSkillWidget(QWidget):
    """Киберпанк-виджет для одного навыка с анимациями"""
    
    # Определяем свойство для анимации уровня
    _target_level = 0
    
    @Property(float)
    def target_level(self):
        return self._target_level
    
    @target_level.setter
    def target_level(self, value):
        self._target_level = value
        self.on_level_animation_changed(value)
    
    def __init__(self, skill_name, level, description, color, parent=None):
        super().__init__(parent)
        self.skill_name = skill_name
        self.current_level = level
        self._target_level = level
        self.max_level = 10
        self.color = QColor(color)
        self.description = description
        self.hovered = False
        self.glow_intensity = 0
        self.pulse_intensity = 0
        self.level_up_animation = False
        self.particles = []
        self.sparks = []
        self.tooltip = None
        self.tooltip_timer = QTimer()
        self.tooltip_timer.setSingleShot(True)
        self.tooltip_timer.timeout.connect(self.show_tooltip)
        
        self.setFixedSize(200, 220)  # Увеличиваем высоту для полного текста уровня
        self.setAttribute(Qt.WA_Hover, True)
        self.setCursor(Qt.PointingHandCursor)
        
        # Эффект тени
        self.shadow_effect = QGraphicsDropShadowEffect(self)
        self.shadow_effect.setBlurRadius(15)
        self.shadow_effect.setOffset(0, 0)
        self.shadow_effect.setColor(QColor(0, 255, 255, 80))
        self.setGraphicsEffect(self.shadow_effect)
        
        # Таймеры для анимаций
        self.glow_timer = QTimer()
        self.glow_timer.timeout.connect(self.update_glow)
        self.glow_timer.start(40)
        
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.update_pulse)
        self.pulse_timer.start(120)
        
        self.particle_timer = QTimer()
        self.particle_timer.timeout.connect(self.update_particles)
        self.particle_timer.start(60)
        
        # Анимация изменения уровня
        self.level_animation = QPropertyAnimation(self, b"target_level")
        self.level_animation.setDuration(1200)
        self.level_animation.setEasingCurve(QEasingCurve.OutElastic)
        
        # Инициализация частиц
        self.init_particles()
    
    def init_particles(self):
        """Инициализация частиц для эффектов"""
        for _ in range(10):
            self.particles.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'size': random.uniform(0.3, 1.5),
                'alpha': random.randint(20, 40),
                'speed': random.uniform(0.3, 1.0),
                'dx': random.uniform(-0.5, 0.5),
                'dy': random.uniform(-0.5, 0.5),
                'color': QColor(self.color),
                'life': random.randint(40, 80)
            })
    
    def update_glow(self):
        """Обновление интенсивности свечения"""
        if self.hovered:
            self.glow_intensity = min(self.glow_intensity + 0.2, 1.0)
            self.shadow_effect.setColor(QColor(self.color.red(), 
                                             self.color.green(), 
                                             self.color.blue(), 
                                             int(120 * self.glow_intensity)))
            self.shadow_effect.setBlurRadius(int(20 * self.glow_intensity))
        else:
            self.glow_intensity = max(self.glow_intensity - 0.08, 0.0)
            self.shadow_effect.setColor(QColor(0, 255, 255, int(80 * (1 - self.glow_intensity))))
            self.shadow_effect.setBlurRadius(int(15 * (1 - self.glow_intensity) + 5))
        
        self.update()
    
    def update_pulse(self):
        """Обновление пульсации"""
        if self.level_up_animation:
            self.pulse_intensity = (math.sin(time.time() * 6) + 1) / 2
        elif self.hovered:
            self.pulse_intensity = 0.2 + (math.sin(time.time() * 3) + 1) / 5
        else:
            self.pulse_intensity = 0
        
        self.update()
    
    def update_particles(self):
        """Обновление частиц"""
        if not self.hovered and not self.level_up_animation:
            return
            
        for particle in self.particles:
            particle['x'] += particle['dx'] * particle['speed']
            particle['y'] += particle['dy'] * particle['speed']
            particle['life'] -= 1
            
            if (particle['x'] < -5 or particle['x'] > self.width() + 5 or
                particle['y'] < -5 or particle['y'] > self.height() + 5 or
                particle['life'] <= 0):
                
                particle.update({
                    'x': random.randint(0, self.width()) if not self.hovered else self.width() // 2,
                    'y': random.randint(0, self.height()) if not self.hovered else self.height() // 2,
                    'size': random.uniform(0.3, 1.5),
                    'alpha': random.randint(20, 40),
                    'speed': random.uniform(0.3, 1.0),
                    'dx': random.uniform(-0.5, 0.5),
                    'dy': random.uniform(-0.5, 0.5),
                    'color': QColor(self.color),
                    'life': random.randint(40, 80)
                })
        
        # Генерация искр при повышении уровня
        if self.level_up_animation and random.random() < 0.2:
            for _ in range(2):
                self.sparks.append({
                    'x': self.width() // 2,
                    'y': self.height() // 2 - 40,
                    'dx': random.uniform(-2, 2),
                    'dy': random.uniform(-3, -0.5),
                    'life': 20,
                    'size': random.uniform(0.8, 2)
                })
        
        # Обновление искр
        for spark in self.sparks[:]:
            spark['x'] += spark['dx']
            spark['y'] += spark['dy']
            spark['life'] -= 1
            
            if spark['life'] <= 0:
                self.sparks.remove(spark)
        
        self.update()
    
    def enterEvent(self, event):
        self.hovered = True
        # Запускаем таймер для показа подсказки через 500 мс
        self.tooltip_timer.start(500)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.hovered = False
        # Останавливаем таймер и скрываем подсказку
        self.tooltip_timer.stop()
        self.hide_tooltip()
        super().leaveEvent(event)
    
    def show_tooltip(self):
        """Показать подсказку с описанием навыка"""
        if not self.hovered:
            return
        
        if self.tooltip is None:
            self.tooltip = QLabel(self.parent())
            self.tooltip.setObjectName("skillTooltip")
            self.tooltip.setWordWrap(True)
            self.tooltip.setAlignment(Qt.AlignCenter)
            self.tooltip.setStyleSheet("""
                QLabel#skillTooltip {
                    background-color: rgba(0, 20, 40, 220);
                    color: #a0e0ff;
                    border: 2px solid #00a0ff;
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 11px;
                    font-family: 'Source Code Pro';
                    min-width: 180px;
                    max-width: 180px;
                }
            """)
        
        # Получаем уровень мастерства
        level_names = [
            tr("skillsmn.level_novice_full", "Новичок"),
            tr("skillsmn.level_apprentice_full", "Ученик"),
            tr("skillsmn.level_experienced_full", "Опытный"),
            tr("skillsmn.level_expert_full", "Эксперт"),
            tr("skillsmn.level_master_full", "Мастер")
        ]
        level_idx = min((int(self.current_level) - 1) // 2, 4)
        
        # Устанавливаем текст подсказки
        tooltip_text = f"<b>{self.skill_name}</b><br><br>{self.description}<br><br>Уровень: {int(self.current_level)}/10<br>Мастерство: {level_names[level_idx]}"
        self.tooltip.setText(tooltip_text)
        
        # Подгоняем размер подсказки
        self.tooltip.adjustSize()
        
        # Получаем глобальные координаты виджета
        global_pos = self.mapToGlobal(self.rect().topLeft())
        parent_pos = self.parent().mapFromGlobal(global_pos)
        
        # Позиционируем подсказку над виджетом
        tooltip_x = parent_pos.x() + (self.width() - self.tooltip.width()) // 2
        tooltip_y = parent_pos.y() - self.tooltip.height() - 10
        
        # Проверяем, чтобы подсказка не выходила за границы экрана
        if tooltip_y < 0:
            tooltip_y = parent_pos.y() + self.height() + 10
        
        self.tooltip.setGeometry(tooltip_x, tooltip_y, 
                                self.tooltip.width(), self.tooltip.height())
        self.tooltip.show()
        self.tooltip.raise_()
    
    def hide_tooltip(self):
        """Скрыть подсказку"""
        if self.tooltip:
            self.tooltip.hide()
    
    def on_level_animation_changed(self, value):
        """Обработчик изменения значения анимации уровня"""
        self.current_level = value
        self.update()
        
        if value >= self._target_level and self.level_up_animation:
            self.level_up_animation = False
    
    def animate_level_change(self, new_level):
        """Анимировать изменение уровня навыка"""
        if new_level <= self.current_level:
            return
            
        self.level_animation.setStartValue(self.current_level)
        self.level_animation.setEndValue(new_level)
        self.level_up_animation = True
        
        # Запускаем анимацию
        self.level_animation.start()
        
        # Создаем эффектные частицы
        self.create_level_up_particles()
    
    def create_level_up_particles(self):
        """Создать частицы для анимации повышения уровня"""
        center_x = self.width() // 2
        center_y = self.height() // 2 - 40
        
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            
            self.particles.append({
                'x': center_x,
                'y': center_y,
                'size': random.uniform(0.8, 2),
                'alpha': random.randint(120, 200),
                'speed': speed,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'color': QColor(self.color).lighter(150),
                'life': random.randint(30, 60)
            })
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Фон с градиентом
        bg_gradient = QLinearGradient(0, 0, self.width(), self.height())
        if self.level_up_animation:
            bg_gradient.setColorAt(0, QColor(30, 30, 60, 180))
            bg_gradient.setColorAt(1, QColor(15, 15, 35, 180))
        elif self.hovered:
            bg_gradient.setColorAt(0, QColor(25, 25, 50, 150))
            bg_gradient.setColorAt(1, QColor(12, 12, 30, 150))
        else:
            bg_gradient.setColorAt(0, QColor(20, 20, 40, 120))
            bg_gradient.setColorAt(1, QColor(10, 10, 25, 120))
        
        # Рисуем фон с закругленными углами
        path = QPainterPath()
        path.addRoundedRect(3, 3, self.width()-6, self.height()-6, 10, 10)
        painter.fillPath(path, bg_gradient)
        
        # Внешняя рамка
        border_width = 2 + (1.5 * self.pulse_intensity)
        border_color = self.color.lighter(150) if self.hovered else self.color
        
        painter.setPen(QPen(border_color, border_width))
        painter.drawPath(path)
        
        # Эффект свечения при наведении
        if self.hovered or self.level_up_animation:
            glow_color = QColor(self.color)
            glow_alpha = int(40 * self.glow_intensity + 30 * self.pulse_intensity)
            glow_color.setAlpha(glow_alpha)
            
            painter.setPen(QPen(glow_color, 5))
            painter.drawPath(path)
        
        # Рисуем частицы
        for particle in self.particles:
            alpha = particle['alpha'] * (particle['life'] / 80.0)
            particle_color = QColor(particle['color'])
            particle_color.setAlpha(int(alpha))
            
            painter.setBrush(particle_color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(particle['x']), int(particle['y']), 
                              int(particle['size']), int(particle['size']))
        
        # Круглый прогресс-бар
        center_x = self.width() // 2
        circle_y = 55
        radius = 35
        
        # Анимированный радиус при повышении уровня
        display_radius = radius * (1 + 0.08 * self.pulse_intensity)
        
        # Фон круга
        painter.setPen(QPen(QColor(40, 40, 70, 100), 2))
        painter.drawEllipse(int(center_x - display_radius), int(circle_y - display_radius), 
                          int(display_radius * 2), int(display_radius * 2))
        
        # Прогресс-дуга
        progress = self.current_level / self.max_level
        angle = 360 * progress
        
        pen_width = 4 + (1.5 * self.pulse_intensity)
        pen = QPen(self.color, pen_width)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        start_angle = 90 * 16
        span_angle = -int(angle * 16)
        painter.drawArc(int(center_x - display_radius), int(circle_y - display_radius), 
                       int(display_radius * 2), int(display_radius * 2), start_angle, span_angle)
        
        # Внутренний круг с градиентом
        inner_radius = display_radius * 0.6
        inner_gradient = QRadialGradient(center_x, circle_y, inner_radius)
        
        if self.level_up_animation:
            inner_gradient.setColorAt(0, self.color.lighter(180))
            inner_gradient.setColorAt(1, self.color.darker(130))
        else:
            inner_gradient.setColorAt(0, self.color.lighter(160))
            inner_gradient.setColorAt(1, self.color.darker(110))
        
        painter.setBrush(inner_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(center_x - inner_radius), int(circle_y - inner_radius), 
                          int(inner_radius * 2), int(inner_radius * 2))
        
        # Уровень навыка в центре
        level_color = QColor(255, 255, 255)
        if self.level_up_animation:
            flash_value = (math.sin(time.time() * 8) + 1) / 2
            level_color = QColor(
                int(255 * flash_value + 255 * (1 - flash_value)),
                int(255 * flash_value + 200 * (1 - flash_value)),
                int(200 * flash_value + 100 * (1 - flash_value))
            )
        
        painter.setPen(level_color)
        font = QFont("Source Code Pro", 16, QFont.Bold)
        painter.setFont(font)
        
        level_text = f"{int(self.current_level)}"
        painter.drawText(center_x - 8, circle_y + 6, level_text)
        
        # Название навыка (сокращенное)
        painter.setPen(QColor(220, 220, 255))
        font = QFont("Source Code Pro", 10, QFont.Bold)
        painter.setFont(font)
        
        # Сокращаем длинные названия с использованием перевода
        short_names = {
            tr("skillsmn.hacking", "Взлом"): tr("skillsmn.hacking_short", "ВЗЛОМ"),
            tr("skillsmn.social", "Социальная инженерия"): tr("skillsmn.social_short", "СОЦ.ИНЖ"),
            tr("skillsmn.programming", "Программирование"): tr("skillsmn.programming_short", "ПРОГРАМ"),
            tr("skillsmn.stealth", "Скрытность"): tr("skillsmn.stealth_short", "СКРЫТН"),
            tr("skillsmn.analysis", "Анализ"): tr("skillsmn.analysis_short", "АНАЛИЗ"),
            tr("skillsmn.network", "Сетевая безопасность"): tr("skillsmn.network_short", "СЕТЬ")
        }
        
        display_name = short_names.get(self.skill_name, self.skill_name[:8])
        painter.drawText(0, circle_y + 45, self.width(), 20, 
                        Qt.AlignCenter, display_name)
        
        # Уровень мастерства с использованием перевода - ПОЛНЫЙ ТЕКСТ
        level_names = [
            tr("skillsmn.level_novice_full", "Новичок"),
            tr("skillsmn.level_apprentice_full", "Ученик"),
            tr("skillsmn.level_experienced_full", "Опытный"),
            tr("skillsmn.level_expert_full", "Эксперт"),
            tr("skillsmn.level_master_full", "Мастер")
        ]
        level_idx = min((int(self.current_level) - 1) // 2, 4)
        
        level_name_color = QColor(200, 230, 255)  # Светло-голубой для лучшей видимости
        if self.level_up_animation:
            level_name_color = QColor(255, 255, 150)
        
        painter.setPen(level_name_color)
        font = QFont("Source Code Pro", 9, QFont.Bold)  # Увеличили шрифт
        painter.setFont(font)
        
        # Рисуем текст уровня мастерства
        level_text = level_names[level_idx]
        text_rect = painter.boundingRect(0, circle_y + 65, self.width(), 25, 
                                         Qt.AlignCenter, level_text)
        
        # Фон для текста уровня мастерства
        bg_rect = text_rect.adjusted(-5, -2, 5, 2)
        painter.fillRect(bg_rect, QColor(0, 0, 0, 150))
        
        painter.drawText(0, circle_y + 65, self.width(), 25, 
                        Qt.AlignCenter, level_text)


class SkillsWidget(QWidget):
    """Виджет навыков для встраивания в главное окно"""
    
    # Сигнал для возврата в игровой интерфейс
    back_to_game = Signal()
    
    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self.game_state = game_state
        self.previous_levels = game_state.skills.copy() if game_state.skills else {}
        self.skill_widgets = {}
        
        self.setObjectName("SkillsWidget")
        
        self.init_ui()
        self.update_translations()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Заголовок с улучшенной видимостью
        self.header = QLabel(tr("skillsmn.title", "⚡ КИБЕРНАВЫКИ СОТРУДНИКА ⚡"))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setObjectName("skillsHeader")
        self.header.setStyleSheet("""
            QLabel#skillsHeader {
                color: #00ffff;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Source Code Pro';
                text-shadow: 0 0 10px #00ffff, 
                             0 0 20px #00ffff, 
                             0 0 30px #0080ff;
                padding: 10px;
                margin: 10px 0;
                background-color: rgba(0, 20, 40, 180);
                border: 2px solid #0066cc;
                border-radius: 8px;
            }
        """)
        
        # Статистика с улучшенной видимостью
        self.stats_label = QLabel(self.get_stats_text())
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setObjectName("statsLabel")
        self.stats_label.setStyleSheet("""
            QLabel#statsLabel {
                color: #a0e0ff;
                font-size: 14px;
                font-family: 'Source Code Pro';
                padding: 8px;
                margin: 5px 0;
                background-color: rgba(0, 30, 60, 150);
                border: 1px solid #004488;
                border-radius: 5px;
            }
        """)
        
        # Сетка навыков
        self.skills_grid = QGridLayout()
        self.skills_grid.setSpacing(25)
        self.skills_grid.setContentsMargins(20, 20, 20, 20)
        
        # Создаем виджеты навыков
        self.create_skill_widgets()
        
        # Контейнер для сетки
        grid_container = QWidget()
        grid_container.setLayout(self.skills_grid)
        
        # Скроллируемая область
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setObjectName("skillsScrollArea")
        scroll_area.setWidget(grid_container)
        
        # Информационная панель
        info_frame = QFrame()
        info_frame.setObjectName("skillsInfoPanel")
        info_frame.setStyleSheet("""
            QFrame#skillsInfoPanel {
                background-color: rgba(0, 30, 60, 180);
                border: 1px solid #0066cc;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        info_layout = QVBoxLayout(info_frame)
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("""
            QLabel {
                color: #a0e0ff;
                font-family: 'Source Code Pro';
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        info_layout.addWidget(self.info_label)
        
        # Кнопка возврата
        self.back_button = QPushButton(tr("skillsmn.back_button", "НАЗАД"))
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.back_to_game.emit)
        self.back_button.setObjectName("backToInfoButton")
        self.back_button.setStyleSheet("""
            QPushButton#backToInfoButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0066cc, stop:1 #004488);
                color: #ffffff;
                border: 2px solid #00aaff;
                border-radius: 5px;
                padding: 10px 30px;
                font-family: 'Source Code Pro';
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#backToInfoButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00aaff, stop:1 #0066cc);
                border-color: #00ffff;
                color: #ffff00;
            }
        """)
        
        # Эффект тени для кнопки
        button_shadow = QGraphicsDropShadowEffect()
        button_shadow.setBlurRadius(15)
        button_shadow.setOffset(0, 3)
        button_shadow.setColor(QColor(0, 191, 255, 100))
        self.back_button.setGraphicsEffect(button_shadow)
        
        # Центрируем кнопку
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()
        
        layout.addWidget(self.header)
        layout.addWidget(self.stats_label)
        layout.addWidget(scroll_area, 1)
        layout.addWidget(info_frame)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Таймер для обновления статистики
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.check_for_updates)
        self.update_timer.start(1000)
    
    def create_skill_widgets(self):
        """Создать виджеты навыков"""
        if not self.game_state or not self.game_state.skills:
            return
        
        # Очищаем сетку
        for i in reversed(range(self.skills_grid.count())): 
            self.skills_grid.itemAt(i).widget().setParent(None)
        
        self.skill_widgets.clear()
        
        # Описания навыков
        skill_descriptions = {
            tr("skillsmn.hacking", "Взлом"): tr("skillsmn.hacking_desc", "Взлом систем, обход защиты, поиск уязвимостей"),
            tr("skillsmn.social", "Социальная инженерия"): tr("skillsmn.social_desc", "Манипулирование людьми для получения информации"),
            tr("skillsmn.programming", "Программирование"): tr("skillsmn.programming_desc", "Создание кода, скриптов и автоматизация"),
            tr("skillsmn.stealth", "Скрытность"): tr("skillsmn.stealth_desc", "Сокрытие следов, анонимность в сети"),
            tr("skillsmn.analysis", "Анализ"): tr("skillsmn.analysis_desc", "Анализ данных, выявление закономерностей"),
            tr("skillsmn.network", "Сетевая безопасность"): tr("skillsmn.network_desc", "Защита сетей, обнаружение вторжений")
        }
        
        # Цвета для навыков
        skill_colors = {
            tr("skillsmn.hacking", "Взлом"): "#ff0066",
            tr("skillsmn.social", "Социальная инженерия"): "#ff9900",
            tr("skillsmn.programming", "Программирование"): "#ffff00",
            tr("skillsmn.stealth", "Скрытность"): "#00ff00",
            tr("skillsmn.analysis", "Анализ"): "#00ffff",
            tr("skillsmn.network", "Сетевая безопасность"): "#0066ff"
        }
        
        sorted_skills = sorted(self.game_state.skills.items(), 
                             key=lambda x: x[1], reverse=True)
        
        for idx, (skill_name, level) in enumerate(sorted_skills):
            row = idx // 3
            col = idx % 3
            
            description = skill_descriptions.get(skill_name, "")
            color = skill_colors.get(skill_name, "#888888")
            
            skill_widget = CyberSkillWidget(skill_name, level, description, color)
            self.skills_grid.addWidget(skill_widget, row, col)
            self.skill_widgets[skill_name] = skill_widget
    
    def get_stats_text(self):
        """Получить текст статистики"""
        if not self.game_state or not self.game_state.skills:
            return tr("skillsmn.no_skills", "Навыки не загружены...")
        
        total = len(self.game_state.skills)
        avg_level = sum(self.game_state.skills.values()) / total
        
        # Находим максимальный навык
        max_skill = max(self.game_state.skills.items(), key=lambda x: x[1])
        
        total_points = sum(self.game_state.skills.values())
        max_points = total * 10
        progress_percent = (total_points / max_points) * 100
        
        return tr(
            "skillsmn.stats_format",
            "📊 Статистика: {total} навыков | Средний уровень: {avg:.1f}/10 | Прогресс: {progress:.0f}% | Макс: {max_name} ({max_level}/10)"
        ).format(
            total=total,
            avg=avg_level,
            progress=progress_percent,
            max_name=max_skill[0],
            max_level=max_skill[1]
        )
    
    def check_for_updates(self):
        """Проверить обновления уровней навыков"""
        if not self.game_state or not self.game_state.skills:
            return
        
        # Обновляем статистику
        self.stats_label.setText(self.get_stats_text())
        
        # Проверяем изменения уровней и запускаем анимации
        for skill_name, current_level in self.game_state.skills.items():
            if skill_name in self.skill_widgets:
                previous_level = self.previous_levels.get(skill_name, 0)
                
                # Если уровень изменился
                if current_level != previous_level and current_level > previous_level:
                    # Запускаем анимацию повышения уровня
                    self.skill_widgets[skill_name].animate_level_change(current_level)
                
                # Обновляем предыдущий уровень
                self.previous_levels[skill_name] = current_level
    
    def update_translations(self):
        """Обновить тексты при смене языка"""
        # Обновляем заголовок
        self.header.setText(tr("skillsmn.title", "⚡ КИБЕРНАВЫКИ СОТРУДНИКА ⚡"))
        
        # Обновляем подсказки
        self.info_label.setText(
            tr("skillsmn.tips", 
               "💡 Подсказки:\n"
               "• Наведите курсор на навык для просмотра деталей\n"
               "• Уровни повышаются выполнением заданий\n"
               "• Высокие навыки открывают доступ к сложным заданиям")
        )
        
        # Обновляем кнопку
        self.back_button.setText(tr("skillsmn.back_button", "НАЗАД"))
        
        # Обновляем статистику
        self.stats_label.setText(self.get_stats_text())
        
        # Пересоздаем виджеты навыков с обновленными названиями
        self.create_skill_widgets()
    
    def set_game_state(self, game_state):
        """Обновить игровое состояние"""
        self.game_state = game_state
        self.previous_levels = game_state.skills.copy() if game_state.skills else {}
        self.update_translations()
    
    def showEvent(self, event):
        """Обработчик показа виджета"""
        super().showEvent(event)
        
        # Обновляем статистику при показе
        self.stats_label.setText(self.get_stats_text())
        
        # Обновляем предыдущие уровни
        if self.game_state and self.game_state.skills:
            self.previous_levels = self.game_state.skills.copy()
        
        # Запускаем таймер обновления
        self.update_timer.start(1000)
    
    def hideEvent(self, event):
        """Обработчик скрытия виджета"""
        super().hideEvent(event)
        
        # Останавливаем таймер при скрытии
        self.update_timer.stop()