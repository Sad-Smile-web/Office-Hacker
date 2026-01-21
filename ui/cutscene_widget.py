# ui/cutscene_widget.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit,
                               QPushButton, QHBoxLayout, QGraphicsOpacityEffect,
                               QSizePolicy, QScrollArea)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import (QFont, QTextCursor, QPalette, QColor,
                          QPainter, QLinearGradient, QPen, QFontMetrics)

class CutsceneWidget(QWidget):
    """Виджет для отображения многочастной кат-сцены с предысторией"""
    
    # Сигнал завершения кат-сцены
    finished = Signal()
    
    def __init__(self, parent=None, player_name=""):
        super().__init__(parent)
        self.parent = parent
        self.player_name = player_name
        self.parts = []  # Список частей кат-сцены
        self.current_part = 0
        self.current_line = 0
        self.char_index = 0
        self.line_complete = False
        self.part_complete = False
        self.final_phrase = ""
        
        # Устанавливаем флаги для предотвращения конфликтов стилей
        self.setAttribute(Qt.WA_StyledBackground, False)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        self.setup_ui()
        self.setup_animations()
        self.setup_blinking()
        
    def setup_ui(self):
        """Настройка интерфейса кат-сцены"""
        # Полностью черный фон
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)
        
        # Основной лейаут
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Индикатор текущей части
        self.part_indicator = QLabel()
        self.part_indicator.setAlignment(Qt.AlignCenter)
        self.part_indicator.setFont(QFont("Arial", 14, QFont.Bold))
        self.part_indicator.setStyleSheet("""
            QLabel {
                color: rgba(180, 180, 255, 200);
                background: transparent;
                border: none;
                padding: 5px;
                margin-bottom: 10px;
            }
        """)
        self.part_indicator.hide()
        
        # Скроллируемая область для текста
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
                padding: 0px;
            }
            QScrollBar:vertical {
                background: #333333;
                width: 10px;
                border-radius: 5px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #00bfff;
                min-height: 30px;
                border-radius: 5px;
                border: none;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Текстовое поле для текущей части
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFrameStyle(0)
        self.text_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # УСТАНАВЛИВАЕМ ОЧЕНЬ БОЛЬШОЙ ШРИФТ
        main_font = QFont()
        main_font.setFamily("Arial")
        main_font.setPointSize(24)  # БОЛЬШОЙ размер шрифта
        main_font.setBold(False)
        self.text_area.setFont(main_font)
        
        # Минимальные стили
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                color: white;
                border: none;
                padding: 20px;
                font-size: 24px;
                line-height: 1.6;
                selection-background-color: transparent;
                selection-color: white;
            }
        """)
        
        self.scroll_area.setWidget(self.text_area)
        
        # Контейнер для нижней панели
        bottom_layout = QVBoxLayout()
        bottom_layout.setSpacing(15)
        
        # Надпись "Нажмите для продолжения" - БУДЕТ МИГАТЬ
        self.continue_label = QLabel("Нажмите любую клавишу для продолжения...")
        self.continue_label.setAlignment(Qt.AlignCenter)
        
        # Устанавливаем шрифт для подсказки
        hint_font = QFont()
        hint_font.setFamily("Arial")
        hint_font.setPointSize(16)
        hint_font.setBold(True)
        self.continue_label.setFont(hint_font)
        
        # Начальный стиль (яркий)
        self.continue_label.setStyleSheet("""
            QLabel {
                color: #00ffff;
                background: transparent;
                border: none;
                padding: 10px;
                text-shadow: 0 0 10px #00ffff;
            }
        """)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.skip_button = QPushButton("Пропустить катсцену")
        self.skip_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.skip_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 50, 50, 80);
                color: white;
                border: 2px solid rgba(255, 100, 100, 150);
                padding: 12px 24px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 6px;
                min-width: 160px;
            }
            QPushButton:hover {
                background-color: rgba(255, 80, 80, 120);
                border: 2px solid rgba(255, 150, 150, 200);
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: rgba(255, 30, 30, 150);
            }
        """)
        self.skip_button.clicked.connect(self.skip_cutscene)
        
        self.next_part_button = QPushButton("Далее →")
        self.next_part_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.next_part_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 150, 255, 120);
                color: white;
                border: 2px solid rgba(0, 150, 255, 200);
                padding: 12px 32px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 6px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: rgba(0, 180, 255, 180);
                border: 2px solid rgba(0, 200, 255, 255);
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: rgba(0, 120, 200, 220);
            }
            QPushButton:disabled {
                background-color: rgba(80, 80, 80, 80);
                color: rgba(180, 180, 180, 150);
                border: 2px solid rgba(120, 120, 120, 100);
            }
        """)
        self.next_part_button.clicked.connect(self.next_part)
        self.next_part_button.hide()
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.skip_button)
        buttons_layout.addWidget(self.next_part_button)
        buttons_layout.addStretch()
        
        bottom_layout.addWidget(self.continue_label)
        bottom_layout.addLayout(buttons_layout)
        
        # Собираем основной лейаут
        main_layout.addWidget(self.part_indicator)
        main_layout.addWidget(self.scroll_area, 1)  # Скроллируемая область занимает все доступное пространство
        main_layout.addLayout(bottom_layout)
        
        # Таймер для эффекта печатания
        self.typewriter_timer = QTimer()
        self.typewriter_timer.timeout.connect(self.type_next_char)
        self.typewriter_timer.setInterval(25)  # Быстрая печать
        
        # Таймер для мигания подсказки
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.blink_continue_label)
        self.blink_timer.setInterval(600)  # Мигаем каждые 600 мс
        
        # Флаг состояния мигания (True - яркий, False - тусклый)
        self.is_bright_mode = True
        
    def setup_animations(self):
        """Настройка анимаций"""
        # Анимация появления виджета
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(1200)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InOutCubic)
        
        # Анимация исчезновения виджета
        self.fade_out_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_animation.setDuration(1200)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.fade_out_animation.finished.connect(self.on_fade_out_finished)
        
        # Анимация перехода между частями
        self.part_fade_out = QPropertyAnimation(self.text_area, b"windowOpacity")
        self.part_fade_out.setDuration(500)
        self.part_fade_out.setStartValue(1.0)
        self.part_fade_out.setEndValue(0.0)
        self.part_fade_out.setEasingCurve(QEasingCurve.OutCubic)
        self.part_fade_out.finished.connect(self.on_part_fade_out_finished)
        
        self.part_fade_in = QPropertyAnimation(self.text_area, b"windowOpacity")
        self.part_fade_in.setDuration(500)
        self.part_fade_in.setStartValue(0.0)
        self.part_fade_in.setEndValue(1.0)
        self.part_fade_in.setEasingCurve(QEasingCurve.InCubic)
        
    def setup_blinking(self):
        """Настройка мигания текста"""
        # Анимация для плавного мигания
        self.blink_animation = QPropertyAnimation(self.continue_label, b"windowOpacity")
        self.blink_animation.setDuration(600)
        self.blink_animation.setStartValue(1.0)
        self.blink_animation.setEndValue(0.3)
        self.blink_animation.setLoopCount(-1)
        self.blink_animation.setEasingCurve(QEasingCurve.InOutSine)
        
    def blink_continue_label(self):
        """Мигание надписи 'продолжить' - переключение между ярким и тусклым"""
        self.is_bright_mode = not self.is_bright_mode
        
        if self.is_bright_mode:
            # Яркий стиль (неоновый синий)
            self.continue_label.setStyleSheet("""
                QLabel {
                    color: #00ffff;
                    background: transparent;
                    border: none;
                    padding: 10px;
                    text-shadow: 0 0 15px #00ffff, 0 0 25px #00ffff;
                }
            """)
        else:
            # Тусклый стиль (темный синий)
            self.continue_label.setStyleSheet("""
                QLabel {
                    color: #006666;
                    background: transparent;
                    border: none;
                    padding: 10px;
                    text-shadow: 0 0 5px #006666;
                }
            """)
        
        # Обновляем виджет
        self.continue_label.update()
    
    def set_cutscene_data(self, parts, final_phrase):
        """Установить данные кат-сцены: список частей и финальную фразу"""
        print(f"[CUTSCENE] Setting cutscene data: {len(parts)} parts, final phrase: '{final_phrase}'")
        
        self.parts = parts
        self.final_phrase = final_phrase
        
        # Подставляем имя игрока в первую часть
        if self.parts and self.player_name:
            self.parts[0] = self.parts[0].format(player_name=self.player_name)
        
        # Показываем индикатор частей, если частей больше 1
        if len(self.parts) > 1:
            self.part_indicator.setText(f"Часть {self.current_part + 1}/{len(self.parts)}")
            self.part_indicator.show()
        
        # Начинаем с первой части
        self.start_current_part()
    
    def start_current_part(self):
        """Начать отображение текущей части"""
        print(f"[CUTSCENE] Starting part {self.current_part + 1}/{len(self.parts)}")
        
        self.current_line = 0
        self.char_index = 0
        self.line_complete = False
        self.part_complete = False
        
        # Очищаем текстовое поле
        self.text_area.clear()
        self.text_area.setWindowOpacity(1.0)
        
        # Устанавливаем шрифт для основной части
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(False)
        self.text_area.setFont(font)
        
        # Обновляем индикатор
        if len(self.parts) > 1:
            self.part_indicator.setText(f"Часть {self.current_part + 1}/{len(self.parts)}")
        
        # Скрываем кнопку "Далее"
        self.next_part_button.hide()
        self.next_part_button.setEnabled(False)
        
        # Устанавливаем текст подсказки
        self.continue_label.setText("Нажмите любую клавишу для продолжения...")
        
        # Запускаем мигание
        self.is_bright_mode = True
        self.continue_label.setStyleSheet("""
            QLabel {
                color: #00ffff;
                background: transparent;
                border: none;
                padding: 10px;
                text-shadow: 0 0 15px #00ffff, 0 0 25px #00ffff;
            }
        """)
        
        # Запускаем таймеры
        self.typewriter_timer.start()
        self.blink_timer.start()
        self.blink_animation.start()
        
        print(f"[CUTSCENE] Timers started for part {self.current_part + 1}")
    
    def type_next_char(self):
        """Эффект печатания следующего символа текущей части"""
        if self.current_part >= len(self.parts):
            self.typewriter_timer.stop()
            return
            
        current_text = self.text_area.toPlainText()
        
        # Получаем текущую часть
        part_text = self.parts[self.current_part]
        
        # Разбиваем на строки
        lines = part_text.split('\n')
        
        # Если строка завершена, переходим к следующей
        if self.line_complete:
            self.text_area.append("")  # Пустая строка
            self.current_line += 1
            self.char_index = 0
            self.line_complete = False
            
            # Если это была последняя строка в части
            if self.current_line >= len(lines):
                self.on_part_complete()
                return
        
        # Получаем текущую строку
        if self.current_line < len(lines):
            line = lines[self.current_line]
            
            # Добавляем следующий символ
            if self.char_index < len(line):
                char = line[self.char_index]
                current_text_lines = current_text.split('\n')
                
                if self.char_index == 0:
                    current_text_lines[-1] = char
                else:
                    current_text_lines[-1] += char
                    
                self.text_area.setPlainText('\n'.join(current_text_lines))
                self.char_index += 1
                
                # Прокручиваем к концу
                cursor = self.text_area.textCursor()
                cursor.movePosition(QTextCursor.End)
                self.text_area.setTextCursor(cursor)
                
                # Пауза после знаков препинания
                if char in '.!?':
                    self.typewriter_timer.setInterval(100)  # Дольше пауза
                elif char in ',;:':
                    self.typewriter_timer.setInterval(60)
                else:
                    self.typewriter_timer.setInterval(25)
            else:
                # Строка завершена
                self.line_complete = True
        else:
            # Часть завершена
            self.on_part_complete()
    
    def on_part_complete(self):
        """Когда текущая часть завершена"""
        print(f"[CUTSCENE] Part {self.current_part + 1} completed")
        
        self.typewriter_timer.stop()
        self.part_complete = True
        
        # Показываем кнопку "Далее" для перехода к следующей части
        if self.current_part < len(self.parts):
            self.next_part_button.show()
            self.next_part_button.setEnabled(True)
            
            # Для последней части меняем текст кнопки
            if self.current_part == len(self.parts) - 1:
                self.next_part_button.setText("Завершить →")
            else:
                self.next_part_button.setText("Далее →")
    
    def next_part(self):
        """Перейти к следующей части или завершить кат-сцену"""
        print(f"[CUTSCENE] Next part requested, current part: {self.current_part}, total parts: {len(self.parts)}")
        
        if self.current_part < len(self.parts) - 1:
            # Анимация исчезновения текущей части
            self.part_fade_out.start()
        else:
            # Это последняя часть - показываем финальную фразу
            self.show_final_phrase()
    
    def on_part_fade_out_finished(self):
        """Когда анимация исчезновения части завершена"""
        # Переходим к следующей части
        self.current_part += 1
        
        # Запускаем новую часть
        self.start_current_part()
        
        # Запускаем анимацию появления
        self.part_fade_in.start()
    
    def show_final_phrase(self):
        """Показать финальную фразу"""
        print(f"[CUTSCENE] Showing final phrase: {self.final_phrase}")
        
        # Останавливаем текущие таймеры
        self.typewriter_timer.stop()
        self.blink_timer.stop()
        self.blink_animation.stop()
        
        # Скрываем кнопки
        self.next_part_button.hide()
        self.skip_button.hide()
        self.part_indicator.hide()
        
        # Очищаем текст
        self.text_area.clear()
        self.text_area.setWindowOpacity(1.0)
        
        # Устанавливаем ОГРОМНЫЙ шрифт для финальной фразы
        final_font = QFont()
        final_font.setFamily("Arial")
        final_font.setPointSize(48)  # ОЧЕНЬ БОЛЬШОЙ размер
        final_font.setBold(True)
        self.text_area.setFont(final_font)
        
        # Устанавливаем стиль для финальной фразы
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 48px;
                font-weight: bold;
                line-height: 1.8;
                padding: 40px;
                text-align: center;
            }
        """)
        
        # Устанавливаем финальную фразу
        self.text_area.setPlainText(self.final_phrase)
        
        # Центрируем текст
        cursor = self.text_area.textCursor()
        cursor.select(QTextCursor.Document)
        block_format = cursor.blockFormat()
        block_format.setAlignment(Qt.AlignCenter)
        cursor.mergeBlockFormat(block_format)
        self.text_area.setTextCursor(cursor)
        
        # Обновляем подсказку
        self.continue_label.setText("Нажмите любую клавишу, чтобы начать игру...")
        
        # Устанавливаем другой цвет для финальной подсказки (зеленый)
        self.continue_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                background: transparent;
                border: none;
                padding: 10px;
                text-shadow: 0 0 15px #00ff00, 0 0 25px #00ff00;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        self.continue_label.show()
        
        # Запускаем мигание с другим интервалом для финальной фразы
        self.blink_timer.setInterval(800)  # Немного медленнее
        self.blink_timer.start()
        
        # Запускаем анимацию мигания
        self.blink_animation.setDuration(800)
        self.blink_animation.start()
        
        print("[CUTSCENE] Final phrase displayed, waiting for user input")
    
    def skip_cutscene(self):
        """Пропустить кат-сцену"""
        print("[CUTSCENE] Cutscene skipped by user")
        
        # Останавливаем все таймеры
        self.typewriter_timer.stop()
        self.blink_timer.stop()
        self.blink_animation.stop()
        
        if not self.part_complete:
            # Показываем всю текущую часть сразу
            if self.current_part < len(self.parts):
                self.text_area.setPlainText(self.parts[self.current_part])
                self.on_part_complete()
        elif self.current_part < len(self.parts):
            # Пропускаем к следующей части или к финальной фразе
            if self.current_part < len(self.parts) - 1:
                self.next_part()
            else:
                # Пропускаем к финальной фразе
                self.show_final_phrase()
        else:
            # Если уже на финальной фразе, завершаем катсцену
            self.start_fade_out()
    
    def start_fade_out(self):
        """Начать плавное исчезновение кат-сцены"""
        print("[CUTSCENE] Starting fade out")
        
        # Останавливаем все таймеры
        self.typewriter_timer.stop()
        self.blink_timer.stop()
        self.blink_animation.stop()
        
        # Запускаем анимацию исчезновения
        self.fade_out_animation.start()
    
    def on_fade_out_finished(self):
        """Когда исчезновение завершено"""
        print("[CUTSCENE] Fade out completed, emitting finished signal")
        
        # Испускаем сигнал завершения
        self.finished.emit()
    
    def showEvent(self, event):
        """При показе виджета"""
        super().showEvent(event)
        
        print("[CUTSCENE] Cutscene widget shown, starting fade in")
        
        # Запускаем анимацию появления
        self.fade_in_animation.start()
        
        # Устанавливаем фокус
        self.setFocus()
        
        # Захватываем клавиатуру
        self.grabKeyboard()
    
    def hideEvent(self, event):
        """При скрытии виджета"""
        super().hideEvent(event)
        
        # Освобождаем клавиатуру
        self.releaseKeyboard()
    
    def keyPressEvent(self, event):
        """Обработка нажатия клавиш"""
        # Игнорируем служебные клавиши
        if event.key() in [Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta, Qt.Key_CapsLock]:
            return
            
        print(f"[CUTSCENE] Key pressed: {event.key()}")
        
        if not self.part_complete:
            # Ускорение печати текущей строки
            if self.line_complete:
                self.type_next_char()
            else:
                # Показать всю текущую строку сразу
                part_text = self.parts[self.current_part]
                lines = part_text.split('\n')
                
                if self.current_line < len(lines):
                    line = lines[self.current_line]
                    current_text = self.text_area.toPlainText()
                    current_text_lines = current_text.split('\n')
                    
                    if current_text_lines:
                        current_text_lines[-1] = line
                        self.text_area.setPlainText('\n'.join(current_text_lines))
                    
                    self.line_complete = True
                    self.char_index = len(line)
                    
                    # Если это была последняя строка в части
                    if self.current_line >= len(lines) - 1:
                        self.on_part_complete()
        elif self.current_part < len(self.parts):
            # Если есть кнопка "Далее", нажимаем ее
            if self.next_part_button.isVisible() and self.next_part_button.isEnabled():
                self.next_part_button.click()
            else:
                # Иначе завершаем кат-сцену
                self.start_fade_out()
        else:
            # Если уже на финальной фразе, завершаем кат-сцену
            self.start_fade_out()
    
    def mousePressEvent(self, event):
        """Обработка клика мыши"""
        print("[CUTSCENE] Mouse click detected")
        
        # Обрабатываем клик как нажатие клавиши
        self.keyPressEvent(event)
    
    def paintEvent(self, event):
        """Отрисовка фона с эффектами"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Градиентный фон от темно-синего к черному
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(10, 10, 40))     # Темно-синий сверху
        gradient.setColorAt(0.3, QColor(8, 8, 30))       # Немного темнее
        gradient.setColorAt(0.7, QColor(5, 5, 20))       # Еще темнее
        gradient.setColorAt(1.0, QColor(0, 0, 0))        # Черный снизу
        
        painter.fillRect(self.rect(), gradient)
        
        # Эффект сканирующих линий (очень прозрачный)
        painter.setOpacity(0.03)
        painter.setPen(QPen(QColor(0, 255, 255, 30), 1))
        
        line_spacing = 4
        for y in range(0, self.height(), line_spacing):
            painter.drawLine(0, y, self.width(), y)
        
        # Эффект углов (киберпанк стиль)
        painter.setOpacity(0.4)
        painter.setPen(QPen(QColor(0, 191, 255, 100), 2))
        
        corner_size = 40
        line_length = 20
        
        # Левый верхний угол
        painter.drawLine(20, 20, 20 + line_length, 20)
        painter.drawLine(20, 20, 20, 20 + line_length)
        
        # Правый верхний угол
        painter.drawLine(self.width() - 20, 20, self.width() - 20 - line_length, 20)
        painter.drawLine(self.width() - 20, 20, self.width() - 20, 20 + line_length)
        
        # Левый нижний угол
        painter.drawLine(20, self.height() - 20, 20 + line_length, self.height() - 20)
        painter.drawLine(20, self.height() - 20, 20, self.height() - 20 - line_length)
        
        # Правый нижний угол
        painter.drawLine(self.width() - 20, self.height() - 20, 
                        self.width() - 20 - line_length, self.height() - 20)
        painter.drawLine(self.width() - 20, self.height() - 20, 
                        self.width() - 20, self.height() - 20 - line_length)
        
        # Центральные линии перекрестия (очень прозрачные)
        painter.setOpacity(0.05)
        painter.setPen(QPen(QColor(255, 255, 255, 50), 1))
        
        # Горизонтальная линия
        painter.drawLine(0, self.height() // 2, self.width(), self.height() // 2)
        
        # Вертикальная линия
        painter.drawLine(self.width() // 2, 0, self.width() // 2, self.height())
        
        # Круг в центре
        painter.drawEllipse(self.width() // 2 - 25, self.height() // 2 - 25, 50, 50)
        
        painter.setOpacity(1.0)
        
        # Вызываем базовую отрисовку виджета
        super().paintEvent(event)

# Минимальная версия для тестирования
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Создаем тестовую катсцену
    window = CutsceneWidget()
    window.setWindowTitle("Тест катсцены")
    window.resize(1000, 700)
    
    # Тестовые данные
    test_parts = [
        "Это первая часть катсцены.\n\nГод 2140. Мир изменился после многолетней войны.\nВласть сосредоточилась в руках большой корпорации.",
        "Это вторая часть катсцены.\n\nSIBERIA-SOFTWARE стала самой крупной корпорацией,\nконтролируя 99% киберпространства Евразии.",
        "Это третья часть катсцены.\n\nВы - новый сотрудник Отдела Кибербезопасности МВД.\nВаша задача - обеспечивать безопасность граждан."
    ]
    
    test_final_phrase = "Добро пожаловать в корпорацию SIBERIA-SOFTWARE."
    
    window.set_cutscene_data(test_parts, test_final_phrase)
    window.show()
    
    # Подключаем сигнал завершения
    window.finished.connect(lambda: print("Катсцена завершена!"))
    
    sys.exit(app.exec())