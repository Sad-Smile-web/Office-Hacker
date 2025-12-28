# ui/menu_widget.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QFrame)
from PySide6.QtCore import Qt, QTimer, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import (QPainter, QLinearGradient, QColor, QPen, QBrush, 
                          QFont, QRadialGradient, QFontMetrics)
from simple_translation import translation
import random
import math
import time
import json
import os

class MenuWidget(QWidget):
    show_settings = Signal()
    show_help = Signal()
    show_about = Signal()
    start_game = Signal()
    load_game = Signal()
    exit_game = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.config = self.load_config()
        self.init_ui()
        self.setup_effects()

        QTimer.singleShot(100, self.start_animations)
        translation.on_language_changed(self.retranslate_ui)
    
    def retranslate_ui(self):
        """Обновить все тексты при смене языка"""
        print(f"🔤 Обновляю меню на язык: {translation.language}")
        
        # Заголовок
        self.title_label.setText(translation.t("menu.office"))
        self.menu_title.setText(translation.t("menu.title"))
        
        # Кнопки
        button_texts = [
            (self.start_btn, "menu.new_game"),
            (self.load_btn, "menu.load_game"),
            (self.settings_btn, "menu.settings"),
            (self.help_btn, "menu.help"),
            (self.about_btn, "menu.about"),
            (self.exit_btn, "menu.exit")
        ]
        
        for btn, key in button_texts:
            btn.setText(translation.t(key))
        
        # Статус - начальное значение
        self.status_label.setText(translation.t("menu.connecting"))
        
        # ОБНОВЛЯЕМ ОПИСАНИЕ
        self.update_description_text()
        
        # Обновляем заголовок главного окна
        if self.parent and hasattr(self.parent, 'setWindowTitle'):
            self.parent.setWindowTitle(translation.t("menu.office"))
    
    def update_description_text(self):
        """Обновить текст описания при смене языка"""
        print(f"📝 Обновляю описание на языке: {translation.language}")
        
        # Останавливаем текущий таймер печати
        if self.typing_timer.isActive():
            self.typing_timer.stop()
        
        # Получаем новый текст
        description_text = translation.t("menu.opican")
        print(f"📝 Текст из перевода: {description_text[:50]}...")
        
        # Устанавливаем новый текст и сбрасываем индекс
        self.typing_text = description_text
        self.typing_index = 0
        self.description.setText("")
        
        # Запускаем печать заново
        self.typing_timer.start(30)
    
    def load_config(self):
        """Загрузить конфигурацию"""
        default_config = {
            "graphics": {
                "enable_effects": True,
                "glitch_effects": True,
                "window_width": 1200,
                "window_height": 800,
                "display_mode": "fullscreen",
                "vsync": True,
                "effect_intensity": 70
            },
            "audio": {
                "enabled": True,
                "volume": 70,
                "master_volume": 70,
                "typing_sounds": True,
                "background_music": True,
                "effects_volume": 80,
                "music_volume": 60,
                "voice_effects": True,
                "environment_sounds": True,
                "dynamic_range": "normal"
            }
        }
        
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r", encoding="utf-8") as f:
                    old_config = json.load(f)
                    
                # Если есть старые настройки графики - переносим их
                if "graphics" in old_config:
                    for key in default_config["graphics"]:
                        if key in old_config["graphics"]:
                            default_config["graphics"][key] = old_config["graphics"][key]
                
                # Если есть старые настройки аудио - переносим их
                if "audio" in old_config:
                    for key in default_config["audio"]:
                        if key in old_config["audio"]:
                            default_config["audio"][key] = old_config["audio"][key]
                            
        except Exception as e:
            print(f"Ошибка загрузки конфига: {e}")
        
        return default_config
    
    def create_new_config(self, config):
        """Создать новый config.json с правильной структурой"""
        try:
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print("[КОНФИГ] Создан новый файл конфигурации")
        except Exception as e:
            print(f"Ошибка создания конфига: {e}")
        
    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(40)
        
        # Левая панель - описание игры
        left_panel = QFrame()
        left_panel.setMinimumWidth(400)
        left_layout = QVBoxLayout()
        
        # Анимированный замок с эффектами - РЕШЕНИЕ: используем QFont вместо font-size
        self.lock_label = QLabel("🔐")
        self.lock_label.setAlignment(Qt.AlignCenter)
        
        # СОЗДАЕМ ШРИФТ ДЛЯ ЗАМКА
        lock_font = QFont()
        lock_font.setPointSize(100)
        self.lock_label.setFont(lock_font)
        
        self.lock_label.setStyleSheet("""
            color: #00bfff;
        """)
        
        # Анимация пульсации для замка
        self.lock_animation = QPropertyAnimation(self.lock_label, b"styleSheet")
        self.lock_animation.setDuration(2000)
        self.lock_animation.setLoopCount(-1)
        self.lock_animation.setStartValue("""
            color: #00bfff;
            text-shadow: 0 0 20px #00bfff;
        """)
        self.lock_animation.setEndValue("""
            color: #00ffff;
            text-shadow: 0 0 40px #00ffff, 0 0 60px #00ffff;
        """)
        self.lock_animation.setEasingCurve(QEasingCurve.InOutSine)
        
        # Заголовок с эффектом неона - РЕШЕНИЕ: тоже используем QFont
        self.title_label = QLabel(translation.t("menu.office"))
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # СОЗДАЕМ ШРИФТ ДЛЯ ЗАГОЛОВКА
        title_font = QFont()
        title_font.setPointSize(36)  # Большой размер
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        
        self.title_label.setStyleSheet("""
            color: #00bfff;
            text-shadow: 0 0 10px #00bfff;
            margin-top: 10px;
        """)
        
        # Анимация для заголовка
        self.title_animation = QPropertyAnimation(self.title_label, b"styleSheet")
        self.title_animation.setDuration(3000)
        self.title_animation.setLoopCount(-1)
        self.title_animation.setStartValue("""
            color: #00bfff;
            text-shadow: 0 0 10px #00bfff;
        """)
        self.title_animation.setEndValue("""
            color: #00ffff;
            text-shadow: 0 0 20px #00ffff, 0 0 30px #00bfff;
        """)
        self.title_animation.setEasingCurve(QEasingCurve.InOutSine)
        
        # Описание игры с эффектом печатной машинки
        description_text = translation.t("menu.opican")
        
        self.description = QLabel("")
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setStyleSheet("""
            font-size: 14px;
            color: #a0a0a0;
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            margin-top: 20px;
            padding: 20px;
            background-color: rgba(16, 16, 16, 0.8);
            border: 1px solid rgba(0, 191, 255, 0.3);
            border-radius: 5px;
        """)
        self.description.setWordWrap(True)
        
        # Таймер для эффекта печатной машинки
        self.typing_index = 0
        self.typing_text = ""
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.type_description)
        self.update_description_text()
        
        left_layout.addWidget(self.lock_label)
        left_layout.addWidget(self.title_label)
        left_layout.addWidget(self.description)
        left_layout.addStretch()
        
        # Статус подключения с эффектом мигания
        self.status_label = QLabel(translation.t("menu.connecting"))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 12px;
            color: #00aa00;
            font-family: 'Courier New', monospace;
        """)
        
        # Анимация мигания для статуса
        self.status_animation = QPropertyAnimation(self.status_label, b"styleSheet")
        self.status_animation.setDuration(1000)
        self.status_animation.setLoopCount(-1)
        self.status_animation.setStartValue("""
            font-size: 12px;
            color: #00aa00;
            font-family: 'Courier New', monospace;
            text-shadow: 0 0 5px #00aa00;
        """)
        self.status_animation.setEndValue("""
            font-size: 12px;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00;
        """)
        self.status_animation.setEasingCurve(QEasingCurve.InOutSine)
        
        left_layout.addWidget(self.status_label)
        
        left_panel.setLayout(left_layout)
        
        # Правая панель - кнопки меню
        right_panel = QFrame()
        right_panel.setMinimumWidth(500)
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        
        # Заголовок правой панели с эффектом
        self.menu_title = QLabel(translation.t("menu.title"))
        self.menu_title.setAlignment(Qt.AlignCenter)
        menu_title_font = QFont()
        menu_title_font.setPointSize(28)
        menu_title_font.setBold(True)
        self.menu_title.setFont(menu_title_font)    
        self.menu_title.setStyleSheet("""
            color: #00ff00;
            margin-bottom: 20px;
            text-shadow: 0 0 5px #00ff00;
        """)
        
        # Анимация для заголовка меню
        self.menu_title_animation = QPropertyAnimation(self.menu_title, b"styleSheet")
        self.menu_title_animation.setDuration(1500)
        self.menu_title_animation.setLoopCount(-1)
        self.menu_title_animation.setStartValue("""
            color: #00ff00;
            text-shadow: 0 0 5px #00ff00;
        """)
        self.menu_title_animation.setEndValue("""
            color: #ffff00;
            text-shadow: 0 0 10px #ffff00, 0 0 15px #ffaa00;
        """)
        
        right_layout.addWidget(self.menu_title)
        
        # Кнопки меню
        self.buttons = []
        
        self.start_btn = self.create_menu_button(translation.t("menu.new_game"), self.start_game.emit)
        self.load_btn = self.create_menu_button(translation.t("menu.load_game"), self.load_game.emit)
        self.settings_btn = self.create_menu_button(translation.t("menu.settings"), lambda: self.show_settings.emit())
        self.help_btn = self.create_menu_button(translation.t("menu.help"), lambda: self.show_help.emit())
        self.about_btn = self.create_menu_button(translation.t("menu.about"), lambda: self.show_about.emit())
        self.exit_btn = self.create_menu_button(translation.t("menu.exit"), lambda: self.exit_game.emit())
        
        # Добавляем всё в правый layout
        for btn in [self.start_btn, self.load_btn, self.settings_btn, 
                   self.help_btn, self.about_btn, self.exit_btn]:
            right_layout.addWidget(btn)
            
        right_layout.addStretch()
        
        right_panel.setLayout(right_layout)
        
        # Добавляем обе панели в главный layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        
        # Таймер для анимации статуса
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(5000)
        
        # Запускаем анимации
        self.start_animations()
        
    def create_menu_button(self, text, callback):
        """Создать стилизованную кнопку меню"""
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        btn.setMinimumHeight(90)

        button_font = QFont()
        button_font.setPointSize(60)
        button_font.setBold(True)
        btn.setFont(button_font)
        
        base_style = """
            QPushButton {
                background-color: rgba(0, 34, 0, 0.8);
                color: #00ff00;
                border: 2px solid #00ff00;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                min-height: 90px;
                border-radius: 8px;
                text-align: center;
                letter-spacing: 1px;
                transition: all 0.3s;
            }
            QPushButton:hover {
                background-color: rgba(0, 68, 0, 0.9);
                border-color: #ffff00;
                color: #ffff00;
                border-width: 3px;
            }
            QPushButton:pressed {
                background-color: rgba(0, 17, 0, 0.9);
                border-color: #ff0000;
                color: #ff0000;
            }
        """
        
        btn.setStyleSheet(base_style)
        self.buttons.append(btn)
        return btn
        
    def type_description(self):
        """Эффект печатной машинки для описания"""
        if self.typing_index < len(self.typing_text):
            char = self.typing_text[self.typing_index]
            current_text = self.description.text()
            self.description.setText(current_text + char)
            self.typing_index += 1
            
            # Звук печати для некоторых символов
            if char not in [' ', '\n'] and random.random() < 0.3:
                try:
                    from audio_manager import AudioManager
                    audio = AudioManager()
                    audio.typing_sound()
                except:
                    pass
        else:
            self.typing_timer.stop()
            
    def start_animations(self):
        """Запустить все анимации"""
        self.lock_animation.start()
        self.title_animation.start()
        self.status_animation.start()
        self.menu_title_animation.start()
        
        # Анимация кнопок
        for i, btn in enumerate(self.buttons):
            animation = QPropertyAnimation(btn, b"geometry")
            original_geometry = btn.geometry()
            animation.setDuration(500 + i * 100)
            animation.setStartValue(original_geometry.translated(0, -30))
            animation.setEndValue(original_geometry)
            animation.setEasingCurve(QEasingCurve.OutBack)
            animation.start()
            
    def setup_effects(self):
        """Настройка эффектов"""
        # Таймер для обновления эффектов
        self.effect_timer = QTimer()
        self.effect_timer.timeout.connect(self.update_effects)
        self.effect_timer.start(30)  # ~33 FPS
        
        # Частицы для эффектов
        self.particles = []
        self.init_particles(20)
        
        # Эффект сканирующих линий
        self.scan_line_y = 0
        self.scan_line_speed = 3
        
        # Эффект пульсации
        self.pulse_value = 0.0
        self.pulse_direction = 1
        
        # Таймер для случайных глитчей
        self.glitch_timer = QTimer()
        self.glitch_timer.timeout.connect(self.trigger_random_effect)
        self.glitch_timer.start(3000)  # Каждые 3 секунды
        
    def init_particles(self, count):
        """Инициализация частиц"""
        for _ in range(count):
            self.particles.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.5, 2.0),
                'color': QColor(
                    random.randint(0, 100),
                    random.randint(150, 255),
                    random.randint(200, 255),
                    random.randint(30, 80)
                ),
                'direction': random.uniform(0, 2 * math.pi),
                'lifetime': random.randint(100, 300)
            })
            
    def update_effects(self):
        """Обновление всех эффектов"""
        # Обновление частиц
        for particle in self.particles:
            particle['x'] += math.cos(particle['direction']) * particle['speed']
            particle['y'] += math.sin(particle['direction']) * particle['speed']
            particle['lifetime'] -= 1
            
            if (particle['x'] < 0 or particle['x'] > self.width() or 
                particle['y'] < 0 or particle['y'] > self.height() or
                particle['lifetime'] <= 0):
                particle.update({
                    'x': random.randint(0, self.width()),
                    'y': random.randint(0, self.height()),
                    'lifetime': random.randint(100, 300)
                })
        
        # Обновление сканирующей линии
        self.scan_line_y = (self.scan_line_y + self.scan_line_speed) % (self.height() + 30)
        
        # Обновление пульсации
        self.pulse_value += 0.02 * self.pulse_direction
        if self.pulse_value >= 1.0:
            self.pulse_direction = -1
            self.pulse_value = 1.0
        elif self.pulse_value <= 0.0:
            self.pulse_direction = 1
            self.pulse_value = 0.0
        
        self.update()
        
    def trigger_random_effect(self):
        """Запустить случайный эффект"""
        if not self.config["graphics"]["enable_effects"]:
            return
            
        # Случайный глитч на кнопке
        if self.buttons and random.random() < 0.3:
            button = random.choice(self.buttons)
            original_style = button.styleSheet()
            
            colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff"]
            color = random.choice(colors)
            
            glitch_style = f"""
                border-color: {color};
                color: {color};
                text-shadow: 0 0 10px {color};
            """
            
            button.setStyleSheet(original_style + glitch_style)
            
            # Возвращаем оригинальный стиль через 300 мс
            QTimer.singleShot(300, lambda: button.setStyleSheet(original_style))
            
    def paintEvent(self, event):
        """Отрисовка эффектов"""
        super().paintEvent(event)
        
        if not self.config["graphics"]["enable_effects"]:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Эффект частиц
        for particle in self.particles:
            alpha = particle['color'].alpha() * (particle['lifetime'] / 300.0)
            color = QColor(particle['color'])
            color.setAlpha(int(alpha))
            
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.setOpacity(0.3)
            painter.drawEllipse(
                int(particle['x']),
                int(particle['y']),
                particle['size'],
                particle['size']
            )
        
        # Сканирующие линии
        scan_height = 25
        scan_gradient = QLinearGradient(0, self.scan_line_y, 0, self.scan_line_y + scan_height)
        scan_gradient.setColorAt(0, QColor(0, 191, 255, 0))
        scan_gradient.setColorAt(0.3, QColor(0, 191, 255, int(100 * self.pulse_value)))
        scan_gradient.setColorAt(0.7, QColor(0, 191, 255, int(100 * self.pulse_value)))
        scan_gradient.setColorAt(1, QColor(0, 191, 255, 0))
        
        painter.setOpacity(0.2)
        painter.fillRect(0, self.scan_line_y, self.width(), scan_height, scan_gradient)
        
        # Эффект сетки
        grid_size = 50
        painter.setOpacity(0.05)
        painter.setPen(QPen(QColor(0, 191, 255, 50), 1))
        
        for x in range(0, self.width(), grid_size):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), grid_size):
            painter.drawLine(0, y, self.width(), y)
        
        # Свечение по краям
        edge_glow = QLinearGradient(0, 0, self.width(), 0)
        edge_glow.setColorAt(0, QColor(0, 191, 255, int(50 * self.pulse_value)))
        edge_glow.setColorAt(0.1, QColor(0, 191, 255, 0))
        edge_glow.setColorAt(0.9, QColor(0, 191, 255, 0))
        edge_glow.setColorAt(1, QColor(0, 191, 255, int(50 * self.pulse_value)))
        
        painter.setOpacity(0.1)
        painter.fillRect(0, 0, self.width(), self.height(), edge_glow)
        
        # Глитч-эффекты если включены
        if (self.config["graphics"]["glitch_effects"] and 
            self.config["graphics"]["enable_effects"] and 
            random.random() < 0.01):
            
            # Случайные цветные полосы
            for _ in range(random.randint(1, 3)):
                y = random.randint(0, self.height())
                height = random.randint(5, 20)
                color = QColor(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(30, 70)
                )
                painter.setOpacity(0.2)
                painter.fillRect(0, y, self.width(), height, color)
        
        painter.setOpacity(1.0)
        
    def update_status(self):
        """Обновление статусного сообщения"""
        # Используем ключи для переводов статусов
        status_keys = [
            "status.encrypting_channel",
            "status.checking_access",
            "status.sync_with_hq",
            "status.loading_missions",
            "status.connecting_to_global_network",
            "status.checking_security_system",
            "status.loading_configuration",
            "status.initializing_terminal",
            "status.call_forwarding",
            "status.sending_admin",
            "status.remembering_name",
            "status.loading_junk",
            "status.updating_software",
            "status.leaving_feedback",
            "status.menu_idle",
            "status.virus_scan",
            "status.updating_database",
            "status.backup",
            "status.memory_optimization",
            "status.calibrating_sensors",
            "status.visit_website"
        ]
        
        current = self.status_label.text()
        available = [translation.t(key) for key in status_keys if translation.t(key) != current]
        new_status = random.choice(available) if available else translation.t(status_keys[0])
        self.status_label.setText(new_status)
        
        if random.random() < 0.3 and self.config["graphics"]["enable_effects"]:
            self.trigger_status_effect()
            
    def trigger_status_effect(self):
        """Эффект при обновлении статуса"""
        flash_animation = QPropertyAnimation(self.status_label, b"styleSheet")
        flash_animation.setDuration(200)
        flash_animation.setStartValue("""
            font-size: 12px;
            color: #ffff00;
            font-family: 'Courier New', monospace;
            text-shadow: 0 0 10px #ffff00;
        """)
        flash_animation.setEndValue("""
            font-size: 12px;
            color: #00aa00;
            font-family: 'Courier New', monospace;
            text-shadow: 0 0 5px #00aa00;
        """)
        flash_animation.start()
        
    def update_effects_config(self):
        """Обновить настройки эффектов (вызывается из main_window)"""
        self.update()