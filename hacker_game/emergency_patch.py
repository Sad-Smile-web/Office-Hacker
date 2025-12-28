# emergency_patch.py
# Экстренный патч для QTextCursor в PySide6
# Запустите этот файл ПЕРЕД запуском main.py

import sys
import os

def emergency_patch():
    """Аварийный патч для QTextCursor"""
    try:
        from PySide6.QtGui import QTextCursor
        
        print("[EMERGENCY PATCH] Применяю аварийный патч для QTextCursor...")
        
        # Патчим класс
        if not hasattr(QTextCursor, 'End'):
            QTextCursor.End = QTextCursor.MoveOperation.End
            QTextCursor.Start = QTextCursor.MoveOperation.Start
            QTextCursor.Right = QTextCursor.MoveOperation.Right
            QTextCursor.Left = QTextCursor.MoveOperation.Left
            QTextCursor.Up = QTextCursor.MoveOperation.Up
            QTextCursor.Down = QTextCursor.MoveOperation.Down
        
        # Патчим экземпляры через метакласс
        class PatchedCursor(QTextCursor.__class__):
            def __getattr__(self, name):
                if name == 'End':
                    return QTextCursor.MoveOperation.End
                elif name == 'Start':
                    return QTextCursor.MoveOperation.Start
                elif name == 'Right':
                    return QTextCursor.MoveOperation.Right
                elif name == 'Left':
                    return QTextCursor.MoveOperation.Left
                elif name == 'Up':
                    return QTextCursor.MoveOperation.Up
                elif name == 'Down':
                    return QTextCursor.MoveOperation.Down
                else:
                    raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        # Применяем метакласс ко всем экземплярам
        QTextCursor.__class__ = PatchedCursor
        
        print("[EMERGENCY PATCH] Патч успешно применен!")
        return True
        
    except Exception as e:
        print(f"[EMERGENCY PATCH ERROR] Ошибка: {e}")
        return False

# Автоматически применяем патч при импорте
if __name__ == "__main__":
    emergency_patch()
    print("Патч готов. Теперь запустите main.py")
else:
    emergency_patch()
