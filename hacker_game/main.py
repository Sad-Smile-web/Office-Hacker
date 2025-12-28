# main.py
import sys
import os
from pathlib import Path

from PySide6.QtGui import QTextCursor

# Исправление для обратной совместимости с PySide6
if not hasattr(QTextCursor, 'End'):
    QTextCursor.End = QTextCursor.MoveOperation.End
    QTextCursor.Start = QTextCursor.MoveOperation.Start
    QTextCursor.Right = QTextCursor.MoveOperation.Right
    QTextCursor.Left = QTextCursor.MoveOperation.Left
    QTextCursor.Up = QTextCursor.MoveOperation.Up
    QTextCursor.Down = QTextCursor.MoveOperation.Down
    QTextCursor.NextWord = QTextCursor.MoveOperation.NextWord
    QTextCursor.PreviousWord = QTextCursor.MoveOperation.PreviousWord
    QTextCursor.NextCell = QTextCursor.MoveOperation.NextCell
    QTextCursor.PreviousCell = QTextCursor.MoveOperation.PreviousCell
    QTextCursor.NextRow = QTextCursor.MoveOperation.NextRow
    QTextCursor.PreviousRow = QTextCursor.MoveOperation.PreviousRow

print("[PATCH] QTextCursor патч применен для PySide6 совместимости")

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import QTimer, Qt
from ui.main_window import MainWindow
from styles import STYLES
from intro import IntroScreen
from simple_translation import translation

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
        "backups",
        "translations",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Создана директория: {directory}")
    
    # Проверяем наличие файлов переводов
    if not os.path.exists("translations/ru.json"):
        print("⚠️ Файл переводов ru.json не найден в translations/")
        # Копируем из корня, если есть
        if os.path.exists("ru.json"):
            import shutil
            shutil.copy2("ru.json", "translations/ru.json")
            print("✓ Скопирован ru.json из корня в translations/")
    
    if not os.path.exists("translations/en.json"):
        print("⚠️ Файл переводов en.json не найден в translations/")
        if os.path.exists("en.json"):
            import shutil
            shutil.copy2("en.json", "translations/en.json")
            print("✓ Скопирован en.json из корня в translations/")

def load_styles(app):
    """Загрузка стилей приложения"""
    try:
        app.setStyleSheet(STYLES)
        print(translation.t("styles.loaded_success", "Стили успешно загружены"))
    except Exception as e:
        print(f"{translation.t('styles.load_error', 'Ошибка загрузки стилей')}: {e}")
        if os.path.exists("styles.qss"):
            try:
                with open("styles.qss", "r", encoding="utf-8") as f:
                    app.setStyleSheet(f.read())
                    print(translation.t("styles.loaded_from_file", "Стили загружены из файла styles.qss"))
            except Exception as e2:
                print(f"{translation.t('styles.file_error', 'Ошибка загрузки стилей из файла')}: {e2}")

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
                        print(f"{translation.t('fonts.loaded', 'Шрифт загружен')}: {families[0]}")
                        font_loaded = True
            except Exception as e:
                print(f"{translation.t('fonts.load_error', 'Ошибка загрузки шрифта')} {font_path}: {e}")
    
    if not font_loaded:
        print(translation.t("fonts.not_found", "Шрифт Source Code Pro не найден. Используется стандартный моноширинный шрифт."))

def show_intro_and_main_window(app):
    """Показать интро и затем главное окно"""
    # Создаем главное окно, но пока не показываем
    main_window = MainWindow()
    
    # Создаем интро
    intro = IntroScreen()
    
    def on_intro_finished():
        """Действия после завершения интро"""
        print(translation.t("intro.completed", "Интро завершено, показываем главное окно..."))
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
    # Добавляем текущую директорию в путь для импортов
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Создаем необходимые директории
    create_directories()
    
    # Загружаем переводы (по умолчанию русский)
    translation.load_translations("ru")
    
    print(f"🌍 Текущий язык: {translation.get_current_language()}")
    print(f"📚 Доступные языки: {translation.get_available_languages()}")
    
    # Создаем экземпляр приложения
    app = QApplication(sys.argv)
    app.setApplicationName(translation.t("app.name", "Офисный хакер"))
    app.setApplicationVersion("0.5")
    app.setApplicationDisplayName(translation.t("app.title", "ОФИСНЫЙ ХАКЕР - СИМУЛЯТОР КИБЕРБЕЗОПАСНОСТИ"))
    
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
                print(f"{translation.t('app.icon_loaded', 'Иконка приложения загружена')}: {icon_path}")
                break
            except Exception as e:
                print(f"{translation.t('app.icon_error', 'Ошибка загрузки иконки')} {icon_path}: {e}")
    
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
                    print(translation.t("intro.already_shown", "Интро уже было показано, пропускаем..."))
                    show_intro = False
        except Exception as e:
            print(f"{translation.t('config.read_error', 'Ошибка чтения конфигурации')}: {e}")
    
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
    
    print(translation.t("app.closed", "Приложение завершено."))
    sys.exit(exit_code)

if __name__ == "__main__":
    main()