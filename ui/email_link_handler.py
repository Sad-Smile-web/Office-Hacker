# ui/email_link_handler.py
from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtGui import QDesktopServices
from simple_translation import translation

try:
    from ui.browser.browser_window import BrowserWindow
    BROWSER_AVAILABLE = True
except ImportError:
    BROWSER_AVAILABLE = False
    print("[ПРЕДУПРЕЖДЕНИЕ] Браузер недоступен. Ссылки не будут открываться.")


class EmailLinkHandler(QObject):
    """Обработчик ссылок в письмах"""
    
    link_clicked = Signal(str)  # Сигнал при клике на ссылку
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.browser_windows = []
    
    def handle_link_click(self, url: QUrl):
        """Обработать клик по ссылке в письме"""
        url_str = url.toString()
        self.link_clicked.emit(url_str)
        
        # Обрабатываем ссылки app.cyb://
        if url_str.startswith("app.cyb://"):
            self.open_cyb_link(url_str)
        # Обрабатываем почтовые адреса (открываем в стандартном клиенте)
        elif url_str.startswith("mailto:"):
            QDesktopServices.openUrl(url)
        # Игнорируем другие ссылки (или открываем стандартным способом)
        else:
            print(f"[ССЫЛКА] Неподдерживаемая ссылка: {url_str}")
    
    def open_cyb_link(self, url: str):
        """Открыть ссылку app.cyb:// в браузере игры"""
        if not BROWSER_AVAILABLE:
            print(f"[ОШИБКА] Браузер недоступен. Не могу открыть: {url}")
            return
        
        try:
            # Создаем новое окно браузера
            from ui.browser.browser_window import BrowserWindow
            browser = BrowserWindow(url)
            browser.show()
            
            # Сохраняем ссылку на окно
            self.browser_windows.append(browser)
            
            # Подключаем сигнал закрытия для удаления из списка
            browser.destroyed.connect(lambda: self.remove_browser(browser))
            
            print(f"[БРАУЗЕР] Открыта ссылка: {url}")
        except Exception as e:
            print(f"[ОШИБКА] Не удалось открыть браузер: {e}")
    
    def remove_browser(self, browser):
        """Удалить браузер из списка при закрытии"""
        if browser in self.browser_windows:
            self.browser_windows.remove(browser)
    
    def close_all_browsers(self):
        """Закрыть все открытые браузеры"""
        for browser in self.browser_windows[:]:
            try:
                browser.close()
            except:
                pass
        self.browser_windows.clear()