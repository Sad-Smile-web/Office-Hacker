# main_window.py
import json
import os
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer, Signal, QSize, QRect
from PySide6.QtGui import QKeySequence, QShortcut, QCloseEvent, QAction, QScreen
from PySide6.QtWidgets import (QMainWindow, QStackedWidget, QWidget, QVBoxLayout, 
                               QMessageBox, QMenuBar, QMenu, QStatusBar)

from core.game_state import GameState
from audio_manager import AudioManager
from simple_translation import translation
from ui.menu_widget import MenuWidget
from ui.game_widget import GameWidget
from ui.skills_widget import SkillsWidget
from ui.settings_widget import SettingsWidget
from ui.about_widget import AboutWidget
from ui.help_widget import HelpWidget
from ui.name_input_dialog import NameInputDialog
from ui.cutscene_widget import CutsceneWidget
# ИМПОРТИРУЕМ БРАУЗЕР
from ui.browser.browser_window import BrowserWindow


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    # Сигнал для смены языка
    language_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        
        # Инициализация систем
        self.game_state: Optional[GameState] = None
        self.audio_manager = AudioManager()
        self.config = self.load_config()
        self.cutscene_widget: Optional[CutsceneWidget] = None
        self.browser_windows = []  # ДОБАВЛЯЕМ список открытых браузеров
        
        # Установка языка из конфигурации
        lang = self.config.get("game", {}).get("language", "ru")
        translation.load_translations(lang)
        
        # Настройка окна
        self.setWindowTitle(translation.t("app.title", "SIBERIA-SOFTWARE - СИМУЛЯТОР КИБЕРБЕЗОПАСНОСТИ"))
        
        # Создание интерфейса
        self.setup_ui()
        self.setup_menubar()
        self.setup_shortcuts()
        self.setup_game_timer()
        
        # Применяем настройки графики из конфига
        self.apply_graphics_settings()
        
        # Показываем меню
        self.show_menu_widget()
        
        print(f"[MainWindow] Инициализация завершена. Язык: {lang}")
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной лейаут
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Стек виджетов для переключения экранов
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # Создаем виджеты
        self.menu_widget = MenuWidget()
        self.game_widget = None  # Создадим позже
        self.skills_widget = None  # Будет создан позже
        self.settings_widget = SettingsWidget(config=self.config)
        self.about_widget = AboutWidget()
        self.help_widget = HelpWidget()
        
        # Добавляем виджеты в стек (кроме game_widget и skills_widget - они добавятся позже)
        self.stacked_widget.addWidget(self.menu_widget)
        self.stacked_widget.addWidget(self.settings_widget)
        self.stacked_widget.addWidget(self.about_widget)
        self.stacked_widget.addWidget(self.help_widget)
        
        # Подключаем сигналы меню
        self.menu_widget.new_game_clicked.connect(self.show_name_input_dialog)
        self.menu_widget.load_game_clicked.connect(self.show_load_game_dialog)
        self.menu_widget.settings_clicked.connect(self.on_settings_clicked_from_menu)
        self.menu_widget.about_clicked.connect(self.on_about_clicked_from_menu)
        self.menu_widget.help_clicked.connect(self.on_help_clicked_from_menu)
        self.menu_widget.exit_clicked.connect(self.close)
        
        # Подключаем сигналы настроек
        self.settings_widget.back_clicked.connect(self.show_menu_widget)
        self.settings_widget.language_changed.connect(self.on_language_changed)
        self.settings_widget.settings_changed.connect(self.on_settings_changed)
        
        # Подключаем сигналы about и help
        self.about_widget.back_clicked.connect(self.show_menu_widget)
        self.help_widget.back_clicked.connect(self.show_menu_widget)
        
        # Статус бар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(translation.t("app.ready", "Готов"))
        
        print("[MainWindow] UI настроен")
    
    def setup_menubar(self):
        """Настройка меню бар - упрощенная версия"""
        menubar = self.menuBar()
        
        # Скрываем меню-бар полностью, чтобы не было кнопок в углу
        menubar.setVisible(False)
        
        # ИЛИ стилизуем меню-бар, чтобы он не выглядел как кнопки
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: transparent;
                color: #00ff00;
                font-size: 12px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: rgba(0, 100, 0, 0.5);
            }
        """)
        
        # Если хотим оставить меню, создаем его
        file_menu = menubar.addMenu("Файл")
        
        new_game_action = QAction("Новая игра", self)
        new_game_action.setShortcut(QKeySequence.New)
        new_game_action.triggered.connect(self.show_name_input_dialog)
        file_menu.addAction(new_game_action)
        
        load_game_action = QAction("Загрузить игру", self)
        load_game_action.setShortcut(QKeySequence.Open)
        load_game_action.triggered.connect(self.show_load_game_dialog)
        file_menu.addAction(load_game_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Выход", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    def setup_shortcuts(self):
        """Настройка горячих клавиш"""
        # Переключение времени Ctrl+T
        time_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        time_shortcut.activated.connect(self.toggle_game_time)
        
        # Пауза игры P
        pause_shortcut = QShortcut(QKeySequence("P"), self)
        pause_shortcut.activated.connect(self.toggle_game_pause)
        
        # Быстрое сохранение F5
        quick_save_shortcut = QShortcut(QKeySequence("F5"), self)
        quick_save_shortcut.activated.connect(lambda: self.save_game(0))
        
        # Быстрая загрузка F9
        quick_load_shortcut = QShortcut(QKeySequence("F9"), self)
        quick_load_shortcut.activated.connect(lambda: self.load_game(0))
        
        # Переключение полноэкранного режима F11
        fullscreen_shortcut = QShortcut(QKeySequence("F11"), self)
        fullscreen_shortcut.activated.connect(self.toggle_fullscreen)
        
        # Выход из игры Esc (только в игровом режиме)
        self.escape_shortcut = QShortcut(QKeySequence("Escape"), self)
        self.escape_shortcut.activated.connect(self.handle_escape)
    
    def setup_game_timer(self):
        """Настройка таймера игрового времени"""
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.update_game_time)
        
        # Начальное состояние - остановлено
        self.game_time_paused = True
        self.game_timer_interval = 1000  # 1 секунда
        
        # Загружаем настройки времени из конфига
        time_config = self.config.get("game_time", {})
        time_speed = time_config.get("time_speed", 1.0)
        self.set_game_time_speed(time_speed)
    
    def apply_graphics_settings(self):
        """Применить графические настройки из конфига"""
        graphics = self.config.get("graphics", {})
        
        # Разрешение
        width = graphics.get("window_width", 1400)
        height = graphics.get("window_height", 800)
        
        # Режим отображения
        display_mode = graphics.get("display_mode", "windowed")
        
        print(f"[MainWindow] Применяю графические настройки: {display_mode} {width}x{height}")
        
        if display_mode == "fullscreen":
            # Полноэкранный режим
            self.showFullScreen()
        elif display_mode == "windowed":
            # Оконный режим
            self.showNormal()
            self.resize(width, height)
            self.center_window()
            # Убираем флаг безрамки если был
            self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
            self.show()
        elif display_mode == "borderless":
            # Безрамочный режим
            self.showNormal()
            self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
            self.resize(width, height)
            self.center_window()
            self.show()
        
        # VSync настройка
        vsync = graphics.get("vsync", False)
        # Здесь можно применить VSync если используется OpenGL
        print(f"[MainWindow] VSync: {vsync}")
    
    def center_window(self):
        """Центрировать окно на экране"""
        # Получаем геометрию основного экрана
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        screen_width = screen.width()
        screen_height = screen.height()
        
        # Получаем размеры окна
        window_width = self.width()
        window_height = self.height()
        
        # Вычисляем позицию для центрирования
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Устанавливаем позицию
        self.move(x, y)
    
    def on_settings_clicked_from_menu(self):
        """Обработчик нажатия кнопки настроек из меню"""
        print("[MainWindow] Кнопка 'Настройки' нажата из меню")
        self.show_settings_widget()
    
    def on_about_clicked_from_menu(self):
        """Обработчик нажатия кнопки 'О программе' из меню"""
        print("[MainWindow] Кнопка 'О программе' нажата из меню")
        self.show_about_widget()
    
    def on_help_clicked_from_menu(self):
        """Обработчик нажатия кнопки 'Помощь' из меню"""
        print("[MainWindow] Кнопка 'Помощь' нажата из меню")
        self.show_help_widget()
    
    def on_settings_changed(self, new_config):
        """Обработчик изменения настроек"""
        print("[MainWindow] Получены новые настройки")
        
        # Обновляем конфиг
        self.config = new_config
        
        # Применяем настройки
        self.apply_settings()
        
        # Сохраняем конфиг в файл
        self.save_config()
    
    def apply_settings(self):
        """Применить все настройки"""
        print("[MainWindow] Применяю настройки...")
        
        # Применяем графические настройки
        self.apply_graphics_settings()
        
        # Применяем настройки звука
        self.apply_audio_settings()
        
        # Применяем настройки времени
        self.apply_time_settings()
        
        # Обновляем все виджеты если нужно
        self.update_all_widgets()
        
        print("[MainWindow] Настройки применены")
    
    def apply_audio_settings(self):
        """Применить аудио настройки"""
        audio_config = self.config.get("audio", {})
        
        if hasattr(self, 'audio_manager') and self.audio_manager:
            # Обновляем настройки в AudioManager
            self.audio_manager.update_settings(audio_config)
            print("[MainWindow] Аудио настройки применены")
    
    def apply_time_settings(self):
        """Применить настройки времени"""
        time_config = self.config.get("game_time", {})
        
        # Устанавливаем скорость времени
        time_speed = time_config.get("time_speed", 1.0)
        self.set_game_time_speed(time_speed)
        
        print(f"[MainWindow] Настройки времени применены: скорость {time_speed}x")
    
    def show_name_input_dialog(self):
        """Показать диалог ввода имени для новой игры"""
        print("[MainWindow] Показываю диалог ввода имени")
        dialog = NameInputDialog(self)
        
        # Обработчик успешного ввода имени
        def on_names_accepted(first_name, last_name):
            print(f"[MainWindow] Получены данные: {first_name} {last_name}")
            # Начинаем новую игру с кат-сценой
            self.start_new_game_with_cutscene(first_name, last_name)
        
        # Обработчик отмены
        def on_rejected():
            print("[MainWindow] Регистрация отменена")
        
        # ИСПРАВЛЕНИЕ: подключаемся к правильному сигналу names_accepted
        dialog.names_accepted.connect(on_names_accepted)
        dialog.rejected.connect(on_rejected)
        
        dialog.exec()
    
    def start_new_game_with_cutscene(self, first_name, last_name):
        """Начать новую игру с кат-сценой"""
        try:
            print(f"[MainWindow] Создаю новую игру для: {first_name} {last_name}")
            
            # Создаем новое состояние игры
            self.game_state = GameState()
            # ИСПРАВЛЕНО: устанавливаем имя напрямую в GameState
            self.game_state.first_name = first_name
            self.game_state.last_name = last_name
        
            # Сохраняем начальное состояние
            self.game_state.save()
        
            # Создаем и показываем кат-сцену
            self.show_cutscene()
        
        except Exception as e:
            print(f"Ошибка при создании новой игры: {e}")
            import traceback
            traceback.print_exc()
            
            # Показать сообщение об ошибке
            QMessageBox.critical(
                self,
                translation.t("error.title", "Ошибка"),
                translation.t("error.new_game_failed", "Не удалось создать новую игру: {error}").format(error=str(e))
            )
    
    def show_cutscene(self):
        """Показать кат-сцену"""
        print("[MainWindow] Показываю кат-сцену")
        
        if not self.game_state:
            print("[MainWindow] Ошибка: нет состояния игры для кат-сцены")
            return
        
        # ИСПРАВЛЕНО: получаем имя напрямую из GameState
        player_name = f"{self.game_state.first_name} {self.game_state.last_name}"
    
        # Создаем виджет кат-сцены с именем игрока
        self.cutscene_widget = CutsceneWidget(self, player_name)
    
        # Получаем части кат-сцены из переводов
        parts = [
            translation.t("cutscene.part1", ""),
            translation.t("cutscene.part2", ""),
            translation.t("cutscene.part3", "")
        ]
    
        # Получаем финальную фразу
        final_phrase = translation.t("cutscene.final_phrase", "НАЧАЛО РАБОТЫ")
    
        # Устанавливаем данные кат-сцены
        self.cutscene_widget.set_cutscene_data(parts, final_phrase)
    
        # Добавляем в стек
        self.stacked_widget.addWidget(self.cutscene_widget)
        self.stacked_widget.setCurrentWidget(self.cutscene_widget)
        
        # Подключаем сигнал завершения кат-сцены
        self.cutscene_widget.finished.connect(self.on_cutscene_finished)
        
        print("[MainWindow] Кат-сцена запущена")
    
    def on_cutscene_finished(self):
        """Когда кат-сцена завершена"""
        print("[MainWindow] Кат-сцена завершена")
        
        # Удаляем виджет кат-сцены
        if self.cutscene_widget:
            self.stacked_widget.removeWidget(self.cutscene_widget)
            self.cutscene_widget.deleteLater()
            self.cutscene_widget = None
        
        # Сохраняем, что кат-сцена была показана
        if self.game_state:
            self.game_state.cutscene_shown = True
            self.game_state.save()
        
        # Начинаем смену в игре
        if self.game_state:
            self.game_state.start_shift()
            print(f"[MainWindow] Начинается смена для {self.game_state.player_name}")
        
        # Показываем игровой интерфейс
        self.show_game_widget()
        # Обновляем игровой интерфейс после кат-сцены
        self.update_game_interface()
    
    def show_load_game_dialog(self):
        """Показать диалог загрузки игры"""
        print("[MainWindow] Показываю диалог загрузки")
        # Проверяем наличие сохранений
        save_dir = Path("saves")
        if not save_dir.exists():
            QMessageBox.information(
                self,
                translation.t("load.no_saves_title", "Нет сохранений"),
                translation.t("load.no_saves", "Сохранения не найдены. Начните новую игру.")
            )
            return
        
        # Создаем диалог выбора слота
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle(translation.t("load.title", "Загрузить игру"))
        dialog.setFixedSize(300, 200)
        
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel(translation.t("load.select_slot", "Выберите слот для загрузки:")))
        
        # Кнопки для слотов 0-3
        for slot in range(4):
            save_path = save_dir / f"slot_{slot}.json"
            if save_path.exists():
                try:
                    with open(save_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
                        if name:
                            btn_text = translation.t("load.slot_with_name", "Слот {slot}: {name}").format(slot=slot, name=name)
                        else:
                            btn_text = translation.t("load.slot", "Слот {slot}").format(slot=slot)
                except:
                    btn_text = translation.t("load.slot_corrupted", "Слот {slot} (поврежден)").format(slot=slot)
            else:
                btn_text = translation.t("load.slot_empty", "Слот {slot} (пусто)").format(slot=slot)
            
            btn = QPushButton(btn_text)
            btn.setEnabled(save_path.exists())
            btn.clicked.connect(lambda checked, s=slot: self.load_game_and_close(dialog, s))
            layout.addWidget(btn)
        
        # Кнопка отмены
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.exec()
    
    def load_game_and_close(self, dialog, slot):
        """Загрузить игру и закрыть диалог"""
        dialog.accept()
        self.load_game(slot)
    
    def load_game(self, slot=0):
        """Загрузить игру из указанного слота"""
        try:
            # Останавливаем текущий игровой таймер
            if hasattr(self, 'game_timer') and self.game_timer.isActive():
                self.game_timer.stop()
            
            # Загружаем сохранение
            self.game_state = GameState.load(slot)
            
            # Показываем игровой виджет
            self.show_game_widget()
            
            # Запускаем игровой таймер заново
            self.start_game_timer()
            
            # Обновляем игровой интерфейс после загрузки
            self.update_game_interface()
            
            self.status_bar.showMessage(
                translation.t("game.loaded", "Игра загружена из слота {slot}").format(slot=slot),
                3000
            )
            
            print(f"[MainWindow] Игра загружена из слота {slot}")
            
        except Exception as e:
            print(f"[MainWindow] Ошибка загрузки игры: {e}")
            QMessageBox.critical(
                self,
                translation.t("error.title", "Ошибка"),
                translation.t("error.load_failed", "Не удалось загрузить игру: {error}").format(error=str(e))
            )
    
    def start_game_timer(self):
        """Запустить игровой таймер"""
        if not self.game_time_paused and self.game_state:
            self.game_timer.start(self.game_timer_interval)
    
    def save_game(self, slot=None):
        """Сохранить игру"""
        if not self.game_state:
            self.status_bar.showMessage(translation.t("game.no_game_to_save", "Нет активной игры для сохранения"), 3000)
            return
        
        try:
            # Используем save_slot из GameState или 0 по умолчанию
            slot_to_save = slot if slot is not None else getattr(self.game_state, 'save_slot', 0)
            
            # Сохраняем игру
            self.game_state.save(slot_to_save)
            
            # Обновляем save_slot в GameState
            if slot is not None:
                self.game_state.save_slot = slot
            
            self.status_bar.showMessage(
                translation.t("game.saved", "Игра сохранена в слот {slot}").format(slot=slot_to_save),
                3000
            )
            
            print(f"[MainWindow] Игра сохранена в слот {slot_to_save}")
            
        except Exception as e:
            print(f"[MainWindow] Ошибка сохранения игры: {e}")
            QMessageBox.critical(
                self,
                translation.t("error.title", "Ошибка"),
                translation.t("error.save_failed", "Не удалось сохранить игру: {error}").format(error=str(e))
            )
    
    def save_game_as(self):
        """Сохранить игру как..."""
        if not self.game_state:
            return
        
        # Создаем диалог выбора слота
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle(translation.t("save.title", "Сохранить игру"))
        dialog.setFixedSize(300, 200)
        
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel(translation.t("save.select_slot", "Выберите слот для сохранения:")))
        
        # Кнопки для слотов 0-3
        for slot in range(4):
            save_path = Path("saves") / f"slot_{slot}.json"
            if save_path.exists():
                try:
                    with open(save_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
                        if name:
                            btn_text = translation.t("save.overwrite_slot", "Слот {slot}: {name} (перезаписать)").format(slot=slot, name=name)
                        else:
                            btn_text = translation.t("save.overwrite", "Слот {slot} (перезаписать)").format(slot=slot)
                except:
                    btn_text = translation.t("save.slot", "Слот {slot}").format(slot=slot)
            else:
                btn_text = translation.t("save.slot_empty", "Слот {slot} (пусто)").format(slot=slot)
            
            btn = QPushButton(btn_text)
            btn.clicked.connect(lambda checked, s=slot: self.save_game_and_close(dialog, s))
            layout.addWidget(btn)
        
        # Кнопка отмены
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.exec()
    
    def save_game_and_close(self, dialog, slot):
        """Сохранить игру в слот и закрыть диалог"""
        dialog.accept()
        self.save_game(slot)
    
    def show_menu_widget(self):
        """Показать главное меню"""
        print("[MainWindow] Показываю меню")
        
        # Сохраняем игру перед переходом в меню, если есть активная игра
        if self.game_state and self.stacked_widget.currentWidget() == self.game_widget:
            self.save_game()
            print("[MainWindow] Игра сохранена перед выходом в меню")
        
        self.stacked_widget.setCurrentWidget(self.menu_widget)
        
        # Пауза игрового времени, если включена опция
        if self.config.get("game_time", {}).get("auto_pause_in_menus", False):
            self.pause_game_time()
        
        self.status_bar.showMessage(translation.t("app.in_menu", "В главном меню"))
    
    def show_game_widget(self):
        """Показать игровой интерфейс"""
        print("[MainWindow] Показываю игровой интерфейс")
        
        # Создаем игровой виджет, если его нет
        if self.game_widget is None:
            print("[MainWindow] Создаю новый GameWidget")
            self.game_widget = GameWidget(self.game_state, self)
            self.game_widget.back_to_menu.connect(self.show_menu_widget)
            
            # Подключаем сигнал для открытия навыков
            if hasattr(self.game_widget, 'open_skills_requested'):
                print("[MainWindow] Подключаю сигнал open_skills_requested")
                self.game_widget.open_skills_requested.connect(self.show_skills_widget)
            
            # ДОБАВЛЯЕМ: Подключаем сигнал для открытия браузера
            if hasattr(self.game_widget, 'open_browser_requested'):
                print("[MainWindow] Подключаю сигнал open_browser_requested")
                self.game_widget.open_browser_requested.connect(self.open_browser)
            
            self.stacked_widget.addWidget(self.game_widget)
            print("[MainWindow] Создан новый игровой виджет")
        else:
            # Обновляем состояние в существующем виджете
            if self.game_state:
                self.game_widget.update_game_state(self.game_state)
                print(f"[MainWindow] Обновлено состояние игры для {self.game_state.player_name}")
        
        # Показываем игровой виджет
        self.stacked_widget.setCurrentWidget(self.game_widget)
        
        # Обновляем игровой интерфейс
        self.update_game_interface()
        
        # Возобновляем игровое время
        self.resume_game_time()
        
        self.status_bar.showMessage(translation.t("app.in_game", "В игре"))
    
    def show_skills_widget(self):
        """Показать виджет навыков"""
        print("[MainWindow] ПОЛУЧЕН СИГНАЛ: показываю виджет навыков")
        print(f"[MainWindow] game_state существует: {self.game_state is not None}")
        
        if self.game_state is None:
            print("[MainWindow] ОШИБКА: game_state равен None!") 
            return
        
        # Создаем виджет навыков, если его нет
        if self.skills_widget is None:
            print("[MainWindow] Создаю новый SkillsWidget")
            try:
                self.skills_widget = SkillsWidget(self.game_state, self)
                self.skills_widget.back_to_game.connect(self.show_game_widget)
                self.stacked_widget.addWidget(self.skills_widget)
                print("[MainWindow] Создан новый виджет навыков")
            except Exception as e:
                print(f"[MainWindow] ОШИБКА при создании SkillsWidget: {e}")
                import traceback
                traceback.print_exc()
                return
        else:
            print("[MainWindow] Обновляю существующий виджет навыков")
            # Обновляем состояние навыков
            try:
                self.skills_widget.set_game_state(self.game_state)
            except Exception as e:
                print(f"[MainWindow] ОШИБКА при обновлении SkillsWidget: {e}")
        
        # Показываем виджет навыков
        self.stacked_widget.setCurrentWidget(self.skills_widget)
        print(f"[MainWindow] Текущий виджет установлен на skills_widget")
        
        # Пауза игрового времени при просмотре навыков
        if self.config.get("game_time", {}).get("auto_pause_in_menus", False):
            self.pause_game_time()
        
        self.status_bar.showMessage(translation.t("app.viewing_skills", "Просмотр навыков"))
    
    def show_settings_widget(self):
        """Показать настройки"""
        print("[MainWindow] Показываю настройки")
        
        # Обновляем конфиг в виджете настроек
        self.settings_widget.config = self.config
        self.settings_widget.load_ui_from_config()
        
        self.stacked_widget.setCurrentWidget(self.settings_widget)
        self.status_bar.showMessage(translation.t("app.in_settings", "В настройках"))
    
    def show_audio_settings(self):
        """Показать настройки звука"""
        self.show_settings_widget()
        if hasattr(self.settings_widget, 'show_audio_tab'):
            self.settings_widget.show_audio_tab()
    
    def show_about_widget(self):
        """Показать информацию о программе"""
        print("[MainWindow] Показываю 'О программе'")
        self.stacked_widget.setCurrentWidget(self.about_widget)
        self.status_bar.showMessage(translation.t("app.about", "О программе"))
    
    def show_help_widget(self):
        """Показать помощь"""
        print("[MainWindow] Показываю помощь")
        self.stacked_widget.setCurrentWidget(self.help_widget)
        self.status_bar.showMessage(translation.t("app.help", "Помощь"))
    
    # ДОБАВЛЯЕМ НОВЫЙ МЕТОД ДЛЯ ОТКРЫТИЯ БРАУЗЕРА
    def open_browser(self, url: str):
        """Открыть браузер с указанным URL"""
        print(f"[MainWindow] Открываю браузер для URL: {url}")
        
        try:
            # Создаем новое окно браузера
            browser = BrowserWindow(self, url)
            
            # Настраиваем окно браузера
            browser.setWindowModality(Qt.WindowModality.NonModal)  # Не модальное
            browser.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            
            # Подключаем сигнал закрытия для удаления из списка
            browser.destroyed.connect(lambda: self.on_browser_closed(browser))
            
            # Добавляем в список открытых браузеров
            self.browser_windows.append(browser)
            
            # Показываем браузер
            browser.show()
            
            # Центрируем окно браузера относительно главного окна
            self.center_browser_window(browser)
            
            print(f"[MainWindow] Браузер открыт для {url}")
            
        except Exception as e:
            print(f"[MainWindow] Ошибка при открытии браузера: {e}")
            import traceback
            traceback.print_exc()
            
            QMessageBox.critical(
                self,
                translation.t("browser.error.title", "Ошибка браузера"),
                translation.t("browser.error.load_failed", "Ошибка загрузки страницы: {error}").format(error=str(e))
            )
    
    def center_browser_window(self, browser_window):
        """Центрировать окно браузера относительно главного окна"""
        # Получаем геометрию главного окна
        main_geometry = self.geometry()
        main_center = main_geometry.center()
        
        # Получаем размеры окна браузера
        browser_size = browser_window.size()
        
        # Вычисляем позицию для центрирования
        x = main_center.x() - browser_size.width() // 2
        y = main_center.y() - browser_size.height() // 2
        
        # Устанавливаем позицию с небольшим смещением
        browser_window.move(x + 50, y + 50)
    
    def on_browser_closed(self, browser):
        """Обработчик закрытия окна браузера"""
        try:
            if browser in self.browser_windows:
                self.browser_windows.remove(browser)
                print("[MainWindow] Браузер закрыт и удален из списка")
        except:
            pass
    
    def close_all_browsers(self):
        """Закрыть все открытые браузеры"""
        for browser in self.browser_windows[:]:  # Используем копию списка
            try:
                browser.close()
                browser.deleteLater()
            except:
                pass
        self.browser_windows.clear()
        print("[MainWindow] Все браузеры закрыты")
    
    def change_language(self, lang_code):
        """Сменить язык интерфейса"""
        # Загружаем новый язык
        translation.load_translations(lang_code)
        
        # Обновляем конфигурацию
        if "game" not in self.config:
            self.config["game"] = {}
        self.config["game"]["language"] = lang_code
        self.save_config()
        
        # Обновляем заголовок окна
        self.setWindowTitle(translation.t("app.title", "SIBERIA-SOFTWARE - СИМУЛЯТОР КИБЕРБЕЗОПАСНОСТИ"))
        
        # Обновляем все виджеты
        self.update_all_widgets()
        
        # Отправляем сигнал о смене языка
        self.language_changed.emit(lang_code)
        
        self.status_bar.showMessage(
            translation.t("app.language_changed", "Язык изменен на {lang}").format(
                lang="Русский" if lang_code == "ru" else "English"
            ),
            3000
        )
        
        print(f"[MainWindow] Язык изменен на {lang_code}")
    
    def on_language_changed(self, lang_code):
        """Обработчик смены языка из настроек"""
        self.change_language(lang_code)
    
    def update_all_widgets(self):
        """Обновить все виджеты при смене языка"""
        # Обновляем меню
        if hasattr(self, 'menu_widget') and self.menu_widget:
            if hasattr(self.menu_widget, 'retranslate_ui'):
                self.menu_widget.retranslate_ui()
        
        # Обновляем игровой виджет
        if hasattr(self, 'game_widget') and self.game_widget:
            if hasattr(self.game_widget, 'retranslate_ui'):
                self.game_widget.retranslate_ui()
        
        # Обновляем виджет навыков
        if hasattr(self, 'skills_widget') and self.skills_widget:
            if hasattr(self.skills_widget, 'update_translations'):
                self.skills_widget.update_translations()
        
        # Обновляем настройки
        if hasattr(self, 'settings_widget') and self.settings_widget:
            if hasattr(self.settings_widget, 'retranslate_ui'):
                self.settings_widget.retranslate_ui()
        
        # Обновляем about
        if hasattr(self, 'about_widget') and self.about_widget:
            if hasattr(self.about_widget, 'retranslate_ui'):
                self.about_widget.retranslate_ui()
        
        # Обновляем help
        if hasattr(self, 'help_widget') and self.help_widget:
            if hasattr(self.help_widget, 'retranslate_ui'):
                self.help_widget.retranslate_ui()
        
        # Обновляем меню бар
        self.setup_menubar()
    
    def update_game_time(self):
        """Обновить игровое время"""
        if self.game_state and not self.game_time_paused:
            # Обновляем время в состоянии игры
            self.game_state.update_time()
            
            # Обновляем виджет времени, если он существует
            if self.game_widget and hasattr(self.game_widget, 'time_widget'):
                self.game_widget.time_widget.update_display()
            
            # Проверяем конец рабочего дня
            if hasattr(self.game_state, 'is_workday_over') and self.game_state.is_workday_over():
                self.end_workday()
    
    def set_game_time_speed(self, speed):
        """Установить скорость игрового времени"""
        # Преобразуем скорость в интервал таймера
        if speed <= 0:
            speed = 0.1  # Минимальная скорость
        
        # Вычисляем интервал таймера (в миллисекундах)
        self.game_timer_interval = int(1000 / speed)
        
        # Обновляем таймер, если он запущен
        if self.game_timer.isActive():
            self.game_timer.setInterval(self.game_timer_interval)
        
        # Сохраняем настройку в конфиг
        if "game_time" not in self.config:
            self.config["game_time"] = {}
        self.config["game_time"]["time_speed"] = speed
        self.save_config()
    
    def toggle_game_time(self):
        """Переключить паузу игрового времени"""
        if self.game_time_paused:
            self.resume_game_time()
        else:
            self.pause_game_time()
    
    def pause_game_time(self):
        """Приостановить игровое время"""
        if self.game_timer.isActive():
            self.game_timer.stop()
            self.game_time_paused = True
            self.status_bar.showMessage(translation.t("game.time_paused", "Время приостановлено"), 2000)
        
        # Также пауза в состоянии игры
        if self.game_state:
            self.game_state.pause_game_time()
    
    def resume_game_time(self):
        """Возобновить игровое время"""
        if not self.game_timer.isActive() and self.game_state:
            self.game_timer.start(self.game_timer_interval)
            self.game_time_paused = False
            self.status_bar.showMessage(translation.t("game.time_resumed", "Время возобновлено"), 2000)
        
        # Также возобновление в состоянии игры
        if self.game_state:
            self.game_state.resume_game_time()
    
    def toggle_game_pause(self):
        """Переключить паузу игры"""
        self.toggle_game_time()
    
    def end_workday(self):
        """Завершить рабочий день"""
        if not self.game_state:
            return
        
        # Сохраняем игру
        self.save_game()
        
        # Показываем сообщение о завершении дня
        self.status_bar.showMessage(translation.t("game.workday_over", "Рабочий день завершен"), 5000)
        
        print("[MainWindow] Рабочий день завершен")
    
    def toggle_fullscreen(self):
        """Переключить полноэкранный режим"""
        if self.isFullScreen():
            # Выход из полноэкранного режима
            self.showNormal()
            
            # Обновляем конфиг
            self.config["graphics"]["display_mode"] = "windowed"
            self.save_config()
            
            self.status_bar.showMessage(translation.t("app.fullscreen_off", "Полноэкранный режим выключен"), 2000)
        else:
            # Вход в полноэкранный режим
            self.showFullScreen()
            
            # Обновляем конфиг
            self.config["graphics"]["display_mode"] = "fullscreen"
            self.save_config()
            
            self.status_bar.showMessage(translation.t("app.fullscreen_on", "Полноэкранный режим включен"), 2000)
    
    def handle_escape(self):
        """Обработка клавиши Escape"""
        current_widget = self.stacked_widget.currentWidget()
        
        if current_widget == self.game_widget:
            # В игровом режиме - спросить о выходе в меню
            self.show_menu_widget()
        elif current_widget == self.skills_widget:
            # В режиме навыков - вернуться в игру
            self.show_game_widget()
        elif current_widget in [self.settings_widget, self.about_widget, self.help_widget]:
            # В других режимах - вернуться в меню
            self.show_menu_widget()
    
    def load_config(self):
        """Загрузить конфигурацию из файла"""
        config_path = Path("config.json")
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[MainWindow] Ошибка загрузки конфигурации: {e}")
                return self.get_default_config()
        else:
            return self.get_default_config()
    
    def get_default_config(self):
        """Получить конфигурацию по умолчанию"""
        return {
            "game": {
                "difficulty": 2,
                "autosave_interval": 300,
                "enable_tutorial": True,
                "language": "ru"
            },
            "graphics": {
                "enable_effects": True,
                "glitch_effects": False,
                "window_width": 1400,
                "window_height": 800,
                "display_mode": "windowed",
                "vsync": False,
                "effect_intensity": 50
            },
            "audio": {
                "enabled": True,
                "volume": 80,
                "master_volume": 80,
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
                "real_time_seconds_per_game_minute": 1,
                "auto_pause_in_menus": True,
                "show_time_widget": True,
                "start_year": 2140
            },
            "intro_shown": False
        }
    
    def save_config(self):
        """Сохранить конфигурацию в файл"""
        try:
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print("[MainWindow] Конфигурация сохранена")
        except Exception as e:
            print(f"[MainWindow] Ошибка сохранения конфигурации: {e}")
    
    # ДОБАВЛЯЕМ НОВЫЙ МЕТОД ДЛЯ ОБНОВЛЕНИЯ ИГРОВОГО ИНТЕРФЕЙСА
    def update_game_interface(self):
        """Обновить игровой интерфейс"""
        if hasattr(self, 'game_widget') and self.game_widget:
            # Обновляем весь интерфейс игры
            self.game_widget.update_ui()
            
            # Если есть терминал, обновляем его тоже
            if hasattr(self.game_widget, 'terminal'):
                # Можете добавить сообщение о завершении задачи
                # Например: self.game_widget.terminal.add_message("Задача завершена")
                pass
    
    def closeEvent(self, event: QCloseEvent):
        """Обработчик закрытия окна"""
        # Закрываем все браузеры
        self.close_all_browsers()
        
        # Сохраняем состояние окна в конфигурацию (только если не в полноэкранном режиме)
        if not self.isFullScreen():
            self.config["graphics"]["window_width"] = self.width()
            self.config["graphics"]["window_height"] = self.height()
        
        # Сохраняем конфигурация
        self.save_config()
        
        # Сохраняем игру, если есть активная
        if self.game_state:
            try:
                self.save_game()
            except:
                pass
        
        # Останавливаем таймеры
        if hasattr(self, 'game_timer'):
            self.game_timer.stop()
        
        print("[MainWindow] Приложение завершает работу")
        event.accept()