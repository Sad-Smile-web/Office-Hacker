# ui/effects.py
from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PySide6.QtCore import QTimer, QPropertyAnimation, Qt, QPoint, QRect, QEasingCurve
from PySide6.QtGui import (QPainter, QLinearGradient, QColor, QPen, QBrush, 
                          QFont, QFontMetrics, QRadialGradient, QConicalGradient,
                          QPixmap, QImage)
import random
import math
import time
from enum import Enum

class EffectType(Enum):
    GLITCH = "glitch"
    SCAN_LINES = "scan_lines"
    MATRIX_RAIN = "matrix_rain"
    PIXELATE = "pixelate"
    BLOOM = "bloom"
    VHS = "vhs"
    CHROMA = "chroma"
    STATIC = "static"
    WAVE = "wave"
    RAINBOW = "rainbow"

class AdvancedEffects:
    """Класс для управления всеми эффектами"""
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.effects = {}
        self.active_effects = set()
        self.intensity = 1.0
        
        # Конфигурация эффектов
        self.config = {
            EffectType.GLITCH: {"enabled": True, "intensity": 0.3},
            EffectType.SCAN_LINES: {"enabled": True, "intensity": 0.2},
            EffectType.MATRIX_RAIN: {"enabled": False, "intensity": 0.5},
            EffectType.PIXELATE: {"enabled": False, "intensity": 0.1},
            EffectType.BLOOM: {"enabled": True, "intensity": 0.4},
            EffectType.VHS: {"enabled": True, "intensity": 0.3},
            EffectType.CHROMA: {"enabled": True, "intensity": 0.2},
            EffectType.STATIC: {"enabled": True, "intensity": 0.15},
            EffectType.WAVE: {"enabled": True, "intensity": 0.25},
            EffectType.RAINBOW: {"enabled": False, "intensity": 0.3}
        }
        
        self.init_timers()
    
    def init_timers(self):
        """Инициализация таймеров для эффектов"""
        self.global_timer = QTimer()
        self.global_timer.timeout.connect(self.update_effects)
        self.global_timer.start(50)  # 20 FPS для плавности
        
        # Отдельные таймеры для разных эффектов
        self.effect_timers = {}
        for effect_type in EffectType:
            timer = QTimer()
            timer.setInterval(self.get_effect_interval(effect_type))
            timer.timeout.connect(lambda et=effect_type: self.update_single_effect(et))
            self.effect_timers[effect_type] = timer
            
    def get_effect_interval(self, effect_type):
        """Получить интервал обновления для эффекта"""
        intervals = {
            EffectType.GLITCH: 100,
            EffectType.SCAN_LINES: 30,
            EffectType.MATRIX_RAIN: 100,
            EffectType.PIXELATE: 200,
            EffectType.BLOOM: 1000,
            EffectType.VHS: 50,
            EffectType.CHROMA: 150,
            EffectType.STATIC: 80,
            EffectType.WAVE: 60,
            EffectType.RAINBOW: 500
        }
        return intervals.get(effect_type, 100)
    
    def update_effects(self):
        """Обновление всех активных эффектов"""
        for effect_type in self.active_effects:
            if self.config[effect_type]["enabled"]:
                self.parent.update()
    
    def update_single_effect(self, effect_type):
        """Обновление конкретного эффекта"""
        if effect_type in self.active_effects and self.config[effect_type]["enabled"]:
            self.parent.update()
    
    def enable_effect(self, effect_type, enabled=True):
        """Включить/выключить эффект"""
        if effect_type in self.config:
            self.config[effect_type]["enabled"] = enabled
            if enabled:
                self.active_effects.add(effect_type)
                self.effect_timers[effect_type].start()
            else:
                self.active_effects.discard(effect_type)
                self.effect_timers[effect_type].stop()
    
    def set_intensity(self, effect_type, intensity):
        """Установить интенсивность эффекта"""
        if effect_type in self.config:
            self.config[effect_type]["intensity"] = max(0.0, min(1.0, intensity))
    
    def paint_effect(self, painter, effect_type):
        """Нарисовать конкретный эффект"""
        if not self.config[effect_type]["enabled"]:
            return
            
        intensity = self.config[effect_type]["intensity"] * self.intensity
        
        if effect_type == EffectType.GLITCH:
            self.paint_glitch(painter, intensity)
        elif effect_type == EffectType.SCAN_LINES:
            self.paint_scan_lines(painter, intensity)
        elif effect_type == EffectType.MATRIX_RAIN:
            self.paint_matrix_rain(painter, intensity)
        elif effect_type == EffectType.PIXELATE:
            self.paint_pixelate(painter, intensity)
        elif effect_type == EffectType.BLOOM:
            self.paint_bloom(painter, intensity)
        elif effect_type == EffectType.VHS:
            self.paint_vhs(painter, intensity)
        elif effect_type == EffectType.CHROMA:
            self.paint_chroma(painter, intensity)
        elif effect_type == EffectType.STATIC:
            self.paint_static(painter, intensity)
        elif effect_type == EffectType.WAVE:
            self.paint_wave(painter, intensity)
        elif effect_type == EffectType.RAINBOW:
            self.paint_rainbow(painter, intensity)
    
    def paint_glitch(self, painter, intensity):
        """Эффект глитча с разными типами искажений"""
        if random.random() < 0.7 * intensity:
            return
            
        width = self.parent.width()
        height = self.parent.height()
        
        # Сохраняем состояние painter
        painter.save()
        
        # Случайное смещение
        offset_x = random.randint(-int(5 * intensity), int(5 * intensity))
        offset_y = random.randint(-int(3 * intensity), int(3 * intensity))
        painter.translate(offset_x, offset_y)
        
        # Случайный цветной сдвиг (хроматическая аберрация)
        if random.random() < 0.3:
            r = random.randint(0, 50)
            g = random.randint(0, 50)
            b = random.randint(0, 50)
            
            # Рисуем красный канал
            painter.setOpacity(0.3)
            painter.setCompositionMode(QPainter.CompositionMode_Plus)
            painter.translate(2, 0)
            painter.setPen(QColor(255, 0, 0, 100))
            painter.drawRect(0, 0, width, height)
            painter.translate(-2, 0)
            
            # Рисуем синий канал
            painter.translate(-2, 0)
            painter.setPen(QColor(0, 0, 255, 100))
            painter.drawRect(0, 0, width, height)
            painter.translate(2, 0)
        
        # Линии разрыва
        if random.random() < 0.4:
            for _ in range(random.randint(1, int(3 * intensity))):
                y = random.randint(0, height)
                height_segment = random.randint(5, int(30 * intensity))
                offset = random.randint(-10, 10)
                
                painter.save()
                painter.translate(offset, 0)
                painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
                painter.drawLine(0, y, width, y)
                painter.drawLine(0, y + height_segment, width, y + height_segment)
                painter.restore()
        
        # Прямоугольники выреза
        if random.random() < 0.2:
            for _ in range(random.randint(1, int(2 * intensity))):
                x = random.randint(0, width - 50)
                y = random.randint(0, height - 30)
                w = random.randint(20, 100)
                h = random.randint(10, 50)
                
                painter.save()
                painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
                painter.setBrush(QColor(0, 0, 0, 200))
                painter.setPen(Qt.NoPen)
                painter.drawRect(x, y, w, h)
                painter.restore()
        
        painter.restore()
    
    def paint_scan_lines(self, painter, intensity):
        """Улучшенные сканирующие линии"""
        width = self.parent.width()
        height = self.parent.height()
        
        # Основные линии
        line_spacing = max(2, int(4 * (1 - intensity * 0.5)))
        line_opacity = 0.1 + intensity * 0.15
        
        painter.setPen(QPen(QColor(0, 255, 0, int(80 * line_opacity)), 1))
        for y in range(0, height, line_spacing):
            painter.drawLine(0, y, width, y)
        
        # Движущаяся линия сканирования
        current_time = time.time()
        scan_y = int((current_time * 50) % (height + 100)) - 50
        scan_height = 30
        
        gradient = QLinearGradient(0, scan_y, 0, scan_y + scan_height)
        gradient.setColorAt(0, QColor(0, 255, 0, 0))
        gradient.setColorAt(0.1, QColor(0, 255, 0, int(150 * intensity)))
        gradient.setColorAt(0.5, QColor(0, 255, 255, int(200 * intensity)))
        gradient.setColorAt(0.9, QColor(0, 255, 0, int(150 * intensity)))
        gradient.setColorAt(1, QColor(0, 255, 0, 0))
        
        painter.setOpacity(0.3 * intensity)
        painter.fillRect(0, scan_y, width, scan_height, gradient)
        painter.setOpacity(1.0)
        
        # Эффект кривизны ЭЛТ
        painter.setOpacity(0.05 * intensity)
        vignette = QRadialGradient(width/2, height/2, max(width, height)/2)
        vignette.setColorAt(0, QColor(0, 0, 0, 0))
        vignette.setColorAt(0.7, QColor(0, 0, 0, 0))
        vignette.setColorAt(1, QColor(0, 0, 0, 150))
        painter.fillRect(0, 0, width, height, vignette)
    
    def paint_matrix_rain(self, painter, intensity):
        """Эффект матричного дождя"""
        if not hasattr(self, 'matrix_chars'):
            # Символы для матрицы
            self.matrix_chars = [chr(i) for i in range(0x30A0, 0x30FF)] + \
                               [chr(i) for i in range(0xFF66, 0xFF9D)]
            self.matrix_columns = []
            self.last_matrix_update = time.time()
        
        width = self.parent.width()
        height = self.parent.height()
        
        # Инициализация колонок
        if not self.matrix_columns or time.time() - self.last_matrix_update > 10:
            column_count = int(20 + 30 * intensity)
            self.matrix_columns = []
            for i in range(column_count):
                self.matrix_columns.append({
                    'x': random.randint(0, width),
                    'y': random.randint(-500, 0),
                    'speed': random.uniform(1, 3) * (0.5 + intensity * 0.5),
                    'length': random.randint(5, 20),
                    'chars': [random.choice(self.matrix_chars) for _ in range(20)],
                    'brightness': random.uniform(0.3, 1.0)
                })
            self.last_matrix_update = time.time()
        
        painter.setFont(QFont("Courier New", int(10 + 4 * intensity)))
        
        for col in self.matrix_columns:
            col['y'] += col['speed']
            if col['y'] > height + 100:
                col['y'] = -col['length'] * 20
                col['x'] = random.randint(0, width)
            
            x = col['x']
            y = col['y']
            
            # Рисуем символы в колонке
            for i in range(col['length']):
                char_y = y + i * 20
                if -20 <= char_y <= height:
                    # Градиент яркости
                    if i == 0:
                        color = QColor(255, 255, 255)
                        alpha = 255
                    elif i == 1:
                        color = QColor(0, 255, 0)
                        alpha = 220
                    else:
                        fade = max(0, 1 - (i / col['length']))
                        alpha = int(fade * 100 + 50)
                        green = int(100 + 155 * fade)
                        color = QColor(0, green, 0, alpha)
                    
                    # Применяем яркость колонки
                    color.setAlpha(int(alpha * col['brightness'] * intensity))
                    
                    painter.setPen(color)
                    char_idx = (i + int(time.time() * 10)) % len(col['chars'])
                    painter.drawText(int(x), int(char_y), col['chars'][char_idx])
    
    def paint_vhs(self, painter, intensity):
        """Эффект VHS-ленты"""
        width = self.parent.width()
        height = self.parent.height()
        current_time = time.time()
        
        # Цветные полосы
        stripe_height = int(15 * intensity)
        for i in range(0, height, stripe_height * 3):
            # Синяя полоса
            painter.setOpacity(0.1 * intensity)
            painter.fillRect(0, i, width, stripe_height, QColor(0, 0, 255, 100))
            
            # Красная полоса
            painter.fillRect(0, i + stripe_height, width, stripe_height, QColor(255, 0, 0, 80))
        
        # Шум VHS
        noise_opacity = 0.05 * intensity
        painter.setOpacity(noise_opacity)
        for _ in range(int(width * height * 0.001 * intensity)):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            color = QColor(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(30, 80)
            )
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(x, y, size, size)
        
        # Искажения вверху и внизу
        distortion_height = int(20 * intensity)
        top_gradient = QLinearGradient(0, 0, 0, distortion_height)
        top_gradient.setColorAt(0, QColor(0, 0, 0, 150))
        top_gradient.setColorAt(1, QColor(0, 0, 0, 0))
        
        bottom_gradient = QLinearGradient(0, height - distortion_height, 0, height)
        bottom_gradient.setColorAt(0, QColor(0, 0, 0, 0))
        bottom_gradient.setColorAt(1, QColor(0, 0, 0, 150))
        
        painter.setOpacity(0.5 * intensity)
        painter.fillRect(0, 0, width, distortion_height, top_gradient)
        painter.fillRect(0, height - distortion_height, width, distortion_height, bottom_gradient)
    
    def paint_chroma(self, painter, intensity):
        """Хроматическая аберрация"""
        if random.random() < 0.7:
            return
            
        width = self.parent.width()
        height = self.parent.height()
        offset = int(2 * intensity)
        
        # Сохраняем состояние
        painter.save()
        painter.setCompositionMode(QPainter.CompositionMode_Plus)
        
        # Красный канал (смещен вправо)
        painter.setOpacity(0.3 * intensity)
        painter.translate(offset, 0)
        painter.setPen(QPen(QColor(255, 0, 0, 100), 1))
        painter.drawRect(0, 0, width, height)
        painter.translate(-offset, 0)
        
        # Синий канал (смещен влево)
        painter.translate(-offset, 0)
        painter.setPen(QPen(QColor(0, 0, 255, 100), 1))
        painter.drawRect(0, 0, width, height)
        painter.translate(offset, 0)
        
        # Зеленый канал (без смещения)
        painter.setPen(QPen(QColor(0, 255, 0, 50), 1))
        painter.drawRect(0, 0, width, height)
        
        painter.restore()
    
    def paint_static(self, painter, intensity):
        """Эффект статического шума"""
        width = self.parent.width()
        height = self.parent.height()
        
        # Мелкий шум
        noise_count = int(width * height * 0.005 * intensity)
        painter.setOpacity(0.3 * intensity)
        
        for _ in range(noise_count):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 2)
            brightness = random.randint(100, 255)
            alpha = random.randint(20, 60)
            color = QColor(brightness, brightness, brightness, alpha)
            
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawRect(x, y, size, size)
        
        # Крупные "вспышки"
        if random.random() < 0.05 * intensity:
            flash_size = random.randint(20, int(100 * intensity))
            flash_x = random.randint(0, width - flash_size)
            flash_y = random.randint(0, height - flash_size)
            
            flash_gradient = QRadialGradient(
                flash_x + flash_size/2,
                flash_y + flash_size/2,
                flash_size/2
            )
            flash_gradient.setColorAt(0, QColor(255, 255, 255, 150))
            flash_gradient.setColorAt(1, QColor(255, 255, 255, 0))
            
            painter.setOpacity(0.5 * intensity)
            painter.fillRect(flash_x, flash_y, flash_size, flash_size, flash_gradient)
    
    def paint_wave(self, painter, intensity):
        """Волновые искажения"""
        width = self.parent.width()
        height = self.parent.height()
        current_time = time.time()
        
        # Сохраняем состояние
        painter.save()
        
        # Применяем волновое искажение
        wave_amplitude = 2 * intensity
        wave_frequency = 0.01
        
        for y in range(0, height, 2):
            offset = math.sin(y * wave_frequency + current_time) * wave_amplitude
            offset += math.sin(y * wave_frequency * 2 + current_time * 1.5) * wave_amplitude * 0.5
            
            painter.setOpacity(0.1 * intensity)
            painter.setPen(QPen(QColor(0, 255, 255, 30), 1))
            painter.drawLine(int(offset), y, width + int(offset), y)
        
        painter.restore()
    
    def paint_rainbow(self, painter, intensity):
        """Радужный эффект"""
        if random.random() < 0.5:
            return
            
        width = self.parent.width()
        height = self.parent.height()
        current_time = time.time()
        
        # Конусный градиент для радуги
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) / 2
        
        rainbow = QConicalGradient(center_x, center_y, (current_time * 20) % 360)
        rainbow.setColorAt(0.0, QColor(255, 0, 0, int(100 * intensity)))
        rainbow.setColorAt(0.2, QColor(255, 165, 0, int(80 * intensity)))
        rainbow.setColorAt(0.4, QColor(255, 255, 0, int(60 * intensity)))
        rainbow.setColorAt(0.6, QColor(0, 255, 0, int(40 * intensity)))
        rainbow.setColorAt(0.8, QColor(0, 0, 255, int(20 * intensity)))
        rainbow.setColorAt(1.0, QColor(75, 0, 130, int(10 * intensity)))
        
        painter.setOpacity(0.3 * intensity)
        painter.setBrush(rainbow)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(
            int(center_x - radius),
            int(center_y - radius),
            int(radius * 2),
            int(radius * 2)
        )
    
    def paint_pixelate(self, painter, intensity):
        """Эффект пикселизации"""
        if random.random() < 0.8:
            return
            
        width = self.parent.width()
        height = self.parent.height()
        pixel_size = max(2, int(10 * intensity))
        
        painter.setOpacity(0.5 * intensity)
        painter.setPen(QPen(QColor(0, 255, 0, 50), 1))
        
        for x in range(0, width, pixel_size):
            for y in range(0, height, pixel_size):
                if random.random() < 0.1:
                    brightness = random.randint(50, 200)
                    painter.setBrush(QColor(0, brightness, 0, 100))
                    painter.drawRect(x, y, pixel_size, pixel_size)
    
    def paint_bloom(self, painter, intensity):
        """Эффект свечения (bloom)"""
        width = self.parent.width()
        height = self.parent.height()
        current_time = time.time()
        
        # Свечение по краям
        bloom_size = int(100 * intensity)
        center_x = width / 2
        center_y = height / 2
        
        # Пульсирующее свечение
        pulse = 0.5 + 0.5 * math.sin(current_time * 2)
        
        for i in range(3):
            radius = bloom_size * (1 + i * 0.3)
            gradient = QRadialGradient(center_x, center_y, radius)
            
            colors = [
                (0, QColor(0, 255, 0, int(30 * pulse * intensity))),
                (0.7, QColor(0, 255, 255, int(20 * pulse * intensity))),
                (1, QColor(0, 0, 0, 0))
            ]
            
            for pos, color in colors:
                gradient.setColorAt(pos, color)
            
            painter.setOpacity(0.5 * intensity / (i + 1))
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(
                int(center_x - radius),
                int(center_y - radius),
                int(radius * 2),
                int(radius * 2)
            )
    
    def paint_all_effects(self, painter):
        """Нарисовать все активные эффекты"""
        # Порядок важен: сначала фон, потом поверхностные эффекты
        effects_order = [
            EffectType.BLOOM,
            EffectType.WAVE,
            EffectType.MATRIX_RAIN,
            EffectType.RAINBOW,
            EffectType.SCAN_LINES,
            EffectType.STATIC,
            EffectType.VHS,
            EffectType.CHROMA,
            EffectType.GLITCH,
            EffectType.PIXELATE
        ]
        
        for effect_type in effects_order:
            if (effect_type in self.active_effects and 
                self.config[effect_type]["enabled"]):
                self.paint_effect(painter, effect_type)

def create_crt_monitor_effect(parent: QWidget):
    """Создать эффект старого ЭЛТ-монитора"""
    class CRTEffectWidget(QWidget):
        def __init__(self, parent):
            super().__init__(parent)
            self.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.scanline_position = 0
            self.scanline_speed = 3
            self.curvature = 0.02
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_effect)
            self.timer.start(16)  # ~60 FPS
            
        def update_effect(self):
            self.scanline_position = (self.scanline_position + self.scanline_speed) % (self.parent().height() + 20)
            self.update()
            
        def paintEvent(self, event):
            if not self.isVisible():
                return
                
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            width = self.width()
            height = self.height()
            
            # Эффект кривизны экрана
            painter.setOpacity(0.1)
            gradient = QRadialGradient(width/2, height/2, max(width, height)/2)
            gradient.setColorAt(0, QColor(0, 0, 0, 0))
            gradient.setColorAt(0.7, QColor(0, 0, 0, 0))
            gradient.setColorAt(1, QColor(0, 0, 0, 100))
            painter.fillRect(0, 0, width, height, gradient)
            
            # Сканирующие линии
            line_spacing = 2
            painter.setOpacity(0.15)
            painter.setPen(QPen(QColor(0, 255, 0, 30), 1))
            for y in range(0, height, line_spacing):
                # Добавляем кривизну линии
                curve_offset = int(math.sin(y * 0.01) * 5)
                painter.drawLine(0 + curve_offset, y, width + curve_offset, y)
            
            # Движущаяся линия сканирования
            scan_y = self.scanline_position
            scan_height = 20
            scan_gradient = QLinearGradient(0, scan_y, 0, scan_y + scan_height)
            scan_gradient.setColorAt(0, QColor(0, 255, 0, 0))
            scan_gradient.setColorAt(0.3, QColor(0, 255, 0, 100))
            scan_gradient.setColorAt(0.7, QColor(0, 255, 0, 100))
            scan_gradient.setColorAt(1, QColor(0, 255, 0, 0))
            
            painter.setOpacity(0.3)
            painter.fillRect(0, scan_y, width, scan_height, scan_gradient)
            
            # Эффект виньетирования
            painter.setOpacity(0.3)
            vignette = QRadialGradient(width/2, height/2, max(width, height)/1.5)
            vignette.setColorAt(0, QColor(0, 0, 0, 0))
            vignette.setColorAt(0.8, QColor(0, 0, 0, 0))
            vignette.setColorAt(1, QColor(0, 0, 0, 150))
            painter.fillRect(0, 0, width, height, vignette)
            
            # Свечение по краям
            painter.setOpacity(0.1)
            glow = QLinearGradient(0, 0, width, 0)
            glow.setColorAt(0, QColor(0, 255, 0, 50))
            glow.setColorAt(0.2, QColor(0, 255, 0, 0))
            glow.setColorAt(0.8, QColor(0, 255, 0, 0))
            glow.setColorAt(1, QColor(0, 255, 0, 50))
            painter.fillRect(0, 0, width, height, glow)
    
    effect_widget = CRTEffectWidget(parent)
    effect_widget.resize(parent.size())
    
    # Переопределяем resizeEvent
    original_resize = parent.resizeEvent
    def new_resize(e):
        effect_widget.resize(parent.size())
        if original_resize:
            original_resize(e)
    parent.resizeEvent = new_resize
    
    return effect_widget

def create_hologram_effect(parent: QWidget):
    """Создать голографический эффект"""
    class HologramWidget(QWidget):
        def __init__(self, parent):
            super().__init__(parent)
            self.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.phase = 0
            self.scanline_y = 0
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_effect)
            self.timer.start(50)
            
        def update_effect(self):
            self.phase = (self.phase + 0.1) % (2 * math.pi)
            self.scanline_y = (self.scanline_y + 2) % self.height()
            self.update()
            
        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            width = self.width()
            height = self.height()
            
            # Интерференционные полосы
            stripe_spacing = 10
            painter.setOpacity(0.2)
            painter.setPen(QPen(QColor(0, 255, 255, 100), 1))
            
            for x in range(0, width, stripe_spacing):
                offset = int(math.sin(self.phase + x * 0.01) * 5)
                painter.drawLine(x + offset, 0, x + offset, height)
            
            # Сканирующая линия
            scan_gradient = QLinearGradient(0, self.scanline_y, 0, self.scanline_y + 30)
            scan_gradient.setColorAt(0, QColor(0, 255, 255, 0))
            scan_gradient.setColorAt(0.5, QColor(0, 255, 255, 150))
            scan_gradient.setColorAt(1, QColor(0, 255, 255, 0))
            
            painter.setOpacity(0.4)
            painter.fillRect(0, self.scanline_y, width, 30, scan_gradient)
            
            # Точечный шум
            painter.setOpacity(0.1)
            for _ in range(100):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(1, 3)
                alpha = random.randint(50, 150)
                color = QColor(0, 255, 255, alpha)
                painter.setBrush(color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(x, y, size, size)
    
    hologram = HologramWidget(parent)
    hologram.resize(parent.size())
    
    original_resize = parent.resizeEvent
    def new_resize(e):
        hologram.resize(parent.size())
        if original_resize:
            original_resize(e)
    parent.resizeEvent = new_resize
    
    return hologram

def create_glitch_overlay(parent: QWidget, intensity=0.5):
    """Создать оверлей с глитч-эффектами"""
    class GlitchOverlayWidget(QWidget):
        def __init__(self, parent, intensity):
            super().__init__(parent)
            self.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.intensity = intensity
            self.glitch_data = []
            self.last_glitch = time.time()
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_glitch)
            self.timer.start(100)
            
        def update_glitch(self):
            current_time = time.time()
            
            # Случайный глитч
            if random.random() < 0.3 * self.intensity:
                self.create_glitch_segment()
            
            # Удаляем старые глитчи
            self.glitch_data = [g for g in self.glitch_data 
                               if current_time - g['time'] < 0.5]
            
            self.update()
            
        def create_glitch_segment(self):
            width = self.width()
            height = self.height()
            
            glitch_type = random.choice(['horizontal', 'vertical', 'block'])
            glitch = {
                'time': time.time(),
                'type': glitch_type,
                'color': QColor(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(100, 200)
                )
            }
            
            if glitch_type == 'horizontal':
                glitch.update({
                    'y': random.randint(0, height - 10),
                    'height': random.randint(5, 20),
                    'offset': random.randint(-10, 10)
                })
            elif glitch_type == 'vertical':
                glitch.update({
                    'x': random.randint(0, width - 10),
                    'width': random.randint(5, 20),
                    'offset': random.randint(-10, 10)
                })
            else:  # block
                glitch.update({
                    'x': random.randint(0, width - 50),
                    'y': random.randint(0, height - 30),
                    'width': random.randint(20, 50),
                    'height': random.randint(15, 30)
                })
            
            self.glitch_data.append(glitch)
            
        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            for glitch in self.glitch_data:
                age = time.time() - glitch['time']
                opacity = max(0, 1 - age * 2) * self.intensity
                painter.setOpacity(opacity)
                
                if glitch['type'] == 'horizontal':
                    painter.fillRect(
                        0, glitch['y'] + glitch['offset'],
                        self.width(), glitch['height'],
                        glitch['color']
                    )
                elif glitch['type'] == 'vertical':
                    painter.fillRect(
                        glitch['x'] + glitch['offset'], 0,
                        glitch['width'], self.height(),
                        glitch['color']
                    )
                else:  # block
                    painter.fillRect(
                        glitch['x'], glitch['y'],
                        glitch['width'], glitch['height'],
                        glitch['color']
                    )
    
    overlay = GlitchOverlayWidget(parent, intensity)
    overlay.resize(parent.size())
    
    original_resize = parent.resizeEvent
    def new_resize(e):
        overlay.resize(parent.size())
        if original_resize:
            original_resize(e)
    parent.resizeEvent = new_resize
    
    return overlay