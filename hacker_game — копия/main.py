# main.py
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import QTimer, Qt
from ui.main_window import MainWindow
from styles import STYLES
from intro import IntroScreen

def test_email_system():
    """Тестирование системы почты"""
    print("=== Тестирование системы почты ===")
    
    from core.game_state import GameState
    
    # Создаем тестовое состояние игры
    game_state = GameState()
    game_state.first_name = "Иван"
    game_state.last_name = "Иванов"
    game_state.player_name = "Иван Иванов"
    game_state.day = 1
    
    print(f"Игрок: {game_state.player_name}")
    print(f"День: {game_state.day}")
    
    # Начинаем смену
    print("\nНачинаем смену...")
    game_state.start_shift()
    
    print(f"Текущая задача: {game_state.current_task}")
    print(f"Прогресс задачи: {game_state.current_task_progress}%")
    print(f"Количество писем: {len(game_state.emails)}")
    print(f"Непрочитанных писем: {game_state.unread_emails}")
    
    # Проверяем наличие письма от МВД
    mvd_email = None
    for email in game_state.emails:
        print(f"\nПисьмо от {email.sender}: {email.subject}")
        print(f"Прочитано: {email.read}, Важное: {email.important}")
        if email.sender == "МВД":
            mvd_email = email
    
    if mvd_email:
        print(f"\nНайдено письмо от МВД с ID: {mvd_email.id}")
        
        # Симулируем открытие почты (30% прогресса)
        print("\nОткрываем почту...")
        game_state.make_task_progress(30)
        print(f"Прогресс после открытия почты: {game_state.current_task_progress}%")
        
        # Симулируем чтение письма от МВД
        print("\nЧитаем письмо от МВД...")
        game_state.mark_email_as_read(mvd_email.id)
        print(f"Письмо прочитано: {mvd_email.read}")
        print(f"Непрочитанных писем после чтения: {game_state.unread_emails}")
        print(f"Прогресс задачи: {game_state.current_task_progress}%")
        print(f"Завершено задач: {game_state.tasks_completed}")
    
    # Добавляем тестовое письмо
    print("\nДобавляем тестовое письмо...")
    new_email_id = game_state.add_new_email(
        sender="Тестовая система",
        subject="Тестовое сообщение",
        content="Это тестовое сообщение для проверки системы.",
        important=False
    )
    print(f"Добавлено письмо с ID: {new_email_id}")
    print(f"Всего писем: {len(game_state.emails)}")
    print(f"Непрочитанных: {game_state.unread_emails}")
    
    # Пробуем сохранить и загрузить
    print("\nСохранение игры...")
    game_state.save(999)  # Сохраняем в специальный слот для теста
    
    print("Загрузка игры...")
    loaded_state = GameState.load(999)
    print(f"Загруженный игрок: {loaded_state.player_name}")
    print(f"Загруженных писем: {len(loaded_state.emails)}")
    
    # Удаляем тестовый файл
    test_file = "saves/slot_999.json"
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\nТестовый файл удален: {test_file}")
    
    print("\n=== Тестирование завершено ===")

def load_styles(app):
    """Загрузка стилей приложения"""
    try:
        app.setStyleSheet(STYLES)
        print("Стили успешно загружены из styles.py")
    except Exception as e:
        print(f"Ошибка загрузки стилей: {e}")
        if os.path.exists("styles.qss"):
            try:
                with open("styles.qss", "r", encoding="utf-8") as f:
                    app.setStyleSheet(f.read())
                    print("Стили загружены из файла styles.qss")
            except Exception as e2:
                print(f"Ошибка загрузки стилей из файла: {e2}")

def load_fonts():
    """Загрузка шрифтов"""
    font_paths = [
        "assets/fonts/SourceCodePro-Regular.ttf",
        "assets/fonts/sourcecodepro-regular.ttf",
        "assets/fonts/SourceCodePro.ttf",
        "assets/fonts/SourceCodePro-Medium.ttf",
        "assets/fonts/SourceCodePro-Bold.ttf",
        "assets/fonts/SourceCodePro-Light.ttf",
    ]
    
    font_loaded = False
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    families = QFontDatabase.applicationFontFamilies(font_id)
                    if families:
                        print(f"Шрифт загружен: {families[0]}")
                        font_loaded = True
            except Exception as e:
                print(f"Ошибка загрузки шрифта {font_path}: {e}")
    
    if not font_loaded:
        print("Шрифт Source Code Pro не найден. Используется стандартный моноширинный шрифт.")

def create_directories():
    """Создание необходимых директорий"""
    directories = [
        "assets/fonts",
        "assets/sounds",
        "assets/icons",
        "saves",
        "core",
        "ui",
        "logs",
        "backups"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Директория создана/проверена: {directory}")

def show_intro_and_main_window(app):
    """Показать интро и затем главное окно"""
    # Создаем главное окно, но пока не показываем
    main_window = MainWindow()
    
    # Создаем интро
    intro = IntroScreen()
    
    def on_intro_finished():
        """Действия после завершения интро"""
        print("Интро завершено, показываем главное окно...")
        intro.close()
        
        # Показываем главное окно
        main_window.show()
        
        # Фокус на главном окне
        main_window.activateWindow()
        main_window.raise_()
        
        # Сохраняем, что интро было показано
        main_window.config["intro_shown"] = True
        main_window.save_config()
    
    # Подключаем сигнал завершения интро
    intro.finished.connect(on_intro_finished)
    
    # Запускаем интро
    intro.start_intro(duration=4000)  # 4 секунды интро
    
    return main_window, intro

def main():
    """Основная функция запуска приложения"""
    # Создаем необходимые директории
    create_directories()
    
    # Запускаем тест системы почты (можно закомментировать для обычного запуска)
    # test_email_system()
    
    # Создаем экземпляр приложения
    app = QApplication(sys.argv)
    app.setApplicationName("Офисный хакер")
    app.setApplicationVersion("0.0.1")
    app.setApplicationDisplayName("Офисный хакер - Panopticum")
    
    # Настраиваем иконку приложения (если есть)
    icon_paths = [
        "assets/icons/app_icon.png",
        "assets/icons/icon.png",
        "assets/icon.png"
    ]
    
    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            try:
                from PySide6.QtGui import QIcon
                app.setWindowIcon(QIcon(icon_path))
                print(f"Иконка приложения загружена: {icon_path}")
                break
            except Exception as e:
                print(f"Ошибка загрузки иконки {icon_path}: {e}")
    
    # Загружаем шрифты
    load_fonts()
    
    # Загружаем стили
    load_styles(app)
    
    # Проверяем конфигурацию для показа интро
    config_path = "config.json"
    show_intro = True
    
    if os.path.exists(config_path):
        try:
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if config.get("intro_shown", False):
                    print("Интро уже было показано, пропускаем...")
                    show_intro = False
        except Exception as e:
            print(f"Ошибка чтения конфигурации: {e}")
    
    if show_intro:
        # Показываем интро, затем главное окно
        main_window, intro = show_intro_and_main_window(app)
    else:
        # Показываем только главное окно
        main_window = MainWindow()
        main_window.show()
    
    # Запускаем основной цикл приложения
    exit_code = app.exec()
    
    # Сохраняем состояние при выходе
    if show_intro:
        try:
            intro.close()
        except:
            pass
    
    print("Приложение завершено.")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()