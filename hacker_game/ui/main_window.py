# ui/main_window.py

import sys
import json
import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QStackedWidget, QMessageBox, QApplication)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QKeyEvent, QIcon, QFont

# Импортируем наши виджеты
from ui.menu_widget import MenuWidget
from ui.game_widget import GameWidget
from ui.settings_widget import SettingsWidget
from ui.help_widget import HelpWidget
from ui.about_widget import AboutWidget
from ui.name_input_dialog import NameInputDialog  # Новый импорт

# Импортируем игровое состояние
from core.game_state import GameState

# Импортируем ПРОСТУЮ систему переводов
from simple_translation import translation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Загружаем конфигурацию
        self.config = self.load_config()
        
        # Устанавливаем язык из конфига
        self.setup_language()
        
        # Инициализируем игровое состояние
        self.game_state = None
        
        # Настройки окна
        self.setWindowTitle(translation.t("app.title", default="Office Hacker - Cybersecurity Simulator"))
        self.setGeometry(100, 100, 1200, 800)
        
        # Устанавливаем стиль для всего приложения
        self.setup_styles()
        
        # Настройка центрального виджета
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Основной layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Стек для переключения между экранами
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        
        # Инициализация виджетов
        self.init_widgets()
        
        # Настройка таймеров
        self.setup_timers()
        
        # Настройка горячих клавиш
        self.setup_shortcuts()
        
        # Показываем меню при запуске
        self.show_menu()
        
        # Устанавливаем полноэкранный режим если нужно
        self.apply_graphics_settings()
        
        # Применяем настройки аудио
        self.apply_audio_settings()
        
        print(translation.t("app.startup_complete", default="🚀 Главное окно инициализировано"))
    
    def setup_language(self):
        """Настройка языка из конфига"""
        try:
            # Получаем язык из конфига
            language = self.config.get("game", {}).get("language", "ru")
            
            # Устанавливаем язык в менеджере переводов
            translation.set_language(language)
            print(f"🌍 {translation.t('app.language_set', language=language)}")
            
        except Exception as e:
            print(f"❌ {translation.t('error.language_setup')}: {e}")
            translation.set_language("ru")  # По умолчанию русский
    
    def load_config(self):
        """Загрузка конфигурации"""
        default_config = {
            "game": {
                "difficulty": 2,
                "autosave_interval": 300,
                "enable_tutorial": True,
                "language": "ru"
            },
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
            },
            "game_time": {
                "time_speed": 1.0,
                "real_time_seconds_per_game_minute": 10,
                "auto_pause_in_menus": True,
                "show_time_widget": True
            }
        }
        
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                
                # Объединяем с конфигом по умолчанию
                for category in default_config:
                    if category in loaded_config:
                        for key in default_config[category]:
                            if key in loaded_config[category]:
                                default_config[category][key] = loaded_config[category][key]
                
                print(translation.t("config.loaded"))
            else:
                # Создаем новый конфиг
                with open("config.json", "w", encoding="utf-8") as f:
                    json.dump(default_config, f, ensure_ascii=False, indent=2)
                print(translation.t("config.created"))
                
        except Exception as e:
            print(f"❌ {translation.t('error.config_load')}: {e}")
        
        return default_config
    
    def setup_styles(self):
        """Настройка стилей приложения"""
        # Устанавливаем шрифт по умолчанию
        font = QFont("Segoe UI", 9)
        QApplication.instance().setFont(font)
        
        # Общий стиль приложения
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a14;
            }
            
            QMessageBox {
                background-color: #1a1a2e;
                color: #ffffff;
            }
            
            QMessageBox QLabel {
                color: #ffffff;
                font-size: 13px;
            }
            
            QMessageBox QPushButton {
                background-color: #0066aa;
                color: #ffffff;
                border: 1px solid #00bfff;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
                min-height: 30px;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #0088cc;
                border-color: #00ffff;
            }
            
            QMessageBox QPushButton:pressed {
                background-color: #004488;
            }
            
            /* Стили для скроллбаров во всем приложении */
            QScrollBar:vertical {
                background: #222244;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background: #00bfff;
                min-height: 30px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #00ffff;
            }
            
            QScrollBar:horizontal {
                background: #222244;
                height: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:horizontal {
                background: #00bfff;
                min-width: 30px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: #00ffff;
            }
        """)
    
    def init_widgets(self):
        """Инициализация всех виджетов"""
        # Создаем виджеты
        self.menu_widget = MenuWidget(self)
        
        # Создаем остальные виджеты
        self.settings_widget = SettingsWidget(self, self.config)
        self.help_widget = HelpWidget(self)
        self.about_widget = AboutWidget(self)
        self.game_widget = None
        
        # Подключаем сигналы меню
        self.menu_widget.start_game.connect(self.start_new_game)
        self.menu_widget.load_game.connect(self.load_existing_game)
        self.menu_widget.show_settings.connect(self.show_settings)
        self.menu_widget.show_help.connect(self.show_help)
        self.menu_widget.show_about.connect(self.show_about)
        self.menu_widget.exit_game.connect(self.exit_game)
        
        # Подключаем сигналы настроек
        self.settings_widget.settings_changed.connect(self.update_config)
        self.settings_widget.back_to_menu.connect(self.show_menu)
        self.settings_widget.language_changed.connect(self.on_language_changed)
        
        # Подключаем сигналы помощи и "О программе"
        self.help_widget.back_requested.connect(self.show_menu)
        self.about_widget.back_requested.connect(self.show_menu)
        
        # Добавляем все виджеты в стек
        self.stack.addWidget(self.menu_widget)
        self.stack.addWidget(self.settings_widget)
        self.stack.addWidget(self.help_widget)
        self.stack.addWidget(self.about_widget)
        
        print(translation.t("app.widgets_initialized"))
    
    def setup_timers(self):
        """Настройка таймеров"""
        # Таймер автосохранения
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.autosave_game)
        self.autosave_timer.start(300000)  # Каждые 5 минут
        
        # Таймер для обновления статуса
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(60000)  # Каждую минуту
        
        print(translation.t("app.timers_setup"))
    
    def setup_shortcuts(self):
        """Настройка горячих клавиш"""
        # Горячие клавиши будут обрабатываться в keyPressEvent
        print(translation.t("app.shortcuts_setup"))
    
    def keyPressEvent(self, event: QKeyEvent):
        """Обработка нажатий клавиш"""
        key = event.key()
        modifiers = event.modifiers()
        
        # ESC - возврат в меню
        if key == Qt.Key_Escape:
            if self.stack.currentWidget() != self.menu_widget:
                if self.game_widget and self.stack.currentWidget() == self.game_widget:
                    # Спросим подтверждение
                    reply = QMessageBox.question(
                        self,
                        translation.t("game.exit_confirm_title"),
                        translation.t("game.exit_to_menu_confirm"),
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.No
                    )
                    
                    if reply == QMessageBox.Yes:
                        self.show_menu()
                else:
                    self.show_menu()
            event.accept()
            return
        
        # F1 - помощь
        elif key == Qt.Key_F1:
            self.show_help()
            event.accept()
            return
        
        # Ctrl+S - сохранить игру
        elif key == Qt.Key_S and modifiers == Qt.ControlModifier:
            if self.game_state:
                self.save_game()
                self.show_status_message(translation.t("game.saved_successfully"))
            event.accept()
            return
        
        # Ctrl+Q - выход
        elif key == Qt.Key_Q and modifiers == Qt.ControlModifier:
            self.exit_game()
            event.accept()
            return
        
        # Ctrl+T - пауза/возобновление времени
        elif key == Qt.Key_T and modifiers == Qt.ControlModifier:
            if self.game_state:
                if self.game_state.time_paused:
                    self.game_state.resume_game_time()
                    status = translation.t("game.time_resumed")
                else:
                    self.game_state.pause_game_time()
                    status = translation.t("game.time_paused")
                self.show_status_message(status)
            event.accept()
            return
        
        # Ctrl+F - переключение полноэкранного режима
        elif key == Qt.Key_F and modifiers == Qt.ControlModifier:
            self.toggle_fullscreen()
            event.accept()
            return
        
        # Ctrl+M - вкл/выкл звук
        elif key == Qt.Key_M and modifiers == Qt.ControlModifier:
            if "audio" in self.config:
                self.config["audio"]["enabled"] = not self.config["audio"].get("enabled", True)
                status = translation.t("game.audio_disabled") if not self.config["audio"]["enabled"] else translation.t("game.audio_enabled")
                self.show_status_message(status)
                self.apply_audio_settings()
            event.accept()
            return
        
        super().keyPressEvent(event)
    
    def show_status_message(self, message):
        """Показать временное сообщение о статусе"""
        # Временно выводим в консоль
        print(f"💬 {message}")
        
        # Если есть виджет игры, показываем в терминале
        if hasattr(self, 'game_widget') and self.game_widget and self.stack.currentWidget() == self.game_widget:
            if hasattr(self.game_widget.terminal, 'output'):
                self.game_widget.terminal.output.append(f"[{translation.t('game.system')}] {message}")
                self.game_widget.terminal.output.moveCursor(self.game_widget.terminal.output.textCursor().MoveOperation.End)
    
    def update_status(self):
        """Обновление статуса приложения"""
        # Здесь можно обновлять статус в статусбаре
        pass
    
    def start_new_game(self):
        """Начать новую игру"""
        try:
            # Спросим подтверждение если есть незаконченная игра
            if self.game_state:
                reply = QMessageBox.question(
                    self,
                    translation.t("game.new_game_confirm_title"),
                    translation.t("game.new_game_confirm"),
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply != QMessageBox.Yes:
                    return
            
            # Создаем диалог для ввода имени
            dialog = NameInputDialog(self)
            dialog.setModal(True)
            
            # Показываем диалог и ждем результат
            if dialog.exec() == NameInputDialog.Accepted:
                first_name, last_name = dialog.get_names()
                
                # Проверяем, что оба поля заполнены
                if not first_name or not last_name:
                    QMessageBox.warning(
                        self,
                        translation.t("game.input_error_title"),
                        translation.t("game.input_name_required")
                    )
                    return
                
                # Создаем новое игровое состояние с именем
                self.game_state = GameState(
                    first_name=first_name.strip(),
                    last_name=last_name.strip()
                )
                
                # Запускаем новую смену
                self.game_state.start_new_shift()
                
                # Показываем игровой экран
                self.show_game()
                
                # Показываем приветственное сообщение
                self.show_status_message(translation.t("game.new_shift_started"))
                self.show_status_message(translation.t("game.welcome", name=self.game_state.player_name))
                
                print(f"🎮 {translation.t('game.new_game_started_for')} {self.game_state.player_name}")
            else:
                # Пользователь отменил ввод
                print(f"❌ {translation.t('game.user_canceled_new_game')}")
                return
                
        except Exception as e:
            print(f"❌ {translation.t('error.new_game_start')}: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self,
                translation.t("common.error"),
                f"{translation.t('game.new_game_error')}: {str(e)}"
            )
    
    def load_existing_game(self):
        """Загрузить существующую игру"""
        try:
            # Пробуем загрузить сохранение
            loaded_state = GameState.load()
            
            if loaded_state and loaded_state.player_name:
                self.game_state = loaded_state
                self.show_game()
                self.show_status_message(translation.t("game.loaded_successfully"))
                self.show_status_message(translation.t("game.welcome_back", name=self.game_state.player_name))
                print(f"💾 {translation.t('game.loaded_for')} {self.game_state.player_name}")
            else:
                QMessageBox.information(
                    self,
                    translation.t("game.no_save_title"),
                    translation.t("game.no_save_found")
                )
                
        except Exception as e:
            print(f"❌ {translation.t('error.game_load')}: {e}")
            QMessageBox.critical(
                self,
                translation.t("common.error"),
                translation.t("game.load_error")
            )
    
    def save_game(self):
        """Сохранить текущую игру"""
        try:
            if self.game_state:
                self.game_state.save()
                print(translation.t("game.saved_successfully"))
        except Exception as e:
            print(f"❌ {translation.t('error.game_save')}: {e}")
            QMessageBox.critical(
                self,
                translation.t("common.error"),
                translation.t("game.save_error")
            )
    
    def autosave_game(self):
        """Автосохранение игры"""
        if self.game_state and self.config.get("game", {}).get("autosave_interval", 300) > 0:
            try:
                self.game_state.save()
                print("💾 {translation.t('game.autosave_performed')}")
            except:
                pass
    
    def show_game(self):
        """Показать игровой экран"""
        if self.game_state:
            if not self.game_widget:
                # Создаем игровой виджет
                self.game_widget = GameWidget(self.game_state, self)
                self.game_widget.back_to_menu.connect(self.show_menu)
                
                # Добавляем в стек
                self.stack.addWidget(self.game_widget)
            else:
                # Если виджет уже создан, обновляем данные
                if hasattr(self.game_widget, 'update_game_data'):
                    self.game_widget.update_game_data()
                else:
                    # Пересоздаем виджет с новыми данными
                    self.stack.removeWidget(self.game_widget)
                    self.game_widget = GameWidget(self.game_state, self)
                    self.game_widget.back_to_menu.connect(self.show_menu)
                    self.stack.addWidget(self.game_widget)
            
            # Показываем виджет игры
            self.stack.setCurrentWidget(self.game_widget)
            
            # Обновляем заголовок окна
            self.setWindowTitle(f"{translation.t('app.name')} - {translation.t('app.office_hacker')} - {translation.t('game.shift')} {self.game_state.day}")
            
            print(translation.t("game.screen_shown"))
    
    def show_menu(self):
        """Показать главное меню"""
        # Сохраняем игру если нужно
        if self.game_state and self.stack.currentWidget() == self.game_widget:
            self.save_game()
        
        # Обновляем заголовок окна
        self.setWindowTitle(f"{translation.t('app.name')} - {translation.t('app.office_hacker')}")
        
        # Показываем меню
        self.stack.setCurrentWidget(self.menu_widget)
        
        print(translation.t("menu.screen_shown"))
    
    def show_settings(self):
        """Показать настройки"""
        # Показываем настройки
        self.stack.setCurrentWidget(self.settings_widget)
        
        # Обновляем переводы в настройках
        if hasattr(self.settings_widget, 'retranslate_ui'):
            self.settings_widget.retranslate_ui()
        
        print(translation.t("settings.screen_shown"))
    
    def show_help(self):
        """Показать справку"""
        # Показываем помощь
        self.stack.setCurrentWidget(self.help_widget)
        
        print(translation.t("help.screen_shown"))
    
    def show_about(self):
        """Показать информацию о программе"""
        # Показываем информацию
        self.stack.setCurrentWidget(self.about_widget)
        
        print(translation.t("about.screen_shown"))
    
    def exit_game(self):
        """Выйти из игры"""
        # Спросим подтверждение
        reply = QMessageBox.question(
            self,
            translation.t("game.exit_confirm_title"),
            translation.t("game.exit_confirm"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Сохраняем игру если нужно
            if self.game_state:
                self.save_game()
            
            # Сохраняем конфиг
            try:
                with open("config.json", "w", encoding="utf-8") as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=2)
            except:
                pass
            
            # Закрываем приложение
            QApplication.instance().quit()
    
    def update_config(self, new_config):
        """Обновить конфигурация"""
        # Объединяем конфиги
        for category in new_config:
            if category not in self.config:
                self.config[category] = {}
            
            for key in new_config[category]:
                self.config[category][key] = new_config[category][key]
        
        # Сохраняем конфиг
        try:
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(translation.t("config.updated"))
        except Exception as e:
            print(f"❌ {translation.t('error.config_save')}: {e}")
        
        # Применяем настройки графики
        self.apply_graphics_settings()
        
        # Применяем настройки аудио
        self.apply_audio_settings()
    
    def on_language_changed(self, language):
        """Обработчик смены языка"""
        # Устанавливаем новый язык
        translation.set_language(language)
        
        # Сохраняем в конфиг
        if "game" not in self.config:
            self.config["game"] = {}
        self.config["game"]["language"] = language
        
        # Сохраняем конфиг
        try:
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(f"🌍 {translation.t('app.language_changed_to', language=language)}")
        except:
            pass
        
        # Обновляем все открытые виджеты
        self.update_all_widgets()
    
    def update_all_widgets(self):
        """Обновить все виджеты при смене языка"""
        # Обновляем меню если оно открыто
        if hasattr(self.menu_widget, 'retranslate_ui'):
            self.menu_widget.retranslate_ui()
        
        # Обновляем настройки если они открыты
        if hasattr(self.settings_widget, 'retranslate_ui'):
            self.settings_widget.retranslate_ui()
        
        # Обновляем игру если она открыта
        if self.game_widget and hasattr(self.game_widget, 'retranslate_ui'):
            self.game_widget.retranslate_ui()
        
        # Обновляем справку если она открыта
        if hasattr(self.help_widget, 'retranslate_ui'):
            self.help_widget.retranslate_ui()
        
        # Обновляем "О программе" если оно открыто
        if hasattr(self.about_widget, 'retranslate_ui'):
            self.about_widget.retranslate_ui()
        
        # Обновляем заголовок окна
        if self.game_state and self.stack.currentWidget() == self.game_widget:
            self.setWindowTitle(f"{translation.t('app.name')} - {translation.t('app.office_hacker')} - {translation.t('game.shift')} {self.game_state.day}")
        else:
            self.setWindowTitle(f"{translation.t('app.name')} - {translation.t('app.office_hacker')}")
    
    def apply_graphics_settings(self):
        """Применить настройки графики"""
        graphics = self.config.get("graphics", {})
        
        # Устанавливаем размер окна
        width = graphics.get("window_width", 1200)
        height = graphics.get("window_height", 800)
        
        if graphics.get("display_mode") == "fullscreen":
            self.showFullScreen()
        elif graphics.get("display_mode") == "windowed":
            self.showNormal()
            self.resize(width, height)
            self.center_window()
        elif graphics.get("display_mode") == "borderless":
            self.showNormal()
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.show()
            self.resize(width, height)
            self.center_window()
        
        # Включаем/выключаем эффекты в виджетах
        if hasattr(self, 'menu_widget'):
            self.menu_widget.config["graphics"] = graphics
        
        if hasattr(self, 'game_widget') and self.game_widget:
            self.game_widget.config["graphics"] = graphics
        
        print(translation.t("graphics.applied"))
    
    def apply_audio_settings(self):
        """Применить настройки аудио"""
        audio = self.config.get("audio", {})
        
        # Здесь можно управлять звуком через audio_manager
        try:
            from audio_manager import AudioManager
            audio_manager = AudioManager()
            
            # Устанавливаем громкость
            if audio.get("enabled", True):
                master_volume = audio.get("master_volume", 70) / 100.0
                effects_volume = audio.get("effects_volume", 80) / 100.0
                music_volume = audio.get("music_volume", 60) / 100.0
                
                audio_manager.set_master_volume(master_volume)
                audio_manager.set_effects_volume(effects_volume)
                audio_manager.set_music_volume(music_volume)
            else:
                audio_manager.set_master_volume(0)
            
            print(translation.t("audio.applied"))
            
        except Exception as e:
            print(f"❌ {translation.t('error.audio_apply')}: {e}")
    
    def toggle_fullscreen(self):
        """Переключить полноэкранный режим"""
        if self.isFullScreen():
            self.showNormal()
            self.config["graphics"]["display_mode"] = "windowed"
        else:
            self.showFullScreen()
            self.config["graphics"]["display_mode"] = "fullscreen"
        
        # Сохраняем настройки
        self.update_config(self.config)
    
    def center_window(self):
        """Центрировать окно на экране"""
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        # Спросим подтверждение только если игра активна
        if self.game_state and self.stack.currentWidget() == self.game_widget:
            reply = QMessageBox.question(
                self,
                translation.t("game.exit_confirm_title"),
                translation.t("game.exit_confirm"),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Сохраняем игру
                self.save_game()
                # Сохраняем конфиг
                try:
                    with open("config.json", "w", encoding="utf-8") as f:
                        json.dump(self.config, f, ensure_ascii=False, indent=2)
                except:
                    pass
                
                event.accept()
            else:
                event.ignore()
        else:
            # Если игра не активна, просто выходим
            try:
                with open("config.json", "w", encoding="utf-8") as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=2)
            except:
                pass
            event.accept()


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Устанавливаем иконку приложения
    try:
        app_icon = QIcon("icon.png")
        app.setWindowIcon(app_icon)
    except:
        pass
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())