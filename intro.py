# intro.py - Исправленный метод draw_logo для полного отображения текста
import sys
import random
import math
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class HolographicSphere:
    """Голографическая сфера с улучшенными эффектами"""
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.base_radius = radius
        self.radius = radius
        self.rotation = 0
        self.pulse = 0
        self.ring_count = 12
        
        # Цвета в сине-голубой гамме
        self.colors = [
            QColor(0, 120, 255, 200),
            QColor(0, 180, 255, 170),
            QColor(100, 220, 255, 140),
            QColor(200, 240, 255, 100),
            QColor(255, 255, 255, 60)
        ]
        
        self.inner_rings = []
        self.init_inner_rings()
        
    def init_inner_rings(self):
        """Инициализация внутренних колец"""
        self.inner_rings = []
        for i in range(4):
            self.inner_rings.append({
                'radius': self.base_radius * (0.2 + i * 0.15),
                'rotation': i * 45,
                'speed': 0.3 + i * 0.2,
                'color': self.colors[i % len(self.colors)]
            })
        
    def update(self):
        """Обновление анимации сферы"""
        self.rotation = (self.rotation + 0.3) % 360
        self.pulse = (self.pulse + 0.02) % (math.pi * 2)
        self.radius = self.base_radius * (0.92 + 0.08 * math.sin(self.pulse * 2))
        
        for ring in self.inner_rings:
            ring['rotation'] = (ring['rotation'] + ring['speed']) % 360
            
    def draw(self, painter):
        """Отрисовка голографической сферы"""
        painter.save()
        painter.translate(self.x, self.y)
        
        # Внешнее свечение
        glow_radius = self.radius * 2.5
        glow_gradient = QRadialGradient(0, 0, glow_radius)
        glow_gradient.setColorAt(0, QColor(0, 120, 255, 40))
        glow_gradient.setColorAt(0.7, QColor(0, 120, 255, 15))
        glow_gradient.setColorAt(1, QColor(0, 120, 255, 0))
        
        painter.setBrush(QBrush(glow_gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-glow_radius, -glow_radius, 
                           glow_radius * 2, glow_radius * 2)
        
        # Внутренние кольца
        for ring in self.inner_rings:
            painter.save()
            painter.rotate(ring['rotation'])
            
            ring_gradient = QRadialGradient(0, 0, ring['radius'])
            ring_gradient.setColorAt(0, ring['color'])
            ring_gradient.setColorAt(0.7, QColor(ring['color'].red(), 
                                                ring['color'].green(), 
                                                ring['color'].blue(), 
                                                ring['color'].alpha() // 2))
            ring_gradient.setColorAt(1, Qt.transparent)
            
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QBrush(ring_gradient), 3))
            painter.drawEllipse(-ring['radius'], -ring['radius'], 
                               ring['radius'] * 2, ring['radius'] * 2)
            painter.restore()
        
        # Основные кольца
        for i in range(self.ring_count):
            angle = i * (360 / self.ring_count) + self.rotation
            radius = self.radius * (0.8 + 0.2 * math.sin(self.pulse + i * 0.3))
            
            painter.save()
            painter.rotate(angle)
            
            gradient = QLinearGradient(-radius, 0, radius, 0)
            alpha = int(180 * (1 - i/self.ring_count))
            
            color_idx = i % len(self.colors)
            color = self.colors[color_idx]
            color.setAlpha(alpha)
            
            gradient.setColorAt(0, Qt.transparent)
            gradient.setColorAt(0.3, color)
            gradient.setColorAt(0.7, color)
            gradient.setColorAt(1, Qt.transparent)
            
            painter.setPen(QPen(QBrush(gradient), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(-radius, -radius, radius*2, radius*2)
            painter.restore()
            
        # Центральная точка
        center_size = 20 + 5 * math.sin(self.pulse * 3)
        center_gradient = QRadialGradient(0, 0, center_size)
        center_gradient.setColorAt(0, QColor(255, 255, 255, 220))
        center_gradient.setColorAt(0.5, QColor(0, 180, 255, 150))
        center_gradient.setColorAt(1, QColor(0, 120, 255, 0))
        
        painter.setBrush(QBrush(center_gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-center_size//2, -center_size//2, 
                           center_size, center_size)
        
        # Лучи
        for i in range(16):
            angle = i * (360 / 16) + self.rotation * 1.5
            length = self.radius * (1.2 + 0.3 * math.sin(self.pulse * 1.5 + i * 0.4))
            
            painter.save()
            painter.rotate(angle)
            
            ray_length = center_size // 2 + 5
            ray_gradient = QLinearGradient(ray_length, 0, length, 0)
            ray_alpha = int(120 + 80 * math.sin(self.pulse * 2 + i * 0.2))
            ray_gradient.setColorAt(0, QColor(255, 255, 255, ray_alpha))
            ray_gradient.setColorAt(0.5, QColor(100, 220, 255, ray_alpha // 2))
            ray_gradient.setColorAt(1, Qt.transparent)
            
            painter.setPen(QPen(QBrush(ray_gradient), 1.5))
            painter.drawLine(ray_length, 0, int(length), 0)
            painter.restore()
            
        painter.restore()

class IntroScreen(QWidget):
    """Стабильное и надежное интро с исправленным отображением текста"""
    finished = Signal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sikorsky's Incorporated - System Initialization")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Цветовая схема
        self.primary_color = QColor(0, 120, 255)
        self.secondary_color = QColor(0, 180, 255)
        self.accent_color = QColor(100, 220, 255)
        self.bg_color = QColor(10, 15, 25)
        self.text_color = QColor(240, 245, 255)
        self.dim_text_color = QColor(180, 200, 230)
        
        # Состояния анимации
        self.phase = 0  # 0: появление, 1: основной экран, 2: исчезновение
        self.opacity = 0.0
        self.time = 0.0
        self.global_timer = 0
        
        # Элементы
        self.sphere = None
        self.particles = []
        self.scan_lines = []
        self.grid_dots = []
        
        # Текст
        self.company_name = "SIKORSKY'S INCORPORATED"
        self.system_name = "PANOPTICUM SECURITY SYSTEM"
        self.version = "v7.3.2 // CLEARANCE: OMEGA-9"
        
        self.messages = [
            "Initializing neural network protocols...",
            "Establishing quantum encrypted channels...",
            "Loading advanced threat detection AI...",
            "Calibrating biometric recognition systems...",
            "Syncing with global surveillance grid...",
            "Verifying security clearance: OMEGA-9...",
            "Activating PANOPTICUM monitoring modules...",
            "Deploying countermeasure systems...",
            "Optimizing real-time data processing...",
            "Securing all communication lines...",
            "Testing system integrity protocols...",
            "Finalizing initialization sequence..."
        ]
        self.current_message = 0
        self.message_progress = 0
        self.message_chars_typed = 0
        self.typing_speed = 2
        
        # Таймеры
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        
        self.message_timer = QTimer()
        self.message_timer.timeout.connect(self.update_message)
        
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self.update_fade)
        
        # Флаги состояния
        self.is_initialized = False
        self.is_running = False
        
    def start_intro(self, duration=8000):
        """Запуск интро - исправленная версия"""
        if self.is_running:
            self.cleanup()
            
        # Остановка всех таймеров перед запуском
        self.animation_timer.stop()
        self.message_timer.stop()
        self.fade_timer.stop()
        
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        # Инициализация элементов
        self.initialize_elements()
        
        # Сброс состояния
        self.phase = 0
        self.opacity = 0.0
        self.time = 0.0
        self.global_timer = 0
        self.current_message = 0
        self.message_progress = 0
        self.message_chars_typed = 0
        self.is_running = True
        
        # Запуск таймеров
        self.animation_timer.start(16)  # 60 FPS
        self.message_timer.start(100)   # Сообщения
        self.fade_timer.start(30)       # Плавное появление
        
        # Автозакрытие
        QTimer.singleShot(duration, self.start_fade_out)
        
        # Показываем окно
        self.show()
        self.raise_()
        self.activateWindow()
        
    def initialize_elements(self):
        """Инициализация графических элементов"""
        center_x = self.width() // 2
        center_y = self.height() // 3
        
        # Создание голографической сферы
        self.sphere = HolographicSphere(center_x, center_y, 120)
        
        # Создание частиц
        self.particles = []
        particle_count = min(100, (self.width() * self.height()) // 5000)
        for _ in range(particle_count):
            self.particles.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'size': random.uniform(1.0, 2.5),
                'speed_x': random.uniform(-0.5, 0.5),
                'speed_y': random.uniform(-0.5, 0.5),
                'color': random.choice([
                    QColor(0, 120, 255, 100),
                    QColor(0, 180, 255, 80),
                    QColor(100, 220, 255, 60),
                    QColor(200, 240, 255, 40)
                ]),
                'phase': random.uniform(0, math.pi * 2)
            })
            
        # Инициализация точек сетки
        self.init_grid_dots()
        
    def init_grid_dots(self):
        """Инициализация точек сетки"""
        self.grid_dots = []
        cell_size = 60
        cols = self.width() // cell_size + 1
        rows = self.height() // cell_size + 1
        
        for col in range(cols):
            for row in range(rows):
                x = col * cell_size
                y = row * cell_size
                
                self.grid_dots.append({
                    'x': x,
                    'y': y,
                    'size': random.uniform(0.5, 1.5),
                    'alpha': random.randint(10, 30),
                    'phase': random.uniform(0, math.pi * 2)
                })
                
    def start_fade_out(self):
        """Начало исчезновения"""
        if self.phase != 2 and self.is_running:
            self.phase = 2
            
    def cleanup(self):
        """Очистка ресурсов"""
        self.animation_timer.stop()
        self.message_timer.stop()
        self.fade_timer.stop()
        
        self.particles.clear()
        self.scan_lines.clear()
        self.grid_dots.clear()
        self.sphere = None
        
        self.is_running = False
        
    def update_fade(self):
        """Обновление плавного появления/исчезновения"""
        if self.phase == 0:  # Появление
            self.opacity = min(1.0, self.opacity + 0.03)
            if self.opacity >= 1.0:
                self.phase = 1
        elif self.phase == 2:  # Исчезновение
            self.opacity = max(0.0, self.opacity - 0.04)
            if self.opacity <= 0.0:
                self.cleanup()
                self.finished.emit()
                
        self.update()
        
    def update_animation(self):
        """Обновление всех анимаций"""
        self.time += 0.04
        self.global_timer += 1
        
        # Обновление сферы
        if self.sphere:
            self.sphere.update()
            
        # Обновление частиц
        for particle in self.particles:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['phase'] += 0.02
            
            # Отражение от границ
            if particle['x'] < 0 or particle['x'] > self.width():
                particle['speed_x'] *= -1
            if particle['y'] < 0 or particle['y'] > self.height():
                particle['speed_y'] *= -1
                
        # Обновление точек сетки
        for dot in self.grid_dots:
            dot['phase'] += 0.01
            dot['alpha'] = 15 + int(10 * math.sin(self.time + dot['phase']))
            
        # Обновление scan lines
        if random.random() < 0.1:
            self.scan_lines.append({
                'y': random.randint(0, self.height()),
                'height': random.randint(3, 8),
                'alpha': 80,
                'speed': random.uniform(1.0, 2.0)
            })
            
        for line in self.scan_lines[:]:
            line['alpha'] -= 5
            line['y'] += line['speed']
            if line['alpha'] <= 0:
                self.scan_lines.remove(line)
                
        self.update()
        
    def update_message(self):
        """Обновление системных сообщений"""
        if self.phase != 1 or not self.is_running:
            return
            
        if self.current_message < len(self.messages):
            current_msg = self.messages[self.current_message]
            
            if self.message_chars_typed < len(current_msg):
                self.message_chars_typed += self.typing_speed
            else:
                if self.message_progress < 100:
                    self.message_progress += 2
                else:
                    self.current_message += 1
                    self.message_chars_typed = 0
                    self.message_progress = 0
                    
    def paintEvent(self, event):
        """Отрисовка интерфейса"""
        if not self.is_running:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Установка общей прозрачности
        painter.setOpacity(self.opacity)
        
        # Фон
        self.draw_background(painter)
        
        # Сетка
        self.draw_grid_dots(painter)
        
        # Частицы
        self.draw_particles(painter)
        
        # Голографическая сфера
        if self.sphere:
            painter.save()
            painter.setOpacity(0.8 * self.opacity)
            self.sphere.draw(painter)
            painter.restore()
            
        # Scan lines
        self.draw_scan_lines(painter)
        
        # Основной контент
        self.draw_logo(painter)
        self.draw_messages(painter)
        self.draw_status(painter)
        self.draw_skip_hint(painter)
        
    def draw_background(self, painter):
        """Отрисовка фона"""
        # Основной градиент
        main_gradient = QLinearGradient(0, 0, 0, self.height())
        main_gradient.setColorAt(0, QColor(5, 10, 25))
        main_gradient.setColorAt(0.5, QColor(10, 18, 40))
        main_gradient.setColorAt(1, QColor(15, 25, 55))
        painter.fillRect(self.rect(), main_gradient)
        
    def draw_grid_dots(self, painter):
        """Отрисовка точек сетки"""
        for dot in self.grid_dots:
            color = QColor(100, 160, 255, dot['alpha'])
            painter.setPen(QPen(color, dot['size']))
            painter.drawPoint(int(dot['x']), int(dot['y']))
            
    def draw_particles(self, painter):
        """Отрисовка частиц"""
        for particle in self.particles:
            # Мерцание
            alpha = int(particle['color'].alpha() * (0.7 + 0.3 * math.sin(particle['phase'])))
            color = QColor(particle['color'])
            color.setAlpha(alpha)
            
            painter.setPen(QPen(color, particle['size']))
            painter.drawPoint(int(particle['x']), int(particle['y']))
            
    def draw_scan_lines(self, painter):
        """Отрисовка сканирующих линий"""
        for line in self.scan_lines:
            alpha = line['alpha'] / 255.0 * self.opacity * 0.6
            painter.setOpacity(alpha)
            
            line_gradient = QLinearGradient(0, line['y'], 0, line['y'] + line['height'])
            line_gradient.setColorAt(0, Qt.transparent)
            line_gradient.setColorAt(0.5, QColor(0, 180, 255, 150))
            line_gradient.setColorAt(1, Qt.transparent)
            
            painter.fillRect(
                0, int(line['y']),
                self.width(), int(line['height']),
                QBrush(line_gradient)
            )
        painter.setOpacity(self.opacity)
        
    def draw_logo(self, painter):
        """ИСПРАВЛЕННЫЙ МЕТОД: Отрисовка логотипа с правильными отступами"""
        center_x = self.width() // 2
        center_y = self.height() // 3
        
        # Название компании
        painter.setFont(QFont("Arial", 36, QFont.Bold))
        
        # Рассчитываем необходимую ширину для полного отображения текста
        font_metrics = painter.fontMetrics()
        text_width = font_metrics.horizontalAdvance(self.company_name)
        
        # Добавляем отступы по 40 пикселей с каждой стороны для надежности
        rect_width = text_width + 80
        rect_x = center_x - rect_width // 2
        
        # Тень
        shadow_color = QColor(0, 0, 0, 80)
        painter.setPen(QPen(shadow_color, 4))
        painter.drawText(
            rect_x, center_y - 15,
            rect_width, 60,
            Qt.AlignCenter,
            self.company_name
        )
        
        # Основной текст с градиентом
        text_gradient = QLinearGradient(
            rect_x, center_y - 15,
            rect_x + rect_width, center_y + 45
        )
        text_gradient.setColorAt(0, self.primary_color)
        text_gradient.setColorAt(0.5, self.secondary_color)
        text_gradient.setColorAt(1, self.accent_color)
        
        painter.setPen(QPen(QBrush(text_gradient), 3))
        painter.drawText(
            rect_x, center_y - 15,
            rect_width, 60,
            Qt.AlignCenter,
            self.company_name
        )
        
        # Подчеркивание - делаем на 20% шире текста
        line_width = rect_width * 1.2
        line_y = center_y + 35
        
        line_gradient = QLinearGradient(
            center_x - line_width/2, line_y,
            center_x + line_width/2, line_y
        )
        line_gradient.setColorAt(0, Qt.transparent)
        line_gradient.setColorAt(0.3, self.accent_color)
        line_gradient.setColorAt(0.7, self.accent_color)
        line_gradient.setColorAt(1, Qt.transparent)
        
        painter.setPen(QPen(QBrush(line_gradient), 2))
        painter.drawLine(
            int(center_x - line_width/2), line_y,
            int(center_x + line_width/2), line_y
        )
        
        # Название системы
        painter.setFont(QFont("Segoe UI Light", 20))
        painter.setPen(QPen(self.text_color, 2))
        
        # Рассчитываем ширину для системного названия
        system_font_metrics = painter.fontMetrics()
        system_text_width = system_font_metrics.horizontalAdvance(self.system_name)
        system_rect_width = system_text_width + 60  # Отступы поменьше
        system_rect_x = center_x - system_rect_width // 2
        
        painter.drawText(
            system_rect_x, center_y + 60,
            system_rect_width, 35,
            Qt.AlignCenter,
            self.system_name
        )
        
        # Версия
        version_alpha = 120 + int(80 * math.sin(self.time * 2))
        painter.setFont(QFont("Consolas", 12))
        
        # Рассчитываем ширину для версии
        version_font_metrics = painter.fontMetrics()
        version_text_width = version_font_metrics.horizontalAdvance(self.version)
        version_rect_width = version_text_width + 40
        version_rect_x = center_x - version_rect_width // 2
        
        painter.setPen(QPen(QColor(180, 220, 255, version_alpha), 1))
        painter.drawText(
            version_rect_x, center_y + 100,
            version_rect_width, 25,
            Qt.AlignCenter,
            self.version
        )
        
    def draw_messages(self, painter):
        """Отрисовка системных сообщений"""
        start_x = self.width() // 4
        start_y = self.height() // 2 + 40
        
        painter.setFont(QFont("Consolas", 14))
        
        # Отображение текущего сообщения
        if self.current_message < len(self.messages):
            message = self.messages[self.current_message]
            chars_to_show = min(self.message_chars_typed, len(message))
            display_text = message[:chars_to_show]
            
            # Рассчитываем ширину для сообщения
            font_metrics = painter.fontMetrics()
            prefix_width = font_metrics.horizontalAdvance("> ")
            text_width = font_metrics.horizontalAdvance(display_text)
            total_width = prefix_width + text_width
            
            # Добавляем отступы
            message_width = total_width + 40
            message_x = start_x
            
            # Текст сообщения
            text_y = start_y
            painter.setPen(QPen(self.text_color, 2))
            painter.drawText(
                message_x, text_y,
                message_width, 30,
                Qt.AlignLeft,
                "> " + display_text
            )
            
            # Курсор
            if chars_to_show < len(message):
                cursor_x = message_x + total_width + 5
                cursor_alpha = int(255 * (0.5 + 0.5 * math.sin(self.time * 15)))
                
                painter.fillRect(
                    cursor_x, text_y - 15,
                    10, 30,
                    QColor(255, 255, 255, cursor_alpha)
                )
                
        # Предыдущие сообщения
        for i in range(1, 4):
            idx = self.current_message - i
            if idx >= 0:
                message = self.messages[idx]
                alpha = 200 - i * 50
                offset_y = -i * 35
                
                # Рассчитываем ширину для предыдущих сообщений
                font_metrics = painter.fontMetrics()
                prefix_width = font_metrics.horizontalAdvance("✓ ")
                text_width = font_metrics.horizontalAdvance(message)
                total_width = prefix_width + text_width
                
                prev_width = total_width + 20
                
                painter.setPen(QPen(QColor(200, 230, 255, alpha), 1))
                painter.drawText(
                    start_x, start_y + offset_y,
                    prev_width, 30,
                    Qt.AlignLeft,
                    "✓ " + message
                )
                
    def draw_status(self, painter):
        """Отрисовка статусной панели"""
        panel_y = self.height() - 120
        panel_width = self.width() - 200
        
        # Фон панели
        painter.fillRect(
            100, panel_y,
            panel_width, 80,
            QColor(0, 0, 0, 50)
        )
        
        # Прогресс-бар
        progress_width = panel_width - 40
        progress = 0.3 + 0.7 * ((self.global_timer % 300) / 300)
        fill_width = int(progress_width * progress)
        
        # Фон прогресс-бара
        painter.fillRect(
            120, panel_y + 25,
            progress_width, 10,
            QColor(255, 255, 255, 20)
        )
        
        # Заполнение
        fill_gradient = QLinearGradient(120, panel_y + 25, 
                                        120 + fill_width, panel_y + 25 + 10)
        fill_gradient.setColorAt(0, self.primary_color)
        fill_gradient.setColorAt(0.5, self.secondary_color)
        fill_gradient.setColorAt(1, self.accent_color)
        
        painter.fillRect(
            120, panel_y + 25,
            fill_width, 10,
            QBrush(fill_gradient)
        )
        
        # Сканирующая линия
        scan_pos = 120 + int(progress_width * ((self.time * 1.5) % 1.0))
        scan_gradient = QLinearGradient(scan_pos - 25, panel_y + 20, 
                                        scan_pos + 25, panel_y + 40)
        scan_gradient.setColorAt(0, Qt.transparent)
        scan_gradient.setColorAt(0.5, QColor(255, 255, 255, 150))
        scan_gradient.setColorAt(1, Qt.transparent)
        
        painter.fillRect(
            scan_pos - 25, panel_y + 20,
            50, 20,
            QBrush(scan_gradient)
        )
        
        # Статус текста
        status_texts = [
            "Initializing security protocols...",
            "Authenticating with central server...",
            "Connecting to secure network...",
            "Synchronizing surveillance systems...",
            "Optimizing threat detection...",
            "Finalizing system checks..."
        ]
        status_idx = int(self.time * 0.3) % len(status_texts)
        
        # Рассчитываем ширину для статуса
        painter.setFont(QFont("Segoe UI", 12))
        font_metrics = painter.fontMetrics()
        status_text = "Status: " + status_texts[status_idx]
        status_width = font_metrics.horizontalAdvance(status_text) + 20
        
        painter.setPen(QPen(self.text_color, 1))
        painter.drawText(
            120, panel_y + 60,
            status_width, 25,
            Qt.AlignLeft,
            status_text
        )
        
        # Процент
        percent = int(progress * 100)
        percent_text = f"{percent:03d}%"
        percent_width = font_metrics.horizontalAdvance(percent_text) + 10
        
        painter.drawText(
            120 + progress_width - percent_width, panel_y + 60,
            percent_width, 25,
            Qt.AlignRight,
            percent_text
        )
        
    def draw_skip_hint(self, painter):
        """Отрисовка подсказки для пропуска"""
        if self.phase != 1:
            return
            
        skip_alpha = int(120 + 80 * math.sin(self.time * 3))
        hint_y = self.height() - 30
        
        painter.setFont(QFont("Segoe UI", 10))
        painter.setPen(QPen(QColor(255, 255, 255, skip_alpha), 1))
        painter.drawText(
            0, hint_y,
            self.width(), 30,
            Qt.AlignCenter,
            "Press any key or click to continue"
        )
        
    def keyPressEvent(self, event):
        """Пропуск по нажатию клавиши"""
        if self.is_running and self.phase == 1:
            self.start_fade_out()
            
    def mousePressEvent(self, event):
        """Пропуск по клику мыши"""
        if self.is_running and self.phase == 1:
            self.start_fade_out()
            
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self.cleanup()
        event.accept()


# Простая демонстрация
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    intro = IntroScreen()
    
    def on_finished():
        intro.close()
        app.quit()
        
    intro.finished.connect(on_finished)
    
    # Запускаем интро
    QTimer.singleShot(100, lambda: intro.start_intro(10000))
    
    sys.exit(app.exec())