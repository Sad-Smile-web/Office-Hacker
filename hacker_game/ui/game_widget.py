from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QTextEdit, QFrame,
                               QListWidget, QListWidgetItem, QStackedWidget)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QPainter, QColor, QBrush, QLinearGradient, QPen, QRadialGradient
from ui.terminal_widget import TerminalWidget
from ui.time_widget import TimeWidget
from ui.skills_widget import SkillsWidget
from simple_translation import translation
import random
import math
import time

class GameWidget(QWidget):
    back_to_menu = Signal()
    
    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self.game_state = game_state
        self._mail_opened_for_task = False
        self._last_task = ""
        self.init_ui()
        self.setup_timers()
        
    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # ЛЕВАЯ ПАНЕЛЬ - стек для переключения между информацией и навыками
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 10, 20, 0.8);
                border: 2px solid #00bfff;
                border-radius: 8px;
                min-width: 320px;
            }
        """)
        
        # Создаем стек для левой панели
        self.left_stack = QStackedWidget()
        
        # Виджет 1: Информация о сотруднике
        self.info_widget = self.create_info_widget()
        
        # Виджет 2: Детальные навыки
        self.skills_widget = SkillsWidget(self.game_state, self)
        self.skills_widget.back_to_info.connect(self.show_employee_info)
        
        # Добавляем виджеты в стек
        self.left_stack.addWidget(self.info_widget)
        self.left_stack.addWidget(self.skills_widget)
        
        # Устанавливаем стек в левую панель
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.left_stack)
        left_panel.setLayout(left_layout)
        
        # Центральная панель - терминал
        self.terminal = TerminalWidget(self)
        
        # Правая панель - стек для переключения между наблюдением и почтой
        right_panel = QFrame()
        right_panel.setMinimumWidth(320)
        right_panel.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 10, 30, 0.8);
                border: 2px solid #ff4444;
                border-radius: 8px;
            }
        """)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(15, 15, 15, 15)
        right_layout.setSpacing(10)
        
        # Стек для переключения между наблюдением и почтой
        self.right_stack = QStackedWidget()
        
        # Создаем виджет наблюдения
        surveillance_widget = self.create_surveillance_widget()
        
        # Создаем виджет почты
        self.mail_widget = MailWidget(self, self.game_state)
        self.mail_widget.back_to_surveillance.connect(self.show_surveillance)
        self.mail_widget.email_read.connect(self.on_email_read)
        
        self.right_stack.addWidget(surveillance_widget)
        self.right_stack.addWidget(self.mail_widget)
        
        right_layout.addWidget(self.right_stack)
        right_panel.setLayout(right_layout)
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.terminal, 2)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        
        # Обновляем прогресс-бары после инициализации
        self.update_progress_bar()
        
    def create_info_widget(self):
        """Создать виджет с информацией о сотруднике"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Заголовок панели сотрудника
        employee_header = QLabel(translation.t("game.employee_status"))
        employee_header.setAlignment(Qt.AlignCenter)
        employee_header.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #00bfff;
            padding: 5px;
            background-color: rgba(0, 34, 68, 0.5);
            border-radius: 5px;
            margin-bottom: 10px;
        """)
        
        # Статус сотрудника
        self.name_label = QLabel(f"{translation.t('game.employee')}: {self.game_state.player_name}")
        self.name_label.setStyleSheet("font-weight: bold; color: #ffffff; font-size: 14px;")
        self.day_label = QLabel(translation.t('game.day', day=self.game_state.day))
        self.day_label.setStyleSheet("color: #cccccc;")
        self.money_label = QLabel(translation.t('game.balance', money=self.game_state.get_money_display()))
        self.money_label.setStyleSheet("color: #ffd700; font-weight: bold; font-size: 13px;")
        self.rep_label = QLabel(translation.t('game.reputation', reputation=self.game_state.reputation))
        self.rep_label.setStyleSheet("color: #ffaa00; font-weight: bold;")
        
        # Кнопка почты с счетчиком непрочитанных
        self.mail_button = QPushButton()
        self.update_mail_button()
        self.mail_button.clicked.connect(self.open_mail)
        
        # Кнопка навыков
        self.skills_button = QPushButton(translation.t("game.skills"))
        self.skills_button.clicked.connect(self.open_skills)
        self.skills_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(42, 42, 62, 0.9);
                color: #cccccc;
                border: 1px solid #00bfff;
                padding: 8px;
                font-weight: bold;
                border-radius: 6px;
                margin-top: 5px;
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
        
        # Разделитель перед временем
        separator_before_time = QFrame()
        separator_before_time.setFrameShape(QFrame.HLine)
        separator_before_time.setStyleSheet("background-color: #00bfff; height: 1px; margin: 5px 0;")
        
        # Виджет времени
        self.time_widget = TimeWidget(self.game_state)
        self.time_widget.setMinimumHeight(150)  # Оптимальная высота
        
        # Разделитель после времени
        separator_after_time = QFrame()
        separator_after_time.setFrameShape(QFrame.HLine)
        separator_after_time.setStyleSheet("background-color: #00bfff; height: 1px; margin: 5px 0;")
        
        # Задачи
        task_header = QLabel(translation.t("game.current_task"))
        task_header.setStyleSheet("font-weight: bold; color: #8a6d3b; font-size: 14px;")
        self.task_text = QLabel(self.game_state.current_task)
        self.task_text.setWordWrap(True)
        self.task_text.setStyleSheet("""
            color: #cccccc; 
            padding: 10px; 
            background-color: rgba(26, 26, 26, 0.7); 
            border: 1px solid #444444; 
            border-radius: 5px;
            font-size: 13px;
        """)
        
        # Прогресс задачи
        self.task_progress_frame = QFrame()
        self.task_progress_frame.setStyleSheet("background-color: transparent;")
        task_progress_layout = QVBoxLayout()
        task_progress_layout.setContentsMargins(0, 5, 0, 5)
        
        self.progress_label = QLabel(translation.t('game.progress', progress=self.game_state.current_task_progress))
        self.progress_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        
        self.progress_bar_bg = QFrame()
        self.progress_bar_bg.setFixedHeight(12)
        self.progress_bar_bg.setStyleSheet("""
            QFrame {
                background-color: #333333;
                border-radius: 6px;
            }
        """)
        
        self.progress_bar_fill = QFrame(self.progress_bar_bg)
        self.progress_bar_fill.setFixedHeight(8)
        self.progress_bar_fill.setStyleSheet("""
            QFrame {
                background-color: #00bfff;
                border-radius: 4px;
                margin: 2px;
            }
        """)
        
        task_progress_layout.addWidget(self.progress_label)
        task_progress_layout.addWidget(self.progress_bar_bg)
        self.task_progress_frame.setLayout(task_progress_layout)
        
        # Кнопка возврата в меню
        menu_btn = QPushButton(translation.t("game.main_menu"))
        menu_btn.clicked.connect(self.back_to_menu.emit)
        menu_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(42, 42, 42, 0.9);
                color: #cccccc;
                border: 1px solid #00bfff;
                padding: 10px;
                font-weight: bold;
                border-radius: 6px;
                margin-top: 10px;
                font-size: 13px;
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
        
        # Добавляем все в layout виджета информации
        layout.addWidget(employee_header)
        layout.addWidget(self.name_label)
        layout.addWidget(self.day_label)
        layout.addWidget(self.money_label)
        layout.addWidget(self.rep_label)
        layout.addWidget(self.mail_button)
        layout.addWidget(self.skills_button)
        layout.addWidget(separator_before_time)
        layout.addWidget(self.time_widget)
        layout.addWidget(separator_after_time)
        layout.addWidget(task_header)
        layout.addWidget(self.task_text)
        layout.addWidget(self.task_progress_frame)
        layout.addStretch()
        layout.addWidget(menu_btn)
        
        widget.setLayout(layout)
        return widget
        
    def create_surveillance_widget(self):
        """Создать виджет наблюдения"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        self.camera_header = QLabel(translation.t("game.surveillance_system"))
        self.camera_header.setAlignment(Qt.AlignCenter)
        self.camera_header.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #ff4444;
            padding: 5px;
            background-color: rgba(68, 0, 0, 0.5);
            border-radius: 5px;
            margin-bottom: 10px;
        """)
        
        self.office_view = OfficeView(self)
        
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.HLine)
        separator3.setStyleSheet("background-color: #ff4444; height: 1px; margin: 10px 0;")
        
        security_header = QLabel(translation.t("game.security_log"))
        security_header.setStyleSheet("font-weight: bold; color: #ff4444; font-size: 14px;")
        
        self.security_log = QTextEdit()
        self.security_log.setMaximumHeight(180)
        self.security_log.setReadOnly(True)
        self.security_log.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #ff8888;
                font-size: 11px;
                font-family: 'Courier New', monospace;
                border: 1px solid #880000;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #660000;
            }
            QScrollBar:vertical {
                background: #330000;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #ff4444;
                min-height: 20px;
                border-radius: 5px;
            }
        """)
        
        # Используем переводы для лога безопасности
        self.security_log.setText(f"""
[{translation.t('game.security_system_title')}]
┌─────────────────────────────────────┐
│ • {translation.t('game.camera1')}         │
│ • {translation.t('game.camera2')}       │
│ • {translation.t('game.camera3')}│
│ • {translation.t('game.microphones')}                │
│ • {translation.t('game.motion_sensors')}         │
│ • {translation.t('game.status_all_operational')}    │
└─────────────────────────────────────┘

[{translation.t('game.recent_events')}]
• 08:30 - {translation.t('game.shift_started')}
• 08:45 - {translation.t('game.security_check')}
• 09:00 - {translation.t('game.daily_meeting')}
• 09:15 - {translation.t('game.network_activity')}
        """)
        
        layout.addWidget(self.camera_header)
        layout.addWidget(self.office_view)
        layout.addWidget(separator3)
        layout.addWidget(security_header)
        layout.addWidget(self.security_log)
        widget.setLayout(layout)
        return widget
        
    def setup_timers(self):
        """Настройка таймеров для обновления игры"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui)
        self.update_timer.start(1000)
        
        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self.random_security_event)
        self.log_timer.start(15000)
        
        self.special_email_timer = QTimer()
        self.special_email_timer.timeout.connect(self.check_special_emails)
        self.special_email_timer.start(30000)
        
    def update_game_data(self):
        """Обновить данные игры в виджете"""
        try:
            if hasattr(self, 'name_label'):
                self.name_label.setText(f"{translation.t('game.employee')}: {self.game_state.player_name}")
            
            if hasattr(self, 'day_label'):
                self.day_label.setText(translation.t('game.day', day=self.game_state.day))
            
            if hasattr(self, 'money_label'):
                self.money_label.setText(translation.t('game.balance', money=self.game_state.get_money_display()))
            
            if hasattr(self, 'rep_label'):
                self.rep_label.setText(translation.t('game.reputation', reputation=self.game_state.reputation))
            
            print(f"[GAME WIDGET] {translation.t('game.data_updated_for')} {self.game_state.player_name}")
        except Exception as e:
            print(f"❌ {translation.t('game.error.game_widget_update')}: {e}")
        
    def update_ui(self):
        """Обновление интерфейса"""
        # Обновляем основные данные игры
        self.update_game_data()
        
        # Обновляем информацию о задаче
        self.task_text.setText(self.game_state.current_task)
        self.progress_label.setText(translation.t('game.progress', progress=self.game_state.current_task_progress))
        
        self.update_progress_bar()
        self.update_mail_button()
        
        # Обновляем виджет навыков, если он открыт
        if self.left_stack.currentIndex() == 1:
            self.skills_widget.update_ui()
        
        if hasattr(self, 'time_widget'):
            self.time_widget.update_display()
                
    def update_progress_bar(self):
        """Обновить прогресс-бар задачи"""
        if self.progress_bar_bg.width() > 4:
            progress = max(0, min(self.game_state.current_task_progress, 100))
            width = int((progress / 100) * (self.progress_bar_bg.width() - 4))
            self.progress_bar_fill.setFixedWidth(max(0, min(width, self.progress_bar_bg.width() - 4)))
        
    def update_mail_button(self):
        """Обновить кнопку почты"""
        unread = self.game_state.unread_emails
        badge = f" ({unread})" if unread > 0 else ""
        
        self.mail_button.setText(f"{translation.t('game.mail')}{badge}")
        self.mail_button.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(42, 42, 62, 0.9);
                color: #cccccc;
                border: 1px solid #8a2be2;
                padding: 8px;
                font-weight: bold;
                border-radius: 6px;
                margin-top: 5px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: rgba(100, 50, 200, 0.8);
                border-color: #9370db;
                color: #ffffff;
                border-width: 2px;
            }}
            QPushButton:pressed {{
                background-color: rgba(70, 30, 150, 0.9);
            }}
        """)
        
    def random_security_event(self):
        """Случайное событие в логе безопасности"""
        events = [
            translation.t('game.security_event.user_activity', id=random.randint(1000, 9999)),
            translation.t('game.security_event.loyalty_check'),
            translation.t('game.security_event.network_scan'),
            translation.t('game.security_event.data_integrity'),
            translation.t('game.security_event.traffic_analysis'),
            translation.t('game.security_event.monitoring_active'),
            translation.t('game.security_event.access_logs'),
            translation.t('game.security_event.motion_test'),
        ]
        
        if random.random() < 0.3:
            event = random.choice(events)
            current_time = time.strftime("%H:%M:%S")
            
            current_log = self.security_log.toPlainText()
            lines = current_log.split('\n')
            
            if len(lines) > 15:
                lines = lines[:8] + lines[-(15-8):]
            
            new_line = f"• {current_time} - {event}"
            lines.insert(8, new_line)
            
            self.security_log.setText('\n'.join(lines))
            
    def add_security_log(self, message: str):
        """Добавить сообщение в лог безопасности"""
        current = self.security_log.toPlainText()
        lines = current.split('\n')
        
        if len(lines) > 15:
            lines = lines[:8] + lines[-(15-8):]
        
        current_time = time.strftime("%H:%M:%S")
        lines.insert(8, f"• {current_time} - {message}")
        self.security_log.setText('\n'.join(lines))
        
    def open_mail(self):
        """Открыть почтовую систему"""
        current_task = self.game_state.current_task
        
        # Если задача изменилась, сбрасываем флаг
        if current_task != self._last_task:
            self._mail_opened_for_task = False
            self._last_task = current_task
        
        # Переключаемся на почту
        self.right_stack.setCurrentIndex(1)
        self.camera_header.setText(translation.t("game.mail_client"))
        self.camera_header.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #8a2be2;
            padding: 5px;
            background-color: rgba(68, 0, 68, 0.5);
            border-radius: 5px;
            margin-bottom: 10px;
        """)
        
        self.right_stack.parent().parent().setStyleSheet("""
            QFrame {
                background-color: rgba(10, 10, 30, 0.8);
                border: 2px solid #8a2be2;
                border-radius: 8px;
            }
        """)
        
        self.mail_widget.load_emails()
        
        # Если задача про почту, добавляем прогресс за первое открытие
        if self.game_state.current_task == translation.t("tasks.check_mvd_email"):
            if not self._mail_opened_for_task and self.game_state.current_task_progress < 30:
                self.game_state.add_mail_task_progress(30)
                self._mail_opened_for_task = True
                self.update_ui()
        
        self.add_security_log(translation.t("game.access_mail_system"))
    
    def show_surveillance(self):
        """Вернуться к системе наблюдения"""
        self.right_stack.setCurrentIndex(0)
        self.camera_header.setText(translation.t("game.surveillance_system"))
        self.camera_header.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #ff4444;
            padding: 5px;
            background-color: rgba(68, 0, 0, 0.5);
            border-radius: 5px;
            margin-bottom: 10px;
        """)
        
        self.right_stack.parent().parent().setStyleSheet("""
            QFrame {
                background-color: rgba(10, 10, 30, 0.8);
                border: 2px solid #ff4444;
                border-radius: 8px;
            }
        """)
        
    def open_skills(self):
        """Открыть панель навыков"""
        self.left_stack.setCurrentIndex(1)
        self.skills_widget.update_ui()
        
    def show_employee_info(self):
        """Вернуться к информации о сотруднике"""
        self.left_stack.setCurrentIndex(0)
        
    def on_email_read(self, email_id):
        """Обработчик прочтения письма"""
        self.update_mail_button()
        
        email = self.game_state.email_system.get_email_by_id(email_id)
        if email and email.get_sender() == translation.t("email.mvd"):
            if self.game_state.current_task == translation.t("tasks.check_mvd_email"):
                if self.game_state.current_task_progress < 100:
                    remaining = 100 - self.game_state.current_task_progress
                    if self.game_state.mark_email_as_read(email_id):
                        self.terminal.output.append(f"[{translation.t('game.system')}] {translation.t('game.mvd_email_read')}")
                        self.terminal.output.moveCursor(self.terminal.output.textCursor().MoveOperation.End)
                        self.update_ui()
    
    def check_special_emails(self):
        """Проверить условия для отправки специальных писем"""
        if self.game_state and self.game_state.email_system:
            self.game_state.check_special_emails()
            
            if hasattr(self, 'mail_widget') and self.mail_widget:
                self.update_mail_button()
                
                if self.right_stack.currentIndex() == 1:
                    self.mail_widget.load_emails()
    
    def retranslate_ui(self):
        """Обновить переводы интерфейса"""
        # Обновляем статические тексты
        if hasattr(self, 'info_widget'):
            # Обновляем заголовки
            if hasattr(self, 'employee_header'):
                self.employee_header.setText(translation.t("game.employee_status"))
            
            # Обновляем кнопки
            if hasattr(self, 'mail_button'):
                self.update_mail_button()
            
            if hasattr(self, 'skills_button'):
                self.skills_button.setText(translation.t("game.skills"))
        
        # Обновляем почту
        if hasattr(self, 'mail_widget'):
            self.mail_widget.retranslate_ui()
        
        # Обновляем заголовок наблюдения
        if hasattr(self, 'camera_header'):
            if self.right_stack.currentIndex() == 0:
                self.camera_header.setText(translation.t("game.surveillance_system"))
            else:
                self.camera_header.setText(translation.t("game.mail_client"))
    
    def resizeEvent(self, event):
        """Обработчик изменения размера окна"""
        super().resizeEvent(event)
        self.update_progress_bar()
        
        # Обновляем виджет навыков, если он открыт
        if self.left_stack.currentIndex() == 1:
            self.skills_widget.update_ui()
    
    def closeEvent(self, event):
        """Сохранить игру при закрытии"""
        self.game_state.save()
        event.accept()


class MailWidget(QWidget):
    """Виджет почтового клиента"""
    back_to_surveillance = Signal()
    email_read = Signal(int)
    
    def __init__(self, parent=None, game_state=None):
        super().__init__(parent)
        self.game_state = game_state
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        self.back_button = QPushButton(translation.t("email.back_to_surveillance"))
        self.back_button.clicked.connect(self.back_to_surveillance.emit)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(68, 0, 68, 0.8);
                color: #cccccc;
                border: 1px solid #8a2be2;
                padding: 8px;
                font-weight: bold;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(100, 50, 200, 0.8);
                border-color: #9370db;
                color: #ffffff;
                border-width: 2px;
            }
            QPushButton:pressed {
                background-color: rgba(70, 30, 150, 0.9);
            }
        """)
        
        self.mail_stats = QLabel()
        self.update_mail_stats()
        self.mail_stats.setStyleSheet("color: #cccccc; font-size: 12px; padding: 5px;")
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #8a2be2; height: 1px; margin: 5px 0;")
        
        self.mail_list_label = QLabel(translation.t("email.inbox_messages"))
        self.mail_list_label.setStyleSheet("font-weight: bold; color: #9370db; font-size: 13px;")
        
        self.mail_list = QListWidget()
        self.mail_list.setStyleSheet("""
            QListWidget {
                background-color: #000000;
                border: 1px solid #4b0082;
                border-radius: 5px;
                padding: 5px;
                color: #cccccc;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333333;
            }
            QListWidget::item:selected {
                background-color: #4b0082;
                border: 1px solid #9370db;
                border-radius: 3px;
            }
            QListWidget::item:hover {
                background-color: #2d004d;
            }
            QScrollBar:vertical {
                background: #330033;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #8a2be2;
                min-height: 20px;
                border-radius: 5px;
            }
        """)
        
        self.mail_view_label = QLabel(translation.t("email.view_message"))
        self.mail_view_label.setStyleSheet("font-weight: bold; color: #9370db; font-size: 13px;")
        
        self.mail_view = QTextEdit()
        self.mail_view.setMaximumHeight(250)
        self.mail_view.setReadOnly(True)
        self.mail_view.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #cccccc;
                font-size: 14px;
                font-family: 'Courier New', monospace;
                border: 1px solid #4b0082;
                border-radius: 5px;
                padding: 12px;
                selection-background-color: #4b0082;
                line-height: 1.4;
            }
            QScrollBar:vertical {
                background: #330033;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #8a2be2;
                min-height: 25px;
                border-radius: 6px;
            }
        """)
        
        button_layout = QHBoxLayout()
        
        self.read_button = QPushButton(translation.t("email.mark_as_read"))
        self.read_button.clicked.connect(self.mark_as_read)
        self.read_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(42, 42, 62, 0.9);
                color: #cccccc;
                border: 1px solid #8a2be2;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(100, 50, 200, 0.8);
                border-color: #9370db;
                color: #ffffff;
            }
        """)
        
        self.delete_button = QPushButton(translation.t("email.delete"))
        self.delete_button.clicked.connect(self.delete_mail)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(62, 42, 42, 0.9);
                color: #cccccc;
                border: 1px solid #ff4444;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(200, 50, 50, 0.8);
                border-color: #ff8888;
                color: #ffffff;
            }
        """)
        
        button_layout.addWidget(self.read_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        
        self.mail_list.currentRowChanged.connect(self.show_mail_content)
        
        layout.addWidget(self.back_button)
        layout.addWidget(self.mail_stats)
        layout.addWidget(separator)
        layout.addWidget(self.mail_list_label)
        layout.addWidget(self.mail_list)
        layout.addWidget(self.mail_view_label)
        layout.addWidget(self.mail_view)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        self.load_emails()
        
        if self.mail_list.count() > 0:
            self.mail_list.setCurrentRow(0)
    
    def update_mail_stats(self):
        """Обновить статистику почты"""
        if self.game_state and self.game_state.email_system:
            total = self.game_state.email_system.get_total_count()
            unread = self.game_state.email_system.get_unread_count()
            self.mail_stats.setText(
                translation.t("email.stats", total=total, unread=unread)
            )
    
    def load_emails(self):
        """Загрузить письма"""
        self.mail_list.clear()
        
        if self.game_state and self.game_state.email_system:
            emails = self.game_state.email_system.get_emails("inbox")
            
            sorted_emails = sorted(emails, 
                                  key=lambda e: (not e.read, not e.important, e.date), 
                                  reverse=True)
            
            for email in sorted_emails:
                icon = "✉" if not email.read else "✓"
                if email.important:
                    icon = "⚠" if not email.read else "✓⚠"
                
                # Используем методы с переводами
                sender = email.get_sender()
                subject = email.get_subject()
                item_text = f"{icon} [{email.date}] {sender}: {subject}"
                item = QListWidgetItem(item_text)
                
                if not email.read:
                    item.setForeground(QColor("#ffffff"))
                    item.setFont(QFont("Arial", 13, QFont.Bold))
                else:
                    item.setForeground(QColor("#888888"))
                    item.setFont(QFont("Arial", 12, QFont.Normal))
                
                if email.important and not email.read:
                    item.setBackground(QColor(100, 0, 0, 50))
                
                item.setData(Qt.UserRole, email.id)
                self.mail_list.addItem(item)
        
        self.update_mail_stats()
    
    def show_mail_content(self, index):
        """Показать содержимое письма"""
        if index >= 0 and self.game_state and self.game_state.email_system:
            item = self.mail_list.item(index)
            if item:
                email_id = item.data(Qt.UserRole)
                email = self.game_state.email_system.get_email_by_id(email_id)
                if email:
                    # Используем метод с переводом
                    self.mail_view.setText(email.get_content())
    
    def mark_as_read(self):
        """Пометить письмо как прочитанное"""
        index = self.mail_list.currentRow()
        if index >= 0 and self.game_state and self.game_state.email_system:
            item = self.mail_list.item(index)
            if item:
                email_id = item.data(Qt.UserRole)
                
                email = self.game_state.email_system.get_email_by_id(email_id)
                if not email:
                    return
                
                if self.game_state.mark_email_as_read(email_id):
                    icon = "✓" + ("⚠" if email.important else "")
                    # Используем методы с переводами
                    sender = email.get_sender()
                    subject = email.get_subject()
                    item_text = f"{icon} [{email.date}] {sender}: {subject}"
                    item.setText(item_text)
                    item.setForeground(QColor("#888888"))
                    item.setFont(QFont("Arial", 12, QFont.Normal))
                    item.setBackground(QColor(0, 0, 0, 0))
                    
                    self.update_mail_stats()
                    self.email_read.emit(email_id)
    
    def delete_mail(self):
        """Удалить письмо"""
        index = self.mail_list.currentRow()
        if index >= 0 and self.game_state and self.game_state.email_system:
            item = self.mail_list.item(index)
            if item:
                email_id = item.data(Qt.UserRole)
                
                if self.game_state.email_system.delete_email(email_id):
                    self.mail_list.takeItem(index)
                    self.mail_view.clear()
                    self.update_mail_stats()
    
    def retranslate_ui(self):
        """Обновить переводы интерфейса почты"""
        self.back_button.setText(translation.t("email.back_to_surveillance"))
        self.mail_list_label.setText(translation.t("email.inbox_messages"))
        self.mail_view_label.setText(translation.t("email.view_message"))
        self.read_button.setText(translation.t("email.mark_as_read"))
        self.delete_button.setText(translation.t("email.delete"))
        
        # Обновляем статистику
        self.update_mail_stats()
        
        # Перезагружаем письма для обновления переводов
        self.load_emails()


class OfficeView(QWidget):
    """Виджет офиса с анимацией"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 220)
        
        self.people = [
            {"x": 50, "y": 30, "color": QColor(255, 100, 100), "typing": True, "name": translation.t("office.ivan"), "status": translation.t("office.status_working")},
            {"x": 160, "y": 80, "color": QColor(100, 200, 255), "typing": False, "name": translation.t("office.maria"), "status": translation.t("office.status_meeting")},
            {"x": 90, "y": 150, "color": QColor(180, 180, 100), "typing": True, "name": translation.t("office.alexey"), "status": translation.t("office.status_report")},
            {"x": 200, "y": 40, "color": QColor(150, 100, 255), "typing": False, "name": translation.t("office.olga"), "status": translation.t("office.status_break")},
        ]
        
        self.blink_state = 0
        self.scan_line_y = 0
        self.scan_line_speed = 2
        self.static_particles = []
        self.camera_glitch = False
        self.camera_glitch_timer = 0
        
        self.init_effects()
        self.setup_animation()
        
    def init_effects(self):
        """Инициализация эффектов"""
        for _ in range(20):
            self.static_particles.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'size': random.randint(1, 2),
                'alpha': random.randint(20, 60),
                'speed': random.uniform(0.5, 1.0),
                'direction': random.uniform(0, 2 * math.pi),
                'lifetime': random.randint(30, 100)
            })
            
        self.effect_timer = QTimer()
        self.effect_timer.timeout.connect(self.update_camera_effects)
        self.effect_timer.start(50)
        
    def setup_animation(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(500)
        
    def update_animation(self):
        """Обновление анимации"""
        self.blink_state = 1 - self.blink_state
        
        for person in self.people:
            if random.random() < 0.2:
                person["typing"] = not person["typing"]
                
        self.update()
        
    def update_camera_effects(self):
        """Обновление эффектов камеры"""
        self.scan_line_y = (self.scan_line_y + self.scan_line_speed) % (self.height() + 30)
        
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
                    'lifetime': random.randint(30, 100),
                    'alpha': random.randint(20, 60)
                })
        
        if random.random() < 0.02 and not self.camera_glitch:
            self.camera_glitch = True
            self.camera_glitch_timer = random.randint(5, 15)
            
        if self.camera_glitch:
            self.camera_glitch_timer -= 1
            if self.camera_glitch_timer <= 0:
                self.camera_glitch = False
        
        self.update()
        
    def paintEvent(self, event):
        """Отрисовка офиса"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        bg_gradient = QLinearGradient(0, 0, 0, self.height())
        bg_gradient.setColorAt(0, QColor(20, 20, 40))
        bg_gradient.setColorAt(1, QColor(10, 10, 25))
        painter.fillRect(self.rect(), bg_gradient)
        
        painter.setPen(QPen(QColor(40, 40, 80, 100), 1))
        grid_size = 20
        for x in range(0, self.width(), grid_size):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), grid_size):
            painter.drawLine(0, y, self.width(), y)
        
        painter.setBrush(QColor(30, 30, 60, 150))
        painter.setPen(QPen(QColor(100, 100, 200, 200), 1))
        painter.drawRect(15, 15, 80, 50)
        painter.drawRect(205, 15, 80, 50)
        
        window_reflection = QLinearGradient(15, 15, 15, 65)
        window_reflection.setColorAt(0, QColor(100, 100, 200, 50))
        window_reflection.setColorAt(1, QColor(100, 100, 200, 0))
        painter.fillRect(15, 15, 80, 50, window_reflection)
        
        desk_shadow_offset = 3
        for desk in [(35, 65), (165, 65), (105, 135)]:
            painter.setBrush(QColor(0, 0, 0, 100))
            painter.setPen(Qt.NoPen)
            painter.drawRect(desk[0] + desk_shadow_offset, 
                           desk[1] + desk_shadow_offset, 
                           60, 40)
            
            desk_gradient = QLinearGradient(desk[0], desk[1], desk[0], desk[1] + 40)
            desk_gradient.setColorAt(0, QColor(60, 60, 60))
            desk_gradient.setColorAt(1, QColor(40, 40, 40))
            painter.setBrush(desk_gradient)
            painter.setPen(QPen(QColor(80, 80, 80), 1))
            painter.drawRect(desk[0], desk[1], 60, 40)
            
            painter.setPen(QPen(QColor(101, 67, 33, 100), 1))
            for i in range(5):
                y_offset = desk[1] + 10 + i * 5
                painter.drawLine(desk[0] + 5, y_offset, desk[0] + 55, y_offset)
        
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        for person in self.people:
            glow_radius = 12
            glow_gradient = QRadialGradient(
                person["x"] + 7, person["y"] + 7, 
                glow_radius
            )
            glow_gradient.setColorAt(0, QColor(person["color"].red(), 
                                             person["color"].green(), 
                                             person["color"].blue(), 100))
            glow_gradient.setColorAt(1, QColor(person["color"].red(), 
                                             person["color"].green(), 
                                             person["color"].blue(), 0))
            
            painter.setBrush(glow_gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(person["x"] - 5, person["y"] - 5, 
                              glow_radius * 2, glow_radius * 2)
            
            painter.setBrush(person["color"])
            painter.setPen(QPen(QColor(255, 255, 255, 150), 1))
            painter.drawEllipse(person["x"], person["y"], 15, 15)
            
            painter.setPen(QColor(220, 220, 220))
            painter.drawText(person["x"] - 15, person["y"] - 8, person["name"])
            
            status_color = QColor(0, 255, 0) if person["status"] == translation.t("office.status_working") else QColor(255, 165, 0)
            painter.setPen(status_color)
            painter.setFont(QFont("Arial", 7))
            painter.drawText(person["x"] - 10, person["y"] + 30, person["status"])
            
            if person["typing"] and self.blink_state:
                typing_color = QColor(255, 255, 200)
                painter.setBrush(typing_color)
                painter.setPen(Qt.NoPen)
                
                for i in range(3):
                    rect_width = random.randint(10, 20)
                    rect_height = 3
                    rect_x = person["x"] + 10 + i * 25
                    rect_y = person["y"] - 5 + random.randint(0, 3)
                    
                    painter.setOpacity(0.7 - i * 0.2)
                    painter.drawRect(rect_x, rect_y, rect_width, rect_height)
                
                painter.setOpacity(1.0)
        
        self.draw_camera_effects(painter)
        
    def draw_camera_effects(self, painter):
        """Рисование эффектов камеры"""
        painter.setOpacity(0.1)
        for particle in self.static_particles:
            alpha = particle['alpha'] * (particle['lifetime'] / 100.0)
            color = QColor(
                random.randint(200, 255),
                random.randint(0, 100),
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
        
        scan_height = 25
        scan_gradient = QLinearGradient(0, self.scan_line_y, 0, self.scan_line_y + scan_height)
        scan_gradient.setColorAt(0, QColor(255, 0, 0, 0))
        scan_gradient.setColorAt(0.2, QColor(255, 0, 0, 150))
        scan_gradient.setColorAt(0.5, QColor(255, 100, 100, 200))
        scan_gradient.setColorAt(0.8, QColor(255, 0, 0, 150))
        scan_gradient.setColorAt(1, QColor(255, 0, 0, 0))
        
        painter.setOpacity(0.4)
        painter.fillRect(0, self.scan_line_y, self.width(), scan_height, scan_gradient)
        
        if self.camera_glitch:
            painter.save()
            
            offset_x = random.randint(-3, 3)
            offset_y = random.randint(-2, 2)
            painter.translate(offset_x, offset_y)
            
            painter.setCompositionMode(QPainter.CompositionMode_Plus)
            painter.setOpacity(0.2)
            
            painter.translate(1, 0)
            painter.setPen(QPen(QColor(255, 0, 0, 100), 1))
            painter.drawRect(0, 0, self.width(), self.height())
            painter.translate(-1, 0)
            
            painter.translate(-1, 0)
            painter.setPen(QPen(QColor(0, 0, 255, 100), 1))
            painter.drawRect(0, 0, self.width(), self.height())
            painter.translate(1, 0)
            
            for _ in range(random.randint(1, 2)):
                y = random.randint(0, self.height())
                offset = random.randint(-5, 5)
                painter.save()
                painter.translate(offset, 0)
                painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
                painter.drawLine(0, y, self.width(), y)
                painter.restore()
            
            painter.restore()
        
        vignette = QRadialGradient(self.width()/2, self.height()/2, 
                                 max(self.width(), self.height())/1.8)
        vignette.setColorAt(0, QColor(0, 0, 0, 0))
        vignette.setColorAt(0.7, QColor(0, 0, 0, 0))
        vignette.setColorAt(1, QColor(0, 0, 0, 120))
        
        painter.setOpacity(0.4)
        painter.setBrush(vignette)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, self.width(), self.height())
        
        painter.setOpacity(0.3)
        painter.setPen(QPen(QColor(255, 0, 0, 100), 1))
        
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        painter.drawLine(0, center_y, self.width(), center_y)
        painter.drawLine(center_x, 0, center_x, self.height())
        
        painter.drawEllipse(int(center_x - 20), int(center_y - 20), 40, 40)
        
        painter.setOpacity(0.7)
        painter.setPen(QColor(255, 100, 100, 200))
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        
        offset_x = random.randint(-1, 1) if random.random() < 0.3 else 0
        offset_y = random.randint(-1, 1) if random.random() < 0.3 else 0
        
        painter.setPen(QColor(255, 0, 0, 100))
        painter.drawText(10 + offset_x + 1, 25 + offset_y + 1, translation.t("office.surveillance_camera"))
        
        painter.setPen(QColor(255, 100, 100, 220))
        painter.drawText(10 + offset_x, 25 + offset_y, translation.t("office.surveillance_camera"))
        
        status_text = translation.t("office.active") if not self.camera_glitch else translation.t("office.glitch")
        status_color = QColor(0, 255, 0, 200) if not self.camera_glitch else QColor(255, 0, 0, 200)
        
        painter.setPen(status_color)
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        painter.drawText(self.width() - 80, 25, status_text)
        
        painter.setOpacity(1.0)