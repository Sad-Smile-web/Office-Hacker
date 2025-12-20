@echo off
chcp 65001 >nul
title Установка "Офисный Хакер"
color 0A

echo ============================================
echo    УСТАНОВКА "ОФИСНЫЙ ХАКЕР"
echo ============================================
echo.

echo [INFO] Установка Python зависимостей...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Ошибка установки зависимостей!
    echo Установка вручную...
    
    pip install PySide6
    pip install pygame
    pip install numpy
    pip install Pillow
)

echo [INFO] Создание структуры папок...
if not exist "assets" mkdir assets
if not exist "assets\fonts" mkdir assets\fonts
if not exist "assets\icons" mkdir assets\icons
if not exist "assets\sounds" mkdir assets\sounds
if not exist "saves" mkdir saves
if not exist "ui" mkdir ui

echo [INFO] Создание звуковых файлов...
if exist "install_sounds.py" (
    python install_sounds.py
)

echo [INFO] Создание иконки...
if exist "create_icon.py" (
    python create_icon.py
)

echo.
echo [SUCCESS] Установка завершена!
echo.
echo Запустите игру командой: run.bat
echo.
pause