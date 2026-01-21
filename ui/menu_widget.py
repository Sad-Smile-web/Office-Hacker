# ui/menu_widget.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QFrame)
from PySide6.QtCore import Qt, QTimer, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import (QPainter, QLinearGradient, QColor, QPen, QBrush, 
                          QFont, QRadialGradient, QFontMetrics)
from simple_translation import translation
import random
import math
import json
import os

class MenuWidget(QWidget):
    # Сигналы для main_window
    new_game_clicked = Signal()
    load_game_clicked = Signal()
    settings_clicked = Signal()
    help_clicked = Signal()
    about_clicked = Signal()
    exit_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.config = self.load_config()
        
        print("MenuWidget: инициализация")
        
        # Устанавливаем стиль для виджета
        self.setStyleSheet("""
            MenuWidget {
                background-color: #0a0a0a;
            }
        """)
        
        # Создаем словарь с текстом по умолчанию для каждого языка
        self.default_texts = {
            "ru": {
                "new_game": "НОВАЯ ИГРА",
                "load_game": "ЗАГРУЗИТЬ ИГРУ", 
                "settings": "НАСТРОЙКИ",
                "help": "ПОМОЩЬ",
                "about": "О ПРОГРАММЕ",
                "exit": "ВЫХОД",
                "office": "ОФИСНЫЙ ТЕРМИНАЛ",
                "title": "ГЛАВНОЕ МЕНЮ",
                "connecting": "Подключение...",
                "opican": "Симулятор работы в сфере кибербезопасности.\nВыполняйте задания, развивайте навыки и продвигайтесь по карьерной лестнице."
            },
            "en": {
                "new_game": "NEW GAME",
                "load_game": "LOAD GAME",
                "settings": "SETTINGS",
                "help": "HELP",
                "about": "ABOUT",
                "exit": "EXIT",
                "office": "OFFICE TERMINAL",
                "title": "MAIN MENU",
                "connecting": "Connecting...",
                "opican": "Cybersecurity work simulator.\nComplete tasks, develop skills and climb the career ladder."
            }
        }
        
        self.init_ui()
        self.setup_effects()
        QTimer.singleShot(100, self.start_animations)
        
        # Подписываемся на смену языка СРАЗУ
        translation.on_language_changed(self.retranslate_ui)
        
        # Вызываем обновление переводов сразу после инициализации
        QTimer.singleShot(50, self.retranslate_ui)
    
    def retranslate_ui(self):
        """Обновить все тексты при смене языка"""
        current_lang = translation.get_current_language()
        if not current_lang:
            current_lang = "ru"
        
        print(f"🔤 Обновляю меню на язык: {current_lang}")
        
        # Получаем тексты для текущего языка
        texts = self.default_texts.get(current_lang, self.default_texts["ru"])
        
        # Заголовок окна
        title_text = translation.t("menu.office", texts["office"])
        self.title_label.setText(title_text)
        
        # Заголовок меню
        menu_title_text = translation.t("menu.title", texts["title"])
        self.menu_title.setText(menu_title_text)
        
        # Кнопки - используем переводы напрямую
        button_mapping = [
            (self.start_btn, "menu.new_game"),
            (self.load_btn, "menu.load_game"),
            (self.settings_btn, "menu.settings"),
            (self.help_btn, "menu.help"),
            (self.about_btn, "menu.about"),
            (self.exit_btn, "menu.exit")
        ]
        
        for btn, key in button_mapping:
            # Получаем перевод
            translated = translation.t(key)
            
            # Если перевод вернул ключ (перевод не найден), используем текст по умолчанию
            if translated == key:
                btn.setText(texts.get(key.split('.')[-1], key))
            else:
                # Используем полученный перевод (в нем уже есть эмодзи из файлов переводов)
                btn.setText(translated)
        
        # Статус
        status_text = translation.t("menu.connecting", texts["connecting"])
        self.status_label.setText(status_text)
        
        # Описание
        description_text = translation.t("menu.opican", texts["opican"])
        self.update_description_text(description_text)
        
        # Обновляем заголовок главного окна
        if self.parent and hasattr(self.parent, 'setWindowTitle'):
            self.parent.setWindowTitle(translation.t("app.title", "SIBERIA-SOFTWARE - СИМУЛЯТОР КИБЕРБЕЗОПАСНОСТИ"))
    
    def update_description_text(self, text):
        """Обновить текст описания"""
        # Останавливаем текущий таймер печати
        if hasattr(self, 'typing_timer') and self.typing_timer.isActive():
            self.typing_timer.stop()
        
        # Устанавливаем новый текст
        self.typing_text = text
        self.typing_index = 0
        self.description.setText("")
        
        # Запускаем печать заново
        if hasattr(self, 'typing_timer'):
            self.typing_timer.start(30)
    
    def load_config(self):
        """Загрузить конфигурацию"""
        default_config = {
            "graphics": {
                "enable_effects": True,
                "glitch_effects": True,
                "effect_intensity": 70
            },
            "audio": {
                "enabled": True
            }
        }
        
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return config
        except Exception as e:
            print(f"Ошибка загрузки конфига: {e}")
        
        return default_config
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(40)
        
        # Левая панель - описание
        left_panel = QFrame()
        left_panel.setMinimumWidth(400)
        left_panel.setStyleSheet("background-color: transparent;")
        left_layout = QVBoxLayout()
        left_layout.setSpacing(20)
        
        # Анимированный замок
        self.lock_label = QLabel("🔐")
        self.lock_label.setAlignment(Qt.AlignCenter)
        lock_font = QFont()
        lock_font.setPointSize(100)
        self.lock_label.setFont(lock_font)
        self.lock_label.setStyleSheet("color: #00bfff;")
        
        # Заголовок
        self.title_label = QLabel("ОФИСНЫЙ ТЕРМИНАЛ")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(36)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("""
            color: #00bfff;
            text-shadow: 0 0 10px #00bfff;
            margin-top: 10px;
        """)
        
        # Описание с эффектом печатной машинки
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
        
        # Инициализация эффекта печатной машинки
        self.typing_index = 0
        self.typing_text = ""
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.type_description)
        
        left_layout.addWidget(self.lock_label)
        left_layout.addWidget(self.title_label)
        left_layout.addWidget(self.description)
        left_layout.addStretch()
        
        # Статус
        self.status_label = QLabel("Подключение...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 12px;
            color: #00aa00;
            font-family: 'Courier New', monospace;
        """)
        left_layout.addWidget(self.status_label)
        
        left_panel.setLayout(left_layout)
        
        # Правая панель - кнопки меню
        right_panel = QFrame()
        right_panel.setMinimumWidth(500)
        right_panel.setStyleSheet("background-color: transparent;")
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        
        # Заголовок меню
        self.menu_title = QLabel("ГЛАВНОЕ МЕНЮ")
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
        right_layout.addWidget(self.menu_title)
        
        # Создаем кнопки (текст будет установлен при обновлении переводов)
        self.buttons = []
        
        # 1. Новая игра
        self.start_btn = self.create_menu_button("", self.on_new_game_clicked)
        right_layout.addWidget(self.start_btn)
        
        # 2. Загрузить игру
        self.load_btn = self.create_menu_button("", self.on_load_game_clicked)
        right_layout.addWidget(self.load_btn)
        
        # 3. Настройки
        self.settings_btn = self.create_menu_button("", self.on_settings_clicked)
        right_layout.addWidget(self.settings_btn)
        
        # 4. Помощь
        self.help_btn = self.create_menu_button("", self.on_help_clicked)
        right_layout.addWidget(self.help_btn)
        
        # 5. О программе
        self.about_btn = self.create_menu_button("", self.on_about_clicked)
        right_layout.addWidget(self.about_btn)
        
        # 6. Выход
        self.exit_btn = self.create_menu_button("", self.on_exit_clicked)
        right_layout.addWidget(self.exit_btn)
        
        right_layout.addStretch()
        right_panel.setLayout(right_layout)
        
        # Добавляем обе панели в главный layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        
        # Таймер для обновления статуса
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(5000)
        
        print(f"MenuWidget: создано {len(self.buttons)} кнопок")
    
    def create_menu_button(self, text, callback):
        """Создать стилизованную кнопку меню"""
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        btn.setMinimumHeight(60)
        
        btn_font = QFont()
        btn_font.setPointSize(14)
        btn_font.setBold(True)
        btn.setFont(btn_font)
        
        base_style = """
            QPushButton {
                background-color: rgba(0, 34, 0, 0.8);
                color: #00ff00;
                border: 2px solid #00ff00;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                min-height: 60px;
                border-radius: 8px;
                text-align: center;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: rgba(0, 68, 0, 0.9);
                border-color: #ffff00;
                color: #ffff00;
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
    
    def on_new_game_clicked(self):
        """Обработчик нажатия кнопки 'Новая игра'"""
        print("MenuWidget: нажата кнопка 'Новая игра'")
        self.new_game_clicked.emit()
    
    def on_load_game_clicked(self):
        """Обработчик нажатия кнопки 'Загрузить игру'"""
        print("MenuWidget: нажата кнопка 'Загрузить игру'")
        self.load_game_clicked.emit()
    
    def on_settings_clicked(self):
        """Обработчик нажатия кнопки 'Настройки'"""
        print("MenuWidget: нажата кнопка 'Настройки'")
        self.settings_clicked.emit()
    
    def on_help_clicked(self):
        """Обработчик нажатия кнопки 'Помощь'"""
        print("MenuWidget: нажата кнопка 'Помощь'")
        self.help_clicked.emit()
    
    def on_about_clicked(self):
        """Обработчик нажатия кнопки 'О программе'"""
        print("MenuWidget: нажата кнопка 'О программе'")
        self.about_clicked.emit()
    
    def on_exit_clicked(self):
        """Обработчик нажатия кнопки 'Выход'"""
        print("MenuWidget: нажата кнопка 'Выход'")
        self.exit_clicked.emit()
    
    def type_description(self):
        """Эффект печатной машинки для описания"""
        if self.typing_index < len(self.typing_text):
            char = self.typing_text[self.typing_index]
            current_text = self.description.text()
            self.description.setText(current_text + char)
            self.typing_index += 1
            
            # Звук печати (если доступен)
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
        print("MenuWidget: запуск анимаций")
        
        # Анимация для замка
        if hasattr(self, 'lock_label'):
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
            self.lock_animation.start()
        
        # Анимация для заголовка
        if hasattr(self, 'title_label'):
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
            self.title_animation.start()
        
        # Анимация для статуса
        if hasattr(self, 'status_label'):
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
            self.status_animation.start()
        
        # Анимация для заголовка меню
        if hasattr(self, 'menu_title'):
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
            self.menu_title_animation.setEasingCurve(QEasingCurve.InOutSine)
            self.menu_title_animation.start()
        
        # Анимация появления кнопок
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
        if not self.config.get("graphics", {}).get("enable_effects", True):
            return
        
        # Таймер для обновления эффектов
        self.effect_timer = QTimer()
        self.effect_timer.timeout.connect(self.update_effects)
        self.effect_timer.start(30)
        
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
        if self.config.get("graphics", {}).get("glitch_effects", True):
            self.glitch_timer = QTimer()
            self.glitch_timer.timeout.connect(self.trigger_random_effect)
            self.glitch_timer.start(3000)
    
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
        if not self.config.get("graphics", {}).get("enable_effects", True):
            return
        
        # Обновление частиц
        for particle in self.particles:
            particle['x'] += math.cos(particle['direction']) * particle['speed']
            particle['y'] += math.sin(particle['direction']) * particle['speed']
            particle['lifetime'] -= 1
            
            # Пересоздаем частицы, которые вышли за границы
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
        if not self.config.get("graphics", {}).get("enable_effects", True) or \
           not self.config.get("graphics", {}).get("glitch_effects", True):
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
            
            QTimer.singleShot(300, lambda: button.setStyleSheet(original_style))
    
    def paintEvent(self, event):
        """Отрисовка эффектов"""
        super().paintEvent(event)
        
        if not self.config.get("graphics", {}).get("enable_effects", True):
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
        if (self.config.get("graphics", {}).get("glitch_effects", True) and 
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
        status_messages = [
            translation.t("status.encrypting_channel", "Шифрование канала..."),
            translation.t("status.checking_access", "Проверка доступа..."),
            translation.t("status.sync_with_hq", "Синхронизация с HQ..."),
            translation.t("status.loading_missions", "Загрузка миссий..."),
            translation.t("status.connecting_to_global_network", "Подключение к глобальной сети..."),
            translation.t("status.checking_security_system", "Проверка системы безопасности..."),
            translation.t("status.loading_configuration", "Загрузка конфигурации..."),
            translation.t("status.initializing_terminal", "Инициализация терминала..."),
            translation.t("status.menu_idle", "Меню готово"),
            translation.t("status.virus_scan", "Сканирование на вирусы..."),
        ]
        
        current = self.status_label.text()
        available = [msg for msg in status_messages if msg != current]
        if available:
            new_status = random.choice(available)
            self.status_label.setText(new_status)
            
            if random.random() < 0.3:
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
    
    def update_translation(self):
        """Обновить переводы (вызывается из main_window)"""
        self.retranslate_ui()