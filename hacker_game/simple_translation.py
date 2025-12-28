# simple_translation.py

import json
import os
import sys

class SimpleTranslation:
    """ПРОСТЕЙШИЙ менеджер переводов"""
    
    def __init__(self):
        """Инициализация менеджера переводов"""
        self.translations = {}
        self.language = "ru"
        self.language_changed_callbacks = []
    
    def get_base_path(self):
        """Получить базовый путь (работает и в exe и в исходниках)"""
        if hasattr(sys, '_MEIPASS'):
            # Мы в упакованном приложении (exe)
            base_path = sys._MEIPASS
        else:
            # Мы в исходном коде
            base_path = os.path.dirname(os.path.abspath(__file__))
        return base_path
    
    def load_translations(self, language):
        """Загрузить переводы из файла"""
        base_path = self.get_base_path()
        
        # Пробуем разные пути
        possible_paths = [
            os.path.join(base_path, "translations", f"{language}.json"),
            os.path.join(os.path.dirname(base_path), "translations", f"{language}.json"),
            os.path.join(os.getcwd(), "translations", f"{language}.json"),
            os.path.join(os.path.dirname(sys.executable), "translations", f"{language}.json"),
        ]
        
        if hasattr(sys, 'frozen'):
            # Добавляем путь рядом с exe файлом
            exe_dir = os.path.dirname(sys.executable)
            possible_paths.append(os.path.join(exe_dir, "translations", f"{language}.json"))
            possible_paths.append(os.path.join(exe_dir, f"{language}.json"))
        
        print(f"📂 Ищу файлы переводов для языка: {language}")
        
        for file_path in possible_paths:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.translations = json.load(f)
                    self.language = language
                    print(f"✅ Загружен язык: {language} из {file_path}")
                    
                    # Вызываем коллбэки для обновления UI
                    for callback in self.language_changed_callbacks:
                        try:
                            callback()
                        except Exception as e:
                            print(f"❌ Ошибка в коллбэке: {e}")
                    return True
                except Exception as e:
                    print(f"❌ Ошибка загрузки переводов из {file_path}: {e}")
        
        # Если файл не найден, пробуем загрузить встроенные переводы
        print(f"⚠️ Файлы переводов не найдены, загружаю встроенные для {language}")
        return self.load_builtin_translations(language)
    
    def load_builtin_translations(self, language):
        """Загрузить встроенные переводы"""
        builtin_translations = {
            "ru": {
                "menu": {
                    "title": "ГЛАВНОЕ МЕНЮ",
                    "new_game": "НОВАЯ ИГРА",
                    "load_game": "ЗАГРУЗИТЬ СОХРАНЕНИЕ",
                    "settings": "НАСТРОЙКИ",
                    "about": "О ПРОГРАММЕ",
                    "help": "ПОМОЩЬ",
                    "exit": "ВЫХОД"
                },
                "game": {
                    "input_name_title": "Регистрация сотрудника",
                    "input_first_name": "Имя:",
                    "input_last_name": "Фамилия:",
                    "ok": "Принять",
                    "cancel": "Отмена"
                }
            },
            "en": {
                "menu": {
                    "title": "MAIN MENU",
                    "new_game": "NEW GAME",
                    "load_game": "LOAD GAME",
                    "settings": "SETTINGS",
                    "about": "ABOUT",
                    "help": "HELP",
                    "exit": "EXIT"
                },
                "game": {
                    "input_name_title": "Employee Registration",
                    "input_first_name": "First Name:",
                    "input_last_name": "Last Name:",
                    "ok": "OK",
                    "cancel": "Cancel"
                }
            },
            "sp": {
                "menu": {
                    "title": "MENÚ PRINCIPAL",
                    "new_game": "NUEVO JUEGO",
                    "load_game": "CARGAR JUEGO",
                    "settings": "AJUSTES",
                    "about": "ACERCA DE",
                    "help": "AYUDA",
                    "exit": "SALIR"
                },
                "game": {
                    "input_name_title": "Registro de Empleado",
                    "input_first_name": "Nombre:",
                    "input_last_name": "Apellido:",
                    "ok": "Aceptar",
                    "cancel": "Cancelar"
                }
            }
        }
        
        if language in builtin_translations:
            self.translations = builtin_translations[language]
            self.language = language
            print(f"✅ Загружены встроенные переводы для: {language}")
            
            # Вызываем коллбэки
            for callback in self.language_changed_callbacks:
                try:
                    callback()
                except Exception as e:
                    print(f"❌ Ошибка в коллбэке: {e}")
            return True
        
        print(f"❌ Встроенных переводов для {language} не найдено")
        return False
    
    def set_language(self, language):
        """Сменить язык"""
        success = self.load_translations(language)
        if success:
            print(f"🌍 Язык установлен: {language}")
        else:
            print(f"⚠️ Не удалось установить язык: {language}")
        return success
    
    def on_language_changed(self, callback):
        """Подписаться на смену языка"""
        if callback not in self.language_changed_callbacks:
            self.language_changed_callbacks.append(callback)
    
    def t(self, key, default=None, **kwargs):
        """
        Получить перевод по ключу
        print(f"🔍 Поиск ключа: '{key}' в языке: {self.language}")
        Пример: t("menu.title") -> "ГЛАВНОЕ МЕНЮ"
        Пример с переменными: t("game.balance", money=100) -> "💰 Баланс: 100"
        
        Аргументы:
            key: ключ перевода (например "menu.title")
            default: значение по умолчанию если ключ не найден
            **kwargs: переменные для подстановки в строку
        """
        try:
            # Ищем ключ в словаре (разделяем по точкам)
            keys = key.split('.')
            value = self.translations
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    # Если ключ не найден, возвращаем значение по умолчанию или ключ
                    if default is not None:
                        return default
                    return f"[{key}]"
            
            # Если есть переменные для замены
            if kwargs and isinstance(value, str):
                try:
                    return value.format(**kwargs)
                except KeyError as e:
                    print(f"⚠️ Недостаточно переменных для перевода '{key}': {e}")
                    return value
            
            return str(value) if value is not None else f"[{key}]"
            
        except Exception as e:
            print(f"❌ Ошибка перевода для ключа '{key}': {e}")
            if default is not None:
                return default
            return f"[{key}]"
    
    def get_translation_dict(self):
        """Получить весь словарь переводов"""
        return self.translations
    
    def get_available_languages(self):
        """Получить список доступных языков"""
        languages = []
        
        # Проверяем разные пути
        base_path = self.get_base_path()
        possible_dirs = [
            os.path.join(base_path, "translations"),
            os.path.join(os.path.dirname(base_path), "translations"),
            os.path.join(os.getcwd(), "translations"),
            os.path.join(os.path.dirname(sys.executable), "translations"),
        ]
        
        if hasattr(sys, 'frozen'):
            exe_dir = os.path.dirname(sys.executable)
            possible_dirs.append(os.path.join(exe_dir, "translations"))
        
        for trans_dir in possible_dirs:
            if os.path.exists(trans_dir):
                for file in os.listdir(trans_dir):
                    if file.endswith(".json"):
                        language = file.replace(".json", "")
                        if language not in languages:
                            languages.append(language)
        
        # Добавляем встроенные языки
        for lang in ["ru", "en", "sp"]:
            if lang not in languages:
                languages.append(lang)
        
        return sorted(languages)
    
    def get_current_language(self):
        """Получить текущий язык"""
        return self.language
    
    def has_key(self, key):
        """Проверить наличие ключа перевода"""
        try:
            keys = key.split('.')
            value = self.translations
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return False
            return True
        except:
            return False

# Создаем глобальный объект для использования везде
translation = SimpleTranslation()