@echo off
chcp 65001 >nul
title Корпоративный хакер - симулятор
color 0A

echo ============================================
echo    ЗАПУСК "ОФИСНЫЙ ХАКЕР"
echo ============================================
echo.

REM Проверка Python
echo [INFO] Проверка Python...
python --version >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python не установлен или не добавлен в PATH!
    echo Установите Python 3.8 или выше с сайта python.org
    echo Или запустите install.bat для установки
    pause
    exit /b 1
)
python --version

REM Проверка PySide6
echo [INFO] Проверка PySide6...
python -c "import PySide6" 2>nul
if errorlevel 1 (
    echo [ERROR] PySide6 не установлен!
    echo Установка PySide6...
    pip install PySide6
    if errorlevel 1 (
        echo [ERROR] Не удалось установить PySide6!
        pause
        exit /b 1
    )
    echo [SUCCESS] PySide6 установлен
)

REM Проверка pygame
echo [INFO] Проверка pygame...
python -c "import pygame" 2>nul
if errorlevel 1 (
    echo [ERROR] pygame не установлен!
    echo Установка pygame...
    pip install pygame
    if errorlevel 1 (
        echo [ERROR] Не удалось установить pygame!
        pause
        exit /b 1
    )
    echo [SUCCESS] pygame установлен
)

REM Проверка numpy
echo [INFO] Проверка numpy...
python -c "import numpy" 2>nul
if errorlevel 1 (
    echo [ERROR] numpy не установлен!
    echo Установка numpy...
    pip install numpy
    if errorlevel 1 (
        echo [ERROR] Не удалось установить numpy!
        pause
        exit /b 1
    )
    echo [SUCCESS] numpy установлен
)

REM Проверка Pillow
echo [INFO] Проверка Pillow...
python -c "import PIL" 2>nul
if errorlevel 1 (
    echo [ERROR] Pillow не установлен!
    echo Установка Pillow...
    pip install Pillow
    if errorlevel 1 (
        echo [ERROR] Не удалось установить Pillow!
        pause
        exit /b 1
    )
    echo [SUCCESS] Pillow установлен
)

REM Проверка папок
echo [INFO] Проверка структуры папок...
if not exist "assets" mkdir assets
if not exist "assets\fonts" mkdir assets\fonts
if not exist "assets\icons" mkdir assets\icons
if not exist "assets\sounds" mkdir assets\sounds
if not exist "saves" mkdir saves
if not exist "ui" mkdir ui

REM Проверка необходимых файлов
echo [INFO] Проверка необходимых файлов...
set "missing_files=0"
for %%f in (
    main.py 
    game_state.py 
    styles.py 
    ui\main_window.py 
    ui\menu_widget.py 
    ui\game_widget.py 
    ui\about_widget.py 
    ui\help_widget.py 
    ui\terminal_widget.py 
    ui\effects.py
    audio_manager.py
) do (
    if not exist "%%f" (
        echo [WARNING] Отсутствует файл: %%f
        set /a missing_files+=1
    )
)

if %missing_files% GTR 0 (
    echo [WARNING] Отсутствует %missing_files% файлов!
    echo Создание недостающих файлов...
    
    REM Создание папки ui если ее нет
    if not exist "ui" mkdir ui
    
    REM Создание пустых файлов если их нет
    for %%f in (
        ui\__init__.py
        ui\help_widget.py
    ) do (
        if not exist "%%f" (
            echo # Файл создан автоматически > "%%f"
            echo [INFO] Создан файл: %%f
        )
    )
)

REM Создание звуков если их нет
echo [INFO] Проверка звуков...
if not exist "assets\sounds\typing.wav" (
    echo [INFO] Создание звуковых файлов...
    python install_sounds.py
)

echo.
echo [SUCCESS] Все проверки пройдены
echo.

REM Запуск игры
echo ============================================
echo    ЗАПУСК ИГРЫ...
echo ============================================
echo.

python main.py

REM Если игра завершилась с ошибкой
if errorlevel 1 (
    echo.
    echo ============================================
    echo    ИГРА ЗАВЕРШИЛАСЬ С ОШИБКОЙ
    echo ============================================
    echo.
    echo Возможные решения:
    echo 1. Запустите install.bat заново
    echo 2. Проверьте наличие файла main.py
    echo 3. Установите зависимости: pip install PySide6 pygame numpy Pillow
    echo 4. Проверьте права доступа к файлам
    echo.
    echo Подробности ошибки выше в логе
    echo.
)

pause