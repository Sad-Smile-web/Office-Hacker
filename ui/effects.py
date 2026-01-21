# ui/effects.py
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QGraphicsOpacityEffect
from PySide6.QtCore import QTimer, QPropertyAnimation, Qt, QPoint
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QLinearGradient

def apply_glow_effect(widget, color=QColor(0, 255, 0), blur_radius=15, offset=0):
    """Применить эффект свечения к виджету"""
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_radius)
    shadow.setColor(color)
    shadow.setOffset(offset, offset)
    widget.setGraphicsEffect(shadow)
    return shadow

def apply_neon_effect(widget, color=QColor(0, 255, 255)):
    """Применить неоновый эффект к тексту или кнопке"""
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setColor(color)
    shadow.setOffset(0, 0)
    
    # Добавляем пульсацию
    animation = QPropertyAnimation(shadow, b"blurRadius")
    animation.setDuration(2000)
    animation.setStartValue(15)
    animation.setEndValue(25)
    animation.setLoopCount(-1)
    animation.start()
    
    widget.setGraphicsEffect(shadow)
    return shadow, animation

def create_fade_animation(widget, duration=1000, start_opacity=0, end_opacity=1):
    """Создать анимацию плавного появления/исчезновения"""
    opacity_effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(opacity_effect)
    
    animation = QPropertyAnimation(opacity_effect, b"opacity")
    animation.setDuration(duration)
    animation.setStartValue(start_opacity)
    animation.setEndValue(end_opacity)
    
    return animation

def apply_scan_lines_effect(widget):
    """Применить эффект сканирующих линий к виджету"""
    class ScanLinesWidget(QWidget):
        def __init__(self, parent):
            super().__init__(parent)
            self.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.scan_line_y = 0
            self.scan_speed = 3
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_scan_line)
            self.timer.start(50)
            
        def update_scan_line(self):
            self.scan_line_y = (self.scan_line_y + self.scan_speed) % (self.height() + 100)
            self.update()
            
        def paintEvent(self, event):
            painter = QPainter(self)
            
            # Сканирующая линия
            scan_height = 30
            scan_gradient = QLinearGradient(0, self.scan_line_y, 0, self.scan_line_y + scan_height)
            scan_gradient.setColorAt(0, QColor(0, 255, 0, 0))
            scan_gradient.setColorAt(0.5, QColor(0, 255, 0, 100))
            scan_gradient.setColorAt(1, QColor(0, 255, 0, 0))
            
            painter.setOpacity(0.3)
            painter.fillRect(0, self.scan_line_y, self.width(), scan_height, scan_gradient)
            
            # Статические линии
            painter.setOpacity(0.1)
            painter.setPen(QPen(QColor(0, 255, 0, 50), 1))
            for y in range(0, self.height(), 4):
                painter.drawLine(0, y, self.width(), y)
    
    scan_lines = ScanLinesWidget(widget)
    scan_lines.resize(widget.size())
    
    # Привязываем изменение размера
    original_resize = widget.resizeEvent
    def new_resize(e):
        scan_lines.resize(widget.size())
        if original_resize:
            original_resize(e)
    widget.resizeEvent = new_resize
    
    return scan_lines

def apply_crt_effect(widget):
    """Применить эффект ЭЛТ-монитора"""
    class CRTEffectWidget(QWidget):
        def __init__(self, parent):
            super().__init__(parent)
            self.setAttribute(Qt.WA_TransparentForMouseEvents)
            
        def paintEvent(self, event):
            painter = QPainter(self)
            
            # Эффект виньетирования
            vignette = QLinearGradient(0, 0, 0, self.height())
            vignette.setColorAt(0, QColor(0, 0, 0, 0))
            vignette.setColorAt(0.3, QColor(0, 0, 0, 0))
            vignette.setColorAt(0.7, QColor(0, 0, 0, 0))
            vignette.setColorAt(1, QColor(0, 0, 0, 100))
            
            painter.setOpacity(0.2)
            painter.fillRect(0, 0, self.width(), self.height(), vignette)
            
            # Эффект закругленных углов
            painter.setOpacity(0.1)
            painter.setPen(QPen(QColor(0, 255, 255, 100), 2))
            
            # Углы
            corner_size = 20
            # Левый верхний
            painter.drawLine(0, 0, corner_size, 0)
            painter.drawLine(0, 0, 0, corner_size)
            # Правый верхний
            painter.drawLine(self.width(), 0, self.width() - corner_size, 0)
            painter.drawLine(self.width(), 0, self.width(), corner_size)
            # Левый нижний
            painter.drawLine(0, self.height(), corner_size, self.height())
            painter.drawLine(0, self.height(), 0, self.height() - corner_size)
            # Правый нижний
            painter.drawLine(self.width(), self.height(), self.width() - corner_size, self.height())
            painter.drawLine(self.width(), self.height(), self.width(), self.height() - corner_size)
    
    crt_effect = CRTEffectWidget(widget)
    crt_effect.resize(widget.size())
    
    original_resize = widget.resizeEvent
    def new_resize(e):
        crt_effect.resize(widget.size())
        if original_resize:
            original_resize(e)
    widget.resizeEvent = new_resize
    
    return crt_effect

def create_pulse_animation(widget, property_name, duration=1000, min_value=1.0, max_value=1.1):
    """Создать пульсирующую анимацию для виджета"""
    animation = QPropertyAnimation(widget, property_name.encode())
    animation.setDuration(duration)
    animation.setStartValue(min_value)
    animation.setEndValue(max_value)
    animation.setLoopCount(-1)
    animation.setEasingCurve(QPropertyAnimation.InOutSine)
    return animation

def apply_button_hover_effect(button):
    """Применить эффект при наведении на кнопку"""
    original_style = button.styleSheet()
    
    def on_enter():
        button.setStyleSheet(original_style + """
            border-width: 3px;
            border-color: #00ffff;
            background-color: rgba(0, 100, 200, 0.8);
        """)
    
    def on_leave():
        button.setStyleSheet(original_style)
    
    button.enterEvent = lambda e: on_enter()
    button.leaveEvent = lambda e: on_leave()

# Простые эффекты для текста
def make_text_glow(label, color=QColor(0, 255, 255)):
    """Сделать текст светящимся"""
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)
    shadow.setColor(color)
    shadow.setOffset(0, 0)
    label.setGraphicsEffect(shadow)
    return shadow

def make_text_blink(label, interval=500):
    """Сделать текст мигающим"""
    timer = QTimer()
    timer.setInterval(interval)
    
    is_visible = True
    def toggle_visibility():
        nonlocal is_visible
        is_visible = not is_visible
        label.setVisible(is_visible)
    
    timer.timeout.connect(toggle_visibility)
    timer.start()
    return timer