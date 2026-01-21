from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, 
                               QLineEdit, QScrollBar, QFrame)
from PySide6.QtCore import Qt, QTimer, Signal, QPropertyAnimation, QPoint
from PySide6.QtGui import (QTextCursor, QColor, QTextCharFormat, QPainter, 
                          QLinearGradient, QRadialGradient, QPen, QBrush,
                          QFont, QFontMetrics)
import random
import math
import time

class TerminalWidget(QWidget):
    command_executed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history = []
        self.history_index = -1
        self.current_dir = "C:/Users/Employee"
        self.typing_timer = QTimer()
        self.typing_text = ""
        self.typing_index = 0
        self.typing_timer.timeout.connect(self._type_next_char)
        
        self.init_ui()
        self.setup_effects()
        self.show_welcome()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Создаем фрейм для терминала с градиентной границей
        self.terminal_frame = QFrame()
        self.terminal_frame.setStyleSheet("""
            QFrame {
                background-color: #000000;
                border: 2px solid transparent;
                border-radius: 5px;
            }
        """)
        
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(2, 2, 2, 2)
        
        # История команд
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #00ff00;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                border: none;
                padding: 10px;
                line-height: 1.2;
                selection-background-color: #003300;
            }
        """)
        
        # Ввод команды
        self.input = QLineEdit()
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #000000;
                color: #00ffff;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                border: 1px solid #008800;
                border-left: none;
                border-right: none;
                border-bottom: none;
                border-top: 1px solid #008800;
                padding: 8px;
                selection-background-color: #003333;
            }
            QLineEdit:focus {
                border-top: 2px solid #00ff00;
                color: #ffffff;
                background-color: #000a00;
            }
        """)
        self.input.returnPressed.connect(self.execute_command)
        
        frame_layout.addWidget(self.output)
        frame_layout.addWidget(self.input)
        self.terminal_frame.setLayout(frame_layout)
        
        layout.addWidget(self.terminal_frame)
        self.setLayout(layout)
        
    def setup_effects(self):
        """Настройка эффектов для терминала"""
        # Таймер для эффектов
        self.effect_timer = QTimer()
        self.effect_timer.timeout.connect(self.update_effects)
        self.effect_timer.start(50)  # 20 FPS
        
        # Эффект сканирующих линий
        self.scan_lines = []
        self.scan_line_y = 0
        self.scan_line_speed = 3
        
        # Эффект статического шума
        self.static_particles = []
        self.init_static_particles()
        
        # Эффект свечения
        self.glow_intensity = 0.5
        self.glow_pulse = 0.0
        self.glow_pulse_direction = 1
        
        # Эффект глитча
        self.glitch_active = False
        self.glitch_offset = 0
        self.glitch_timer = 0
        
        # Эффект матричных символов в углах
        self.matrix_symbols = ['░', '▒', '▓', '█', '▄', '▀', '▌', '▐']
        self.corner_symbols = []
        
    def init_static_particles(self):
        """Инициализация частиц статического шума"""
        self.static_particles = []
        for _ in range(30):
            self.static_particles.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'size': random.randint(1, 2),
                'alpha': random.randint(20, 80),
                'speed': random.uniform(0.5, 1.5),
                'direction': random.uniform(0, 2 * math.pi),
                'lifetime': random.randint(50, 150)
            })
        
    def update_effects(self):
        """Обновление всех эффектов"""
        # Обновление сканирующей линии
        self.scan_line_y = (self.scan_line_y + self.scan_line_speed) % (self.height() + 20)
        
        # Обновление статических частиц
        for particle in self.static_particles:
            particle['x'] += math.cos(particle['direction']) * particle['speed']
            particle['y'] += math.sin(particle['direction']) * particle['speed']
            particle['lifetime'] -= 1
            
            if (particle['x'] < 0 or particle['x'] > self.width() or 
                particle['y'] < 0 or particle['y'] > self.height() or
                particle['lifetime'] <= 0):
                particle.update({
                    'x': random.randint(0, self.width()),
                    'y': random.randint(0, self.height()),
                    'lifetime': random.randint(50, 150),
                    'alpha': random.randint(20, 80)
                })
        
        # Обновление пульсации свечения
        self.glow_pulse += 0.02 * self.glow_pulse_direction
        if self.glow_pulse >= 1.0:
            self.glow_pulse_direction = -1
            self.glow_pulse = 1.0
        elif self.glow_pulse <= 0.0:
            self.glow_pulse_direction = 1
            self.glow_pulse = 0.0
        
        # Обновление символов в углах
        if random.random() < 0.05:
            self.corner_symbols = []
            corners = [
                (5, 5, 0),  # левый верхний
                (self.width() - 15, 5, 1),  # правый верхний
                (5, self.height() - 15, 2),  # левый нижний
                (self.width() - 15, self.height() - 15, 3)  # правый нижний
            ]
            for x, y, corner_type in corners:
                self.corner_symbols.append({
                    'x': x,
                    'y': y,
                    'char': random.choice(self.matrix_symbols),
                    'color': QColor(0, random.randint(150, 255), 0, random.randint(100, 200)),
                    'lifetime': random.randint(10, 30),
                    'corner': corner_type
                })
        
        # Обновление символов в углах
        self.corner_symbols = [s for s in self.corner_symbols if s['lifetime'] > 0]
        for symbol in self.corner_symbols:
            symbol['lifetime'] -= 1
        
        self.update()
            
    def paintEvent(self, event):
        """Отрисовка эффектов терминала"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Эффект свечения границы
        self.draw_glow_effect(painter)
        
        # Сканирующие линии
        self.draw_scan_lines(painter)
        
        # Статический шум
        self.draw_static_noise(painter)
        
        # Глитч-эффект
        if self.glitch_active:
            self.draw_glitch_effect(painter)
        
        # Символы в углах
        self.draw_corner_symbols(painter)
        
        # Эффект виньетирования
        self.draw_vignette(painter)
        
    def draw_glow_effect(self, painter):
        """Рисование эффекта свечения"""
        width = self.width()
        height = self.height()
        
        # Внешнее свечение
        glow_opacity = 0.2 + 0.1 * math.sin(time.time() * 2)
        for i in range(3):
            glow_size = i * 3
            glow_color = QColor(0, 255, 0, int(50 * glow_opacity / (i + 1)))
            
            painter.setPen(QPen(glow_color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(glow_size, glow_size, 
                           width - 2*glow_size, 
                           height - 2*glow_size)
        
        # Пульсирующее свечение в углах
        corner_radius = 20
        pulse_value = 0.5 + 0.5 * math.sin(time.time() * 3)
        glow_color = QColor(0, 255, 0, int(100 * pulse_value))
        
        corners = [
            (0, 0),  # левый верхний
            (width, 0),  # правый верхний
            (0, height),  # левый нижний
            (width, height)  # правый нижний
        ]
        
        for x, y in corners:
            gradient = QRadialGradient(x, y, corner_radius)
            gradient.setColorAt(0, glow_color)
            gradient.setColorAt(1, QColor(0, 255, 0, 0))
            
            painter.setOpacity(0.3)
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(x - corner_radius, y - corner_radius, 
                              corner_radius * 2, corner_radius * 2)
        
    def draw_scan_lines(self, painter):
        """Рисование сканирующих линий"""
        width = self.width()
        
        # Основные линии
        line_spacing = 2
        painter.setOpacity(0.15)
        painter.setPen(QPen(QColor(0, 255, 0, 30), 1))
        
        for y in range(0, self.height(), line_spacing):
            # Добавляем легкое искажение
            distortion = math.sin(y * 0.01 + time.time()) * 1.5
            painter.drawLine(int(distortion), y, 
                           width + int(distortion), y)
        
        # Движущаяся линия сканирования
        scan_height = 20
        scan_gradient = QLinearGradient(0, self.scan_line_y, 0, self.scan_line_y + scan_height)
        scan_gradient.setColorAt(0, QColor(0, 255, 0, 0))
        scan_gradient.setColorAt(0.2, QColor(0, 255, 0, 150))
        scan_gradient.setColorAt(0.5, QColor(0, 255, 255, 200))
        scan_gradient.setColorAt(0.8, QColor(0, 255, 0, 150))
        scan_gradient.setColorAt(1, QColor(0, 255, 0, 0))
        
        painter.setOpacity(0.3)
        painter.fillRect(0, self.scan_line_y, width, scan_height, scan_gradient)
        
        # Свечение под линией сканирования
        painter.setOpacity(0.1)
        for i in range(3):
            glow_y = self.scan_line_y + scan_height + i * 2
            glow_alpha = 100 - i * 30
            painter.setPen(QPen(QColor(0, 255, 0, glow_alpha), 1))
            painter.drawLine(0, glow_y, width, glow_y)
        
    def draw_static_noise(self, painter):
        """Рисование статического шума"""
        painter.setOpacity(0.1)
        
        for particle in self.static_particles:
            alpha = particle['alpha'] * (particle['lifetime'] / 150.0)
            color = QColor(
                random.randint(0, 100),
                random.randint(200, 255),
                random.randint(0, 100),
                int(alpha)
            )
            
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawRect(
                int(particle['x']),
                int(particle['y']),
                particle['size'],
                particle['size']
            )
        
        # Крупные частицы шума
        for _ in range(5):
            x = random.randint(0, self.width())
            y = random.randint(0, self.height())
            size = random.randint(1, 3)
            alpha = random.randint(10, 30)
            color = QColor(0, 255, 0, alpha)
            
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawRect(x, y, size, size)
        
    def draw_glitch_effect(self, painter):
        """Рисование глитч-эффекта"""
        if not self.glitch_active:
            return
            
        width = self.width()
        height = self.height()
        
        # Сохраняем состояние painter
        painter.save()
        
        # Случайное смещение
        offset_x = self.glitch_offset
        offset_y = random.randint(-2, 2)
        painter.translate(offset_x, offset_y)
        
        # Цветное разложение (хроматическая аберрация)
        if random.random() < 0.5:
            # Красный канал
            painter.setCompositionMode(QPainter.CompositionMode_Plus)
            painter.setOpacity(0.2)
            painter.translate(1, 0)
            painter.setPen(QPen(QColor(255, 0, 0, 100), 1))
            painter.drawRect(0, 0, width, height)
            painter.translate(-1, 0)
            
            # Синий канал
            painter.translate(-1, 0)
            painter.setPen(QPen(QColor(0, 0, 255, 100), 1))
            painter.drawRect(0, 0, width, height)
            painter.translate(1, 0)
        
        # Вертикальные полосы разрыва
        for _ in range(random.randint(1, 3)):
            y = random.randint(0, height)
            height_segment = random.randint(5, 15)
            offset = random.randint(-3, 3)
            
            painter.save()
            painter.translate(offset, 0)
            painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
            painter.drawLine(0, y, width, y)
            painter.drawLine(0, y + height_segment, width, y + height_segment)
            painter.restore()
        
        painter.restore()
        
    def draw_corner_symbols(self, painter):
        """Рисование символов в углах"""
        painter.setFont(QFont("Consolas", 10))
        
        for symbol in self.corner_symbols:
            x = symbol['x']
            y = symbol['y']
            
            # Эффект дрожания для некоторых символов
            if random.random() < 0.3:
                x += random.randint(-1, 1)
                y += random.randint(-1, 1)
            
            painter.setPen(symbol['color'])
            painter.setOpacity(symbol['lifetime'] / 30.0)
            painter.drawText(x, y, symbol['char'])
        
        # Постоянные угловые метки
        corner_labels = [
            (5, 20, "┌─ ТЕРМИНАЛ МВД ─┐", QColor(0, 255, 0, 200)),
            (self.width() - 150, 20, "СЕКУРНОСТЬ: 87%", QColor(0, 255, 0, 150)),
            (5, self.height() - 10, "MINOS v.7.84", QColor(0, 255, 0, 180)),
            (self.width() - 120, self.height() - 10, "ДОСТУП: 5/10", QColor(0, 255, 0, 180))
        ]
        
        painter.setFont(QFont("Consolas", 8))
        for x, y, text, color in corner_labels:
            painter.setPen(color)
            painter.setOpacity(0.7)
            painter.drawText(x, y, text)
        
    def draw_vignette(self, painter):
        """Рисование эффекта виньетирования"""
        width = self.width()
        height = self.height()
        
        vignette = QRadialGradient(width/2, height/2, max(width, height)/1.5)
        vignette.setColorAt(0, QColor(0, 0, 0, 0))
        vignette.setColorAt(0.7, QColor(0, 0, 0, 0))
        vignette.setColorAt(1, QColor(0, 0, 0, 80))
        
        painter.setOpacity(0.3)
        painter.setBrush(vignette)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, width, height)
        
    def show_welcome(self):
        """Показать приветственное сообщение в стиле 1984"""
        employee_id = random.randint(1000, 9999)
        welcome = f"""
╔════════════════════════════════════════════════════════════════╗
║                 ДЕПАРТАМЕНТ МВД - СЕКТОР 7                     ║
║          МИНИСТЕРСТВО ВНУТРЕННИХ ДЕЛ - ОП УПРАВЛЕНИЕ           ║
║                                                                ║
║  Система: MINOS v.3.84 (Мониторинг и Надзор)                   ║
║  Пользователь: СОТРУДНИК #{employee_id}                        ║
║  Каталог: {self.current_dir}                                    ║
║  Уровень доступа: БАЗОВЫЙ (наблюдение)                         ║
║                                                                ║
║  Введите 'help' для списка команд                              ║
║  Введите 'status' для проверки статуса лояльности              ║
║  Введите 'report' для отправки отчета в МВД                    ║
╚════════════════════════════════════════════════════════════════╝

[СИСТЕМА] Внимание: Все действия записываются.
[СИСТЕМА] Лояльность проверяется ежечасно.

{self.current_dir}> 
"""
        self.output.setText(welcome)
        self.output.moveCursor(QTextCursor.MoveOperation.End)  # ИСПРАВЛЕНО
        self.input.setFocus()
        
    def _type_next_char(self):
        if self.typing_index < len(self.typing_text):
            char = self.typing_text[self.typing_index]
            self.output.insertPlainText(char)
            self.output.moveCursor(QTextCursor.MoveOperation.End)  # ИСПРАВЛЕНО
            self.typing_index += 1
        else:
            self.typing_timer.stop()
            self.input.setFocus()
            
    def type_text(self, text: str, speed: int = 15):
        self.typing_text = text
        self.typing_index = 0
        self.typing_timer.start(speed)
        
    def execute_command(self):
        command = self.input.text().strip()
        self.input.clear()
        
        if not command:
            return
            
        self.history.append(command)
        self.history_index = len(self.history)
        
        self.output.append(f"{self.current_dir}> {command}")
        
        result = self.process_command(command)
        if result:
            self.output.append(result)
            
        self.output.moveCursor(QTextCursor.MoveOperation.End)  # ИСПРАВЛЕНО
        self.command_executed.emit(command)
        
    def process_command(self, command: str) -> str:
        cmd = command.lower().split()[0]
        args = command.split()[1:] if len(command.split()) > 1 else []
        
        commands = {
            "help": self.cmd_help,
            "status": self.cmd_status,
            "report": lambda: self.cmd_report(args),
            "scan": self.cmd_scan,
            "connect": lambda: self.cmd_connect(args),
            "clear": self.cmd_clear,
            "dir": self.cmd_dir,
            "whoami": self.cmd_whoami,
            "loyalty": self.cmd_loyalty,
            "mvd": lambda: self.cmd_mvd(args),
            # Новые команды времени
            "time": self.cmd_time,
            "date": self.cmd_date,
            "время": self.cmd_time,
            "дата": self.cmd_date,
        }
        
        if cmd in commands:
            return commands[cmd]()
        else:
            return f"[ОШИБКА] Неизвестная команда: {cmd}"
            
    def cmd_help(self) -> str:
        return """
[СИСТЕМА МВД] Доступные команды:

  help         - Справка по командам
  status       - Проверить статус системы
  report [текст] - Отправить отчет в МВД
  scan         - Сканировать локальную сеть
  connect [ip] - Подключиться к устройству
  clear        - Очистить экран терминала
  dir          - Показать файлы в каталоге
  whoami       - Информация о текущем пользователе
  loyalty      - Проверить уровень лояльности
  mvd [код]    - Команды МВД (требуется авторизация)
  time / время - Текущее игровое время
  date / дата  - Текущая игровая дата
"""
    
    def cmd_status(self) -> str:
        status = """
[СТАТУС СИСТЕМЫ МВД]
• Система мониторинга: АКТИВНА
• Камеры наблюдения: 24/7 (87% покрытие)
• Микрофоны: АКТИВНЫ
• Анализ поведения: В РЕЖИМЕ РЕАЛЬНОГО ВРЕМЕНИ
• Лояльность персонала: ПРОВЕРЯЕТСЯ
• Сеть: СТАБИЛЬНА
• Соединение с ЦЕНТРАЛЬНЫМ СЕРВЕРОМ МВД: УСТАНОВЛЕНО
• Последняя проверка: Сегодня, 08:47

[ПРЕДУПРЕЖДЕНИЕ] Уровень лояльности: 74% (требует улучшения)
"""
        return status
        
    def cmd_report(self, args):
        if not args:
            return "[МВД] Укажите текст отчета: report [текст]"
        return f"[МВД] Отчет отправлен: {' '.join(args)}\n[МВД] Статус: ПРИНЯТО К РАССМОТРЕНИЮ"
        
    def cmd_scan(self) -> str:
        targets = [
            "192.168.1.1  - МАРШРУТИЗАТОР МВД",
            "192.168.1.10 - ТЕРМИНАЛ НАБЛЮДЕНИЯ",
            "192.168.1.15 - БАЗА ДАННЫХ КАДРОВ",
            "192.168.1.20 - БАЗА ДАННЫХ ВРЕМЕНИ (системные часы)",
            "192.168.1.25 - СИСТЕМА БЕЗОПАСНОСТИ А",
            "192.168.1.30 - СИСТЕМА БЕЗОПАСНОСТИ Б",
            "192.168.1.35 - СЕРВЕР ЛОЯЛЬНОСТИ",
            "192.168.1.40 - ТЕЛЕЭКРАН УПРАВЛЕНИЯ",
        ]
        result = "[МВД] Сканирование сети...\n"
        result += "[МВД] Обнаружены устройства:\n"
        for target in targets:
            result += f"  • {target}\n"
        result += "[МВД] Сканирование завершено."
        return result
        
    def cmd_connect(self, args):
        if not args:
            return "[МВД] Укажите IP адрес: connect [ip]"
        return f"[МВД] Подключение к {args[0]}...\n[МВД] Статус: ДОСТУП ОГРАНИЧЕН"
        
    def cmd_clear(self):
        self.output.clear()
        self.show_welcome()
        return ""
        
    def cmd_dir(self):
        files = [
            "ОТЧЕТ_ЛОЯЛЬНОСТИ_ДЕНЬ7.txt",
            "ПРИКАЗ_МВД_№847.pdf",
            "ИНСТРУКЦИЯ_ПОВЕДЕНИЯ.doc",
            "ФОРМА_ОТЧЕТА_МВД.xls",
            "СПИСОК_СОТРУДНИКОВ.csv",
            "ПРОТОКОЛ_НАБЛЮДЕНИЯ.log",
            "СИСТЕМНЫЕ_ЧАСЫ.log",
            "КАЛЕНДАРЬ_МВД.dat",
        ]
        result = "[СИСТЕМА] Содержимое каталога:\n"
        for file in files:
            result += f"  - {file}\n"
        return result
        
    def cmd_whoami(self):
        return """
[ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ]
• Идентификатор: СОТРУДНИК #7824
• Уровень доступа: БАЗОВЫЙ (5 из 10)
• Департамент: ОТДЕЛ НАБЛЮДЕНИЙ
• Должность: МЛАДШИЙ АНАЛИТИК
• Дата найма: 15.11.2024
• Лояльность: 74% (требует улучшения)
• Нарушения: 0
• Поощрения: 2

[ОГРАНИЧЕНИЯ]
• Доступ только к базовым функциям
• Отсутствие доступа к архивам МВД
• Мониторинг активности: ВКЛЮЧЕН
"""
    
    def cmd_loyalty(self):
        loyalty = random.randint(65, 85)
        messages = [
            f"[МВД] Уровень лояльности: {loyalty}%",
            "[МВД] Анализ поведения...",
            "[МВД] Проверка социальных связей...",
            "[МВД] Анализ высказываний...",
            f"[МВД] ИТОГ: {loyalty}% лояльности",
        ]
        
        if loyalty < 70:
            messages.append("[МВД] ПРЕДУПРЕЖДЕНИЕ: Низкий уровень лояльности")
            messages.append("[МВД] РЕКОМЕНДАЦИЯ: Посетите семинар 'Мысли правильно'")
        elif loyalty < 80:
            messages.append("[МВД] Статус: УДОВЛЕТВОРИТЕЛЬНО")
            messages.append("[МВД] Продолжайте в том же духе")
        else:
            messages.append("[МВД] Статус: ОТЛИЧНО")
            messages.append("[МВД] Вы - пример для других сотрудников")
            
        return "\n".join(messages)
    
    def cmd_mvd(self, args):
        if not args:
            return "[МВД] Требуется код авторизации"
            
        if args[0] == "8472":
            return """
[МВД] АВТОРИЗАЦИЯ ПРОЙДЕНА
[МВД] ДОСТУП К СИСТЕМЕ МВД РАЗРЕШЕН

Доступные команды МВД:
• mvd surveillance [id] - Просмотр камеры наблюдения
• mvd profile [id] - Просмотр досье сотрудника
• mvd report_all - Все отчеты отдела
• mvd analyze [id] - Анализ лояльности сотрудника
• mvd alert [уровень] - Изменить уровень тревоги
• mvd time [команда] - Управление системным временем
"""
        else:
            return "[МВД] ОШИБКА: Неверный код авторизации"
    
    # НОВЫЕ КОМАНДЫ ВРЕМЕНИ
    
    def cmd_time(self) -> str:
        """Показать текущее игровое время"""
        try:
            # Ищем game_widget среди родителей
            widget = self
            while widget and not hasattr(widget, 'game_state'):
                widget = widget.parent()
                
            if widget and hasattr(widget, 'game_state') and widget.game_state:
                game_state = widget.game_state
                
                # Получаем время из game_state
                time_str = game_state.get_formatted_time()
                progress = game_state.get_workday_progress()
                current_hour = game_state.game_time.get('current_hour', 9)
                hours_left = 18 - current_hour
                
                # Определяем часть дня
                if current_hour < 12:
                    time_of_day = "УТРО"
                elif current_hour < 15:
                    time_of_day = "ДЕНЬ"
                elif current_hour < 18:
                    time_of_day = "ВЕЧЕР"
                else:
                    time_of_day = "ВНЕ РАБОЧЕГО ВРЕМЕНИ"
                
                # Форматируем вывод
                time_display = f"""
┌─────────── ВРЕМЯ СИСТЕМЫ МВД ───────────┐
│ Текущее время:        {time_str}          │
│ Часть дня:            {time_of_day:20s} │
│ Прогресс смены:      {progress:6.1f}%            │
│ До конца смены:      {hours_left:2d} ч.          │
│ Статус времени:      {'⏹ ПАУЗА' if game_state.game_time.get('is_paused', False) else '▶ АКТИВНО'} │
│ Скорость времени:    {game_state.game_time.get('time_speed', 1.0):.1f}x      │
└──────────────────────────────────────────┘
"""
                return time_display
            else:
                return "[ОШИБКА] Не удалось получить доступ к игровому времени\n[СИСТЕМА] Используйте: 09:00"
        except Exception as e:
            return f"[ОШИБКА] {str(e)}\n[СИСТЕМА] Время по умолчанию: 09:00"
    
    def cmd_date(self) -> str:
        """Показать текущую игровую дату"""
        try:
            # Ищем game_widget среди родителей
            widget = self
            while widget and not hasattr(widget, 'game_state'):
                widget = widget.parent()
                
            if widget and hasattr(widget, 'game_state') and widget.game_state:
                game_state = widget.game_state
                
                # Получаем дату из game_state
                date_str = game_state.get_formatted_date()
                day = game_state.game_time.get('day', 1)
                month = game_state.game_time.get('month', 1)
                year = game_state.game_time.get('year', 1984)
                
                # Название месяца (русские)
                month_names = {
                    1: "ЯНВАРЬ", 2: "ФЕВРАЛЬ", 3: "МАРТ", 4: "АПРЕЛЬ", 
                    5: "МАЙ", 6: "ИЮНЬ", 7: "ИЮЛЬ", 8: "АВГУСТ", 
                    9: "СЕНТЯБРЬ", 10: "ОКТЯБРЬ", 11: "НОЯБРЬ", 12: "ДЕКАБРЬ"
                }
                month_name = month_names.get(month, "НЕИЗВЕСТНО")
                
                # Определяем день недели (упрощенно)
                day_of_week = ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", 
                              "ПЯТНИЦА", "СУББОТА", "ВОСКРЕСЕНЬЕ"][(day - 1) % 7]
                
                date_display = f"""
┌─────────── КАЛЕНДАРЬ МВД ───────────┐
│ Текущая дата:   {date_str}           │
│ День недели:    {day_of_week:15s} │
│ Рабочий день:   {day:3d}                 │
│ Месяц:          {month_name:15s} │
│ Год:            {year}                │
│                                    │
│ Рабочие часы:   09:00 - 18:00      │
│ Обед:           13:00 - 14:00      │
└──────────────────────────────────────┘
"""
                return date_display
            else:
                return "[ОШИБКА] Не удалось получить доступ к игровой дате\n[СИСТЕМА] Используйте: 01.01.1984"
        except Exception as e:
            return f"[ОШИБКА] {str(e)}\n[СИСТЕМА] Дата по умолчанию: 01.01.1984"

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            if self.history and self.history_index > 0:
                self.history_index -= 1
                self.input.setText(self.history[self.history_index])
        elif event.key() == Qt.Key_Down:
            if self.history and self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.input.setText(self.history[self.history_index])
            else:
                self.history_index = len(self.history)
                self.input.clear()
        else:
            super().keyPressEvent(event)