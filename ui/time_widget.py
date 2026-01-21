from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPainter, QColor, QLinearGradient, QPen
import datetime

class TimeWidget(QWidget):
    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self.game_state = game_state
        self.blink_state = True
        self.time_pulse = 0.0
        self.time_pulse_direction = 1
        
        # Инициализируем таймеры как None
        self.blink_timer = None
        self.pulse_timer = None
        self.update_timer = None
        
        self.init_ui()
        self.setup_animations()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # Увеличиваем минимальную высоту виджета
        self.setMinimumHeight(220)
        
        # Верхняя панель с датой и временем
        time_frame = QFrame()
        time_frame.setObjectName("timeDisplay")
        time_frame.setStyleSheet("""
            QFrame#timeDisplay {
                background-color: rgba(10, 20, 30, 0.9);
                border: 2px solid #1dd1a1;
                border-radius: 8px;
                padding: 12px;
                min-height: 180px;
            }
        """)
        
        time_layout = QVBoxLayout()
        time_layout.setSpacing(8)
        
        # Дата
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setObjectName("dateLabel")
        self.date_label.setStyleSheet("""
            QLabel#dateLabel {
                color: #00bfff;
                font-family: 'Source Code Pro';
                font-size: 14px;
                font-weight: bold;
                text-shadow: 0 0 5px rgba(0, 191, 255, 0.5);
                padding-bottom: 5px;
            }
        """)
        
        # Время с разделителем - ИСПРАВЛЕНО: добавлены прокладки для правильного выравнивания
        time_row = QHBoxLayout()
        time_row.setSpacing(2)
        time_row.setContentsMargins(0, 0, 0, 0)
        
        # Левый отступ
        time_row.addStretch()
        
        # Часы - ИСПРАВЛЕНО: установлен фиксированный размер шрифта
        self.hour_label = QLabel("09")
        self.hour_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.hour_label.setObjectName("hourLabel")
        self.hour_label.setMinimumWidth(60)
        self.hour_label.setMaximumWidth(70)
        
        # Разделитель
        self.separator_label = QLabel(":")
        self.separator_label.setAlignment(Qt.AlignCenter)
        self.separator_label.setObjectName("separatorLabel")
        self.separator_label.setMinimumWidth(10)
        self.separator_label.setMaximumWidth(20)
        
        # Минуты - ИСПРАВЛЕНО: установлен фиксированный размер шрифта
        self.minute_label = QLabel("00")
        self.minute_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.minute_label.setObjectName("minuteLabel")
        self.minute_label.setMinimumWidth(60)
        self.minute_label.setMaximumWidth(70)
        
        # Правый отступ
        time_row.addStretch()
        
        # Добавляем виджеты в правильном порядке
        time_row.addWidget(self.hour_label)
        time_row.addWidget(self.separator_label)
        time_row.addWidget(self.minute_label)
        
        # Стили для часов и минут - ИСПРАВЛЕНО: единый стиль для обоих
        time_style = """
            font-family: 'Source Code Pro';
            font-size: 42px;
            font-weight: bold;
            padding: 8px 12px;
            border-radius: 8px;
            background-color: rgba(0, 0, 0, 0.4);
            min-height: 70px;
            min-width: 70px;
            qproperty-alignment: 'AlignCenter';
        """
        
        self.hour_label.setStyleSheet(f"""
            QLabel#hourLabel {{
                {time_style}
                color: #1dd1a1;
                text-shadow: 0 0 15px rgba(29, 209, 161, 0.8);
            }}
        """)
        
        self.minute_label.setStyleSheet(f"""
            QLabel#minuteLabel {{
                {time_style}
                color: #00bfff;
                text-shadow: 0 0 15px rgba(0, 191, 255, 0.8);
            }}
        """)
        
        self.separator_label.setStyleSheet("""
            QLabel#separatorLabel {
                color: #ffffff;
                font-family: 'Source Code Pro';
                font-size: 42px;
                font-weight: bold;
                background-color: transparent;
                min-width: 20px;
                min-height: 70px;
                padding: 8px 0;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        
        # Прогресс рабочего дня
        self.progress_frame = QFrame()
        self.progress_frame.setFixedHeight(30)
        self.progress_frame.setMinimumWidth(250)
        self.progress_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(20, 30, 40, 0.8);
                border: 2px solid #333;
                border-radius: 15px;
                padding: 3px;
                margin: 10px 0 5px 0;
            }
        """)
        
        self.progress_bar = QFrame(self.progress_frame)
        self.progress_bar.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1dd1a1, stop:0.5 #00bfff, stop:1 #54a0ff);
                border-radius: 12px;
            }
        """)
        
        # Текст прогресса
        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-family: 'Source Code Pro';
                font-size: 13px;
                font-weight: bold;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
                padding: 3px 0;
            }
        """)
        
        # Время до конца смены
        self.time_left_label = QLabel()
        self.time_left_label.setAlignment(Qt.AlignCenter)
        self.time_left_label.setStyleSheet("""
            QLabel {
                color: #feca57;
                font-family: 'Source Code Pro';
                font-size: 12px;
                font-weight: bold;
                padding: 5px;
                background-color: rgba(254, 202, 87, 0.1);
                border-radius: 5px;
                margin-top: 5px;
            }
        """)
        
        # Добавляем все в layout - ИСПРАВЛЕНО: порядок добавления
        time_layout.addWidget(self.date_label)
        time_layout.addLayout(time_row)
        time_layout.addWidget(self.progress_frame)
        time_layout.addWidget(self.progress_label)
        time_layout.addWidget(self.time_left_label)
        time_frame.setLayout(time_layout)
        
        layout.addWidget(time_frame)
        self.setLayout(layout)
        
        # Инициализируем отображение
        self.update_display()
        
    def setup_animations(self):
        """Настройка анимаций времени"""
        # Останавливаем старые таймеры, если они существуют
        self.stop_animations()
        
        # Таймер для мигания разделителя
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.update_blink)
        self.blink_timer.start(500)  # Мигание каждые 500 мс
        
        # Таймер для пульсации времени
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.update_pulse)
        self.pulse_timer.start(50)  # Плавная анимация
        
        # Таймер для обновления времени
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(1000)  # Обновление каждую секунду
    
    def stop_animations(self):
        """Остановка всех анимаций и таймеров"""
        if self.blink_timer and self.blink_timer.isActive():
            self.blink_timer.stop()
        if self.pulse_timer and self.pulse_timer.isActive():
            self.pulse_timer.stop()
        if self.update_timer and self.update_timer.isActive():
            self.update_timer.stop()
    
    def restart_animations(self):
        """Перезапуск анимаций после загрузки сохранения"""
        self.setup_animations()
        self.update_display()  # Немедленное обновление
    
    def update_game_state(self, new_game_state):
        """Обновить игровое состояние (вызывается при загрузке сохранения)"""
        self.game_state = new_game_state
        self.restart_animations()
        
    def update_blink(self):
        """Обновление мигания разделителя"""
        self.blink_state = not self.blink_state
        
        if self.blink_state:
            self.separator_label.setStyleSheet("""
                QLabel#separatorLabel {
                    color: #ffffff;
                    font-family: 'Source Code Pro';
                    font-size: 42px;
                    font-weight: bold;
                    background-color: transparent;
                    min-width: 20px;
                    min-height: 70px;
                    padding: 8px 0;
                    qproperty-alignment: 'AlignCenter';
                }
            """)
        else:
            self.separator_label.setStyleSheet("""
                QLabel#separatorLabel {
                    color: rgba(255, 255, 255, 0.3);
                    font-family: 'Source Code Pro';
                    font-size: 42px;
                    font-weight: bold;
                    background-color: transparent;
                    min-width: 20px;
                    min-height: 70px;
                    padding: 8px 0;
                    qproperty-alignment: 'AlignCenter';
                }
            """)
            
    def update_pulse(self):
        """Обновление пульсации времени"""
        self.time_pulse += 0.05 * self.time_pulse_direction
        
        if self.time_pulse >= 1.0:
            self.time_pulse_direction = -1
            self.time_pulse = 1.0
        elif self.time_pulse <= 0.0:
            self.time_pulse_direction = 1
            self.time_pulse = 0.0
            
        # Обновляем свечение в зависимости от времени суток
        if self.game_state:
            hour = self.game_state.game_time.get('current_hour', 9)
            
            pulse_intensity = 15 + int(self.time_pulse * 8)
            
            if hour >= 17:  # Вечер
                hour_color = "#ff6b6b"
                minute_color = "#ff8e8e"
            elif hour >= 13:  # День
                hour_color = "#feca57"
                minute_color = "#ffd98c"
            else:  # Утро
                hour_color = "#1dd1a1"
                minute_color = "#00bfff"
                
            # Применяем пульсацию к часам
            self.hour_label.setStyleSheet(f"""
                QLabel#hourLabel {{
                    font-family: 'Source Code Pro';
                    font-size: 42px;
                    font-weight: bold;
                    padding: 8px 12px;
                    border-radius: 8px;
                    background-color: rgba(0, 0, 0, 0.4);
                    min-height: 70px;
                    min-width: 70px;
                    qproperty-alignment: 'AlignCenter';
                    color: {hour_color};
                    text-shadow: 0 0 {pulse_intensity}px {hour_color};
                }}
            """)
            
            # Применяем пульсацию к минутам (слегка отстающую)
            minute_pulse = max(0, pulse_intensity - 2)
            self.minute_label.setStyleSheet(f"""
                QLabel#minuteLabel {{
                    font-family: 'Source Code Pro';
                    font-size: 42px;
                    font-weight: bold;
                    padding: 8px 12px;
                    border-radius: 8px;
                    background-color: rgba(0, 0, 0, 0.4);
                    min-height: 70px;
                    min-width: 70px;
                    qproperty-alignment: 'AlignCenter';
                    color: {minute_color};
                    text-shadow: 0 0 {minute_pulse}px {minute_color};
                }}
            """)
                
    def update_display(self):
        """Обновить отображение времени"""
        if not self.game_state:
            return
            
        try:
            # Получаем время и дату напрямую из game_state
            current_hour = self.game_state.game_time.get('current_hour', 9)
            current_minute = self.game_state.game_time.get('current_minute', 0)
            date_str = self.game_state.get_formatted_date()
            progress = self.game_state.get_workday_progress()
            
            # Форматируем часы и минуты с ведущим нулем
            hours = f"{current_hour:02d}"
            minutes = f"{current_minute:02d}"
            
            # Проверяем корректность прогресса
            if progress < 0 or progress > 100:
                progress = 0
                print(f"[DEBUG] Некорректный прогресс: {progress}, время: {hours}:{minutes}")
            
            self.date_label.setText(f"📅 {date_str}")
            self.hour_label.setText(hours)
            self.minute_label.setText(minutes)
            
            # Обновляем прогресс-бар только если фрейм видим
            if self.progress_frame.width() > 10:
                progress_width = int((progress / 100) * (self.progress_frame.width() - 6))
                self.progress_bar.setGeometry(3, 3, max(10, progress_width), 24)
            
            # Обновляем текст прогресса
            self.progress_label.setText(f"📊 Прогресс смены: {progress:.1f}%")
            
            # Обновляем время до конца смены
            workday_end = self.game_state.game_time.get('workday_end', 18)
            
            # Расчет оставшегося времени в минутах
            total_minutes_left = (workday_end - current_hour) * 60 - current_minute
            
            if total_minutes_left > 0:
                hours_left = total_minutes_left // 60
                minutes_left = total_minutes_left % 60
                
                if hours_left > 0:
                    time_left_text = f"🕐 До конца смены: {hours_left} ч. {minutes_left} мин."
                else:
                    time_left_text = f"🕐 До конца смены: {minutes_left} мин."
            elif total_minutes_left == 0:
                time_left_text = f"🕐 Смена завершена"
            else:
                time_left_text = f"🕐 Время сверх смены"
                
            self.time_left_label.setText(time_left_text)
            
            # Меняем цвет рамки в зависимости от времени
            time_display_frame = self.findChild(QFrame, "timeDisplay")
            if time_display_frame:
                if current_hour >= 17:
                    time_display_frame.setStyleSheet("""
                        QFrame#timeDisplay {
                            background-color: rgba(30, 10, 10, 0.9);
                            border: 2px solid #ff6b6b;
                            border-radius: 8px;
                            padding: 12px;
                            min-height: 180px;
                        }
                    """)
                elif current_hour >= 13:
                    time_display_frame.setStyleSheet("""
                        QFrame#timeDisplay {
                            background-color: rgba(30, 25, 10, 0.9);
                            border: 2px solid #feca57;
                            border-radius: 8px;
                            padding: 12px;
                            min-height: 180px;
                        }
                    """)
                else:
                    time_display_frame.setStyleSheet("""
                        QFrame#timeDisplay {
                            background-color: rgba(10, 20, 30, 0.9);
                            border: 2px solid #1dd1a1;
                            border-radius: 8px;
                            padding: 12px;
                            min-height: 180px;
                        }
                    """)
                    
        except Exception as e:
            print(f"[ОШИБКА TimeWidget] {str(e)}")
            # Устанавливаем значения по умолчанию при ошибке
            self.date_label.setText("📅 01.01.1984")
            self.hour_label.setText("09")
            self.minute_label.setText("00")
            self.progress_label.setText("📊 Прогресс смены: 0.0%")
            self.time_left_label.setText("🕐 До конца смены: 9 ч. 0 мин.")
            
    def resizeEvent(self, event):
        """Обработка изменения размера"""
        super().resizeEvent(event)
        # Пересчитываем размер прогресс-бара
        if self.game_state:
            try:
                progress = self.game_state.get_workday_progress()
                if self.progress_frame.width() > 10:
                    progress_width = int((progress / 100) * (self.progress_frame.width() - 6))
                    self.progress_bar.setGeometry(3, 3, max(10, progress_width), 24)
            except:
                pass
                
    def paintEvent(self, event):
        """Отрисовка дополнительных эффектов"""
        super().paintEvent(event)
        
        # Эффект свечения вокруг виджета времени
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.game_state:
            try:
                hour = self.game_state.game_time.get('current_hour', 9)
                
                # Определяем цвет свечения по времени суток
                if hour >= 17:  # Вечер
                    glow_color = QColor(255, 107, 107, 30)
                elif hour >= 13:  # День
                    glow_color = QColor(254, 202, 87, 30)
                else:  # Утро
                    glow_color = QColor(29, 209, 161, 30)
                    
                # Рисуем свечение
                painter.setBrush(Qt.NoBrush)
                
                for i in range(3):
                    radius = i * 2
                    alpha = 50 - i * 15
                    glow_color.setAlpha(alpha)
                    painter.setPen(QPen(glow_color, 1))
                    painter.drawRoundedRect(
                        radius, radius,
                        self.width() - 2*radius, self.height() - 2*radius,
                        10, 10
                    )
            except:
                pass
    
    def closeEvent(self, event):
        """Очистка ресурсов при закрытии виджета"""
        self.stop_animations()
        super().closeEvent(event)