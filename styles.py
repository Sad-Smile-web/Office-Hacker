# styles.py - Полный файл стилей для "Офисный Хакер" с киберпанк-стилями
STYLES = """
/* ============================================================================
   БАЗОВЫЕ СТИЛИ
   ============================================================================ */

/* Основные стили для приложения */
QMainWindow {
    background-color: #000000;
    border: 2px solid #00ff00;
}

QWidget {
    color: #00ff00;
    font-family: 'Source Code Pro', 'Consolas', monospace;
    background-color: transparent;
}

/* ============================================================================
   КНОПКИ
   ============================================================================ */

/* Стандартные кнопки */
QPushButton {
    background-color: #002200;
    color: #00ff00;
    border: 2px solid #00ff00;
    padding: 8px 12px;
    font-weight: bold;
    border-radius: 4px;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

QPushButton:hover {
    background-color: #004400;
    border-color: #00ff00;
    color: #ffffff;
    border-width: 3px;
}

QPushButton:pressed {
    background-color: #001100;
    border-color: #00aa00;
}

QPushButton:disabled {
    background-color: #001100;
    color: #008800;
    border-color: #008800;
    opacity: 0.5;
}

/* Киберпанк кнопки */
.cyber-button {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #2a2a3e,
        stop:1 #1a1a2e
    );
    color: #cccccc;
    border: 2px solid #00ffff;
    padding: 10px 15px;
    font-weight: bold;
    border-radius: 6px;
    font-size: 13px;
    font-family: 'Source Code Pro';
    text-transform: uppercase;
    letter-spacing: 1px;
}

.cyber-button:hover {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #0064c8,
        stop:1 #003264
    );
    border-color: #00ffff;
    color: #ffffff;
    border-width: 3px;
    text-shadow: 0 0 10px #00ffff;
}

.cyber-button:pressed {
    background-color: rgba(0, 50, 100, 0.9);
}

/* Неоновые кнопки */
.neon-button {
    background-color: transparent;
    color: #00ffff;
    border: 2px solid #00ffff;
    padding: 8px 16px;
    font-weight: bold;
    border-radius: 5px;
    font-size: 12px;
    text-shadow: 0 0 5px #00ffff;
}

.neon-button:hover {
    background-color: rgba(0, 255, 255, 0.1);
    border-color: #ffffff;
    color: #ffffff;
    text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.neon-button:pressed {
    background-color: rgba(0, 200, 200, 0.2);
}

/* ============================================================================
   ПОЛЯ ВВОДА И ТЕКСТА
   ============================================================================ */

QLineEdit {
    background-color: #001100;
    color: #00ff00;
    border: 2px solid #00ff00;
    padding: 8px;
    border-radius: 4px;
    font-size: 12px;
    selection-background-color: #00aa00;
}

QLineEdit:focus {
    border: 2px solid #00ffff;
    background-color: #002200;
    color: #ffffff;
}

QTextEdit, QPlainTextEdit {
    background-color: #000000;
    color: #00ff00;
    border: 2px solid #00ff00;
    padding: 8px;
    border-radius: 4px;
    font-size: 11px;
    selection-background-color: #00aa00;
}

QTextEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #00ffff;
}

/* ============================================================================
   МЕТКИ
   ============================================================================ */

QLabel {
    color: #00ff00;
    background-color: transparent;
}

QLabel[important="true"] {
    color: #ffff00;
    font-weight: bold;
    text-shadow: 0 0 5px #ffff00;
}

QLabel[title="true"] {
    color: #00bfff;
    font-size: 24px;
    font-weight: bold;
    text-shadow: 0 0 10px #00bfff;
}

/* Неоновые заголовки */
.neon-header {
    color: #ffffff;
    font-family: 'Source Code Pro';
    font-size: 22px;
    font-weight: bold;
    letter-spacing: 3px;
    text-transform: uppercase;
    text-shadow: 
        0 0 5px currentColor,
        0 0 10px currentColor,
        0 0 15px currentColor,
        0 0 20px currentColor;
}

/* ============================================================================
   ФРЕЙМЫ И ПАНЕЛИ
   ============================================================================ */

QFrame {
    border: 1px solid #00ff00;
    border-radius: 5px;
    background-color: #0a0a0a;
}

QFrame[flat="true"] {
    border: none;
    background-color: transparent;
}

/* Киберпанк фреймы */
.cyber-frame {
    background-color: rgba(10, 10, 20, 0.8);
    border: 2px solid #00bfff;
    border-radius: 8px;
    padding: 10px;
}

.cyber-frame-alternate {
    background-color: rgba(10, 10, 30, 0.8);
    border: 2px solid #8a2be2;
    border-radius: 8px;
    padding: 10px;
}

.cyber-frame-danger {
    background-color: rgba(30, 10, 10, 0.8);
    border: 2px solid #ff4444;
    border-radius: 8px;
    padding: 10px;
}

/* Голографические фреймы */
.holographic-frame {
    background-color: rgba(0, 20, 40, 0.6);
    border: 2px solid #00ffff;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

/* ============================================================================
   ПРОКРУТКА
   ============================================================================ */

QScrollBar:vertical {
    background: #001100;
    width: 14px;
    border-radius: 7px;
    border: 2px solid #003300;
}

QScrollBar::handle:vertical {
    background: #00aa00;
    min-height: 30px;
    border-radius: 7px;
    border: 1px solid #00ff00;
}

QScrollBar::handle:vertical:hover {
    background: #00ffff;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: #003300;
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: #001100;
}

QScrollBar:horizontal {
    background: #001100;
    height: 14px;
    border-radius: 7px;
    border: 2px solid #003300;
}

QScrollBar::handle:horizontal {
    background: #00aa00;
    min-width: 30px;
    border-radius: 7px;
    border: 1px solid #00ff00;
}

QScrollBar::handle:horizontal:hover {
    background: #00ffff;
}

/* Неоновые скроллбары */
.neon-scrollbar:vertical {
    background: #1a1a2e;
    width: 14px;
    border-radius: 7px;
    border: 2px solid #2a2a3e;
}

.neon-scrollbar::handle:vertical {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #ff00ff,
        stop:0.5 #00ffff,
        stop:1 #ff00ff
    );
    min-height: 40px;
    border-radius: 7px;
    border: 1px solid #ffffff;
}

.neon-scrollbar::handle:vertical:hover {
    background: #ffffff;
}

/* ============================================================================
   СЛАЙДЕРЫ И ПРОГРЕСС-БАРЫ
   ============================================================================ */

QSlider::groove:horizontal {
    border: 1px solid #00ff00;
    height: 10px;
    background: #001100;
    border-radius: 5px;
}

QSlider::handle:horizontal {
    background: #00ff00;
    width: 20px;
    margin: -5px 0;
    border-radius: 10px;
}

QSlider::handle:horizontal:hover {
    background: #00ffff;
    border: 1px solid #ffffff;
}

QProgressBar {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    border-radius: 4px;
    text-align: center;
    font-size: 11px;
}

QProgressBar::chunk {
    background-color: #00ff00;
    border-radius: 3px;
}

/* Киберпанк прогресс-бары */
.cyber-progress {
    background-color: #1a1a2e;
    border: 2px solid #00ffff;
    border-radius: 8px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
}

.cyber-progress::chunk {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #00ffff,
        stop:0.5 #0088ff,
        stop:1 #00ffff
    );
    border-radius: 6px;
    border: 1px solid #ffffff;
}

/* ============================================================================
   МЕНЮ И ВКЛАДКИ
   ============================================================================ */

QMenuBar {
    background-color: #001100;
    color: #00ff00;
    border-bottom: 2px solid #00ff00;
    font-size: 12px;
}

QMenuBar::item:selected {
    background-color: #003300;
    border-radius: 3px;
}

QMenu {
    background-color: #001100;
    color: #00ff00;
    border: 2px solid #00ff00;
    padding: 5px;
    border-radius: 5px;
}

QMenu::item:selected {
    background-color: #003300;
    border-radius: 3px;
}

QMenu::separator {
    height: 1px;
    background-color: #00ff00;
    margin: 5px 0;
}

QTabWidget::pane {
    border: 2px solid #00ff00;
    background-color: #000000;
    border-radius: 6px;
    padding: 5px;
}

QTabBar::tab {
    background-color: #001100;
    color: #00ff00;
    padding: 8px 16px;
    border: 2px solid #00ff00;
    margin-right: 2px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background-color: #003300;
    border-bottom: none;
    color: #ffffff;
}

QTabBar::tab:hover {
    background-color: #002200;
    color: #00ffff;
}

QTabBar::tab:!selected {
    margin-top: 2px;
}

/* ============================================================================
   СПИСКИ И ТАБЛИЦЫ
   ============================================================================ */

QListView, QTreeView, QTableView {
    background-color: #001100;
    color: #00ff00;
    border: 2px solid #00ff00;
    border-radius: 5px;
    outline: none;
    font-size: 11px;
}

QListView::item:selected, QTreeView::item:selected, QTableView::item:selected {
    background-color: #003300;
    color: #ffffff;
}

QListView::item:hover, QTreeView::item:hover, QTableView::item:hover {
    background-color: #002200;
}

/* ============================================================================
   КОМБО-БОКСЫ, ЧЕКБОКСЫ, РАДИОКНОПКИ
   ============================================================================ */

QComboBox {
    background-color: #001100;
    color: #00ff00;
    border: 2px solid #00ff00;
    padding: 5px;
    border-radius: 4px;
    min-width: 100px;
}

QComboBox::drop-down {
    border: none;
    width: 25px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #00ff00;
}

QComboBox QAbstractItemView {
    background-color: #001100;
    color: #00ff00;
    border: 2px solid #00ff00;
    selection-background-color: #003300;
}

QCheckBox {
    color: #00ff00;
    spacing: 8px;
    font-size: 12px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #00ff00;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: #00ff00;
    image: url("assets/icons/check.svg");
}

QCheckBox::indicator:unchecked:hover {
    border: 2px solid #00ffff;
}

QRadioButton {
    color: #00ff00;
    spacing: 8px;
    font-size: 12px;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #00ff00;
    border-radius: 8px;
}

QRadioButton::indicator:checked {
    background-color: #00ff00;
}

QRadioButton::indicator:unchecked:hover {
    border: 2px solid #00ffff;
}

/* ============================================================================
   ДИАЛОГИ И СООБЩЕНИЯ
   ============================================================================ */

QDialog {
    background-color: #000000;
    border: 3px solid #00ff00;
    border-radius: 8px;
}

QMessageBox {
    background-color: #000000;
    color: #00ff00;
    border: 3px solid #00ff00;
    border-radius: 8px;
}

QMessageBox QLabel {
    color: #00ff00;
}

QMessageBox QPushButton {
    min-width: 100px;
    padding: 8px 16px;
}

/* ============================================================================
   СПЕЦИАЛЬНЫЕ КЛАССЫ ВИДЖЕТОВ
   ============================================================================ */

/* Терминал */
TerminalWidget {
    background-color: #000000;
    border: 3px solid #00ff00;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
}

TerminalWidget QTextEdit {
    border: none;
    background-color: transparent;
}

TerminalWidget QLineEdit {
    border-left: none;
    border-right: none;
    border-bottom: none;
    border-top: 2px solid #00ff00;
}

/* Наблюдение */
OfficeView {
    background-color: #101020;
    border: 3px solid #ff4444;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
}

/* ============================================================================
   КИБЕРПАНК СТИЛИ ДЛЯ НАВЫКОВ
   ============================================================================ */

/* Контейнер навыков */
SkillsContainer {
    background-color: transparent;
    border: none;
    padding: 0px;
}

/* Отдельный виджет навыка */
CyberSkillWidget {
    background-color: transparent;
    border: none;
    padding: 0px;
}

/* Круглые индикаторы навыков (компактный вид) */
CompactSkillCircle {
    background-color: transparent;
    border: none;
}

/* Заголовок панели навыков */
#skillsHeader {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #ff00ff,
        stop:0.3 #00ffff,
        stop:0.7 #ffff00,
        stop:1 #ff00ff
    );
    border-radius: 12px;
    padding: 2px;
}

/* Внутренний заголовок */
#skillsHeader QFrame {
    background-color: #0a0a1a;
    border-radius: 10px;
    padding: 15px;
}

/* Кнопка возврата из навыков */
#backToInfoButton {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #2a2a3e,
        stop:1 #1a1a2e
    );
    color: #cccccc;
    border: 2px solid #00bfff;
    padding: 12px;
    font-family: 'Source Code Pro';
    font-weight: bold;
    border-radius: 10px;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

#backToInfoButton:hover {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #0064c8,
        stop:1 #003264
    );
    border-color: #00ffff;
    color: #ffffff;
    border-width: 3px;
    text-shadow: 0 0 10px #00ffff;
}

/* Информационная панель навыков */
.skills-info-panel {
    background-color: rgba(20, 20, 40, 0.7);
    border: 1px solid rgba(0, 191, 255, 0.3);
    border-radius: 8px;
    padding: 10px;
}

.skills-info-panel QLabel {
    color: #aaaaaa;
    font-family: 'Source Code Pro';
    font-size: 11px;
    line-height: 1.4;
}

/* ============================================================================
   ПОЧТОВЫЙ КЛИЕНТ
   ============================================================================ */

.mail-client {
    background-color: rgba(10, 10, 30, 0.8);
    border: 2px solid #8a2be2;
    border-radius: 8px;
}

.mail-header {
    font-size: 16px;
    font-weight: bold;
    color: #8a2be2;
    padding: 5px;
    background-color: rgba(68, 0, 68, 0.5);
    border-radius: 5px;
    margin-bottom: 10px;
}

.mail-list {
    background-color: #000000;
    border: 1px solid #4b0082;
    border-radius: 5px;
    padding: 5px;
    color: #cccccc;
    font-size: 12px;
}

.mail-list::item {
    padding: 8px;
    border-bottom: 1px solid #333333;
}

.mail-list::item:selected {
    background-color: #4b0082;
    border: 1px solid #9370db;
    border-radius: 3px;
}

.mail-list::item:hover {
    background-color: #2d004d;
}

.mail-list-unread {
    color: #ffffff;
    font-weight: bold;
}

.mail-list-read {
    color: #888888;
}

.mail-view {
    background-color: #000000;
    color: #cccccc;
    font-size: 11px;
    font-family: 'Courier New', monospace;
    border: 1px solid #4b0082;
    border-radius: 5px;
    padding: 10px;
    selection-background-color: #4b0082;
}

.mail-button {
    background-color: rgba(42, 42, 62, 0.9);
    color: #cccccc;
    border: 1px solid #8a2be2;
    padding: 6px;
    font-weight: bold;
    border-radius: 4px;
    font-size: 11px;
}

.mail-button:hover {
    background-color: rgba(100, 50, 200, 0.8);
    border-color: #9370db;
    color: #ffffff;
}

.mail-button-delete {
    background-color: rgba(62, 42, 42, 0.9);
    border: 1px solid #ff4444;
}

.mail-button-delete:hover {
    background-color: rgba(200, 50, 50, 0.8);
    border-color: #ff8888;
}

/* ============================================================================
   ВРЕМЯ И ДАТА
   ============================================================================ */

TimeWidget {
    background-color: transparent;
    margin: 10px 0px;
}

.time-display {
    color: #00ffff;
    font-family: 'Source Code Pro', monospace;
    font-size: 14px;
    font-weight: bold;
}

.time-hour {
    color: #1dd1a1;
    font-family: 'Source Code Pro';
    font-size: 28px;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(29, 209, 161, 0.7);
}

.time-minute {
    color: #00bfff;
    font-family: 'Source Code Pro';
    font-size: 28px;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(0, 191, 255, 0.7);
}

.time-date {
    color: #00bfff;
    font-family: 'Source Code Pro';
    font-size: 14px;
    font-weight: bold;
    text-shadow: 0 0 5px rgba(0, 191, 255, 0.5);
}

.time-left {
    color: #feca57;
    font-family: 'Source Code Pro';
    font-size: 11px;
    font-weight: bold;
}

/* ============================================================================
   АНИМАЦИИ
   ============================================================================ */

/* Общие анимации */
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0.3; }
    100% { opacity: 1; }
}

.blink {
    animation: blink 1s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.8; }
    100% { transform: scale(1); opacity: 1; }
}

.pulse {
    animation: pulse 2s infinite;
}

/* Анимация для времени */
@keyframes time-blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.time-separator {
    animation: time-blink 1s infinite;
}

@keyframes time-pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}

.time-pulse {
    animation: time-pulse 2s infinite;
}

/* Анимации для навыков */
@keyframes skill-level-up {
    0% {
        transform: scale(1);
        opacity: 1;
    }
    25% {
        transform: scale(1.3);
        opacity: 0.8;
    }
    50% {
        transform: scale(1.1);
        opacity: 1;
    }
    75% {
        transform: scale(1.2);
        opacity: 0.9;
    }
    100% {
        transform: scale(1);
        opacity: 1;
    }
}

.skill-level-up {
    animation: skill-level-up 2s ease-out;
}

@keyframes skill-pulse {
    0%, 100% { 
        opacity: 0.7;
        box-shadow: 0 0 10px currentColor;
    }
    50% { 
        opacity: 1;
        box-shadow: 0 0 20px currentColor, 0 0 30px currentColor;
    }
}

.skill-pulse {
    animation: skill-pulse 2s infinite;
}

@keyframes skill-glow {
    0%, 100% { 
        filter: brightness(1);
        text-shadow: 0 0 5px currentColor;
    }
    50% { 
        filter: brightness(1.3);
        text-shadow: 0 0 10px currentColor, 0 0 15px currentColor;
    }
}

.skill-glow {
    animation: skill-glow 1.5s infinite;
}

@keyframes skill-sparkle {
    0% {
        transform: translate(0, 0) rotate(0deg);
        opacity: 0;
    }
    10% {
        opacity: 1;
    }
    90% {
        opacity: 1;
    }
    100% {
        transform: translate(var(--sparkle-x, 50px), var(--sparkle-y, -50px)) rotate(360deg);
        opacity: 0;
    }
}

.skill-sparkle {
    animation: skill-sparkle 1s ease-out;
}

/* Неоновое свечение */
@keyframes neon-glow {
    0%, 100% {
        text-shadow: 
            0 0 5px currentColor,
            0 0 10px currentColor,
            0 0 15px currentColor;
        box-shadow: 
            0 0 5px currentColor,
            0 0 10px currentColor,
            0 0 15px currentColor inset;
    }
    50% {
        text-shadow: 
            0 0 10px currentColor,
            0 0 20px currentColor,
            0 0 30px currentColor;
        box-shadow: 
            0 0 10px currentColor,
            0 0 20px currentColor,
            0 0 25px currentColor inset;
    }
}

.neon-glow {
    animation: neon-glow 2s infinite;
}

/* Голографический эффект */
@keyframes hologram-scan {
    0% {
        background-position: 0% 0%;
        opacity: 0.7;
    }
    50% {
        opacity: 1;
    }
    100% {
        background-position: 0% 100%;
        opacity: 0.7;
    }
}

.hologram-effect {
    background: linear-gradient(
        to bottom,
        transparent,
        rgba(0, 255, 255, 0.1) 20%,
        rgba(0, 255, 255, 0.3) 50%,
        rgba(0, 255, 255, 0.1) 80%,
        transparent
    );
    background-size: 100% 200%;
    animation: hologram-scan 3s linear infinite;
}

/* ============================================================================
   ЦВЕТОВЫЕ СХЕМЫ ПО ВРЕМЕНИ СУТОК
   ============================================================================ */

.time-morning {
    color: #1dd1a1;
    border-color: #1dd1a1;
    text-shadow: 0 0 10px rgba(29, 209, 161, 0.5);
}

.time-afternoon {
    color: #feca57;
    border-color: #feca57;
    text-shadow: 0 0 10px rgba(254, 202, 87, 0.5);
}

.time-evening {
    color: #ff6b6b;
    border-color: #ff6b6b;
    text-shadow: 0 0 10px rgba(255, 107, 107, 0.5);
}

.time-night {
    color: #5f27cd;
    border-color: #5f27cd;
    text-shadow: 0 0 10px rgba(95, 39, 205, 0.5);
}

/* ============================================================================
   ЦВЕТОВЫЕ СХЕМЫ НАВЫКОВ
   ============================================================================ */

.skill-hacking {
    color: #ff0066;
    border-color: #ff0066;
}

.skill-social {
    color: #ff9900;
    border-color: #ff9900;
}

.skill-programming {
    color: #ffff00;
    border-color: #ffff00;
}

.skill-stealth {
    color: #00ff00;
    border-color: #00ff00;
}

.skill-analysis {
    color: #00ffff;
    border-color: #00ffff;
}

.skill-network {
    color: #0066ff;
    border-color: #0066ff;
}

/* Уровни навыков */
.skill-beginner {
    color: #00ff00;
    border-color: #00ff00;
}

.skill-intermediate {
    color: #00bfff;
    border-color: #00bfff;
}

.skill-advanced {
    color: #ff00ff;
    border-color: #ff00ff;
}

.skill-expert {
    color: #ff8800;
    border-color: #ff8800;
}

.skill-master {
    color: #ffff00;
    border-color: #ffff00;
    text-shadow: 0 0 10px #ffff00;
}

/* ============================================================================
   ЦВЕТОВЫЕ СХЕМЫ ИНТЕРФЕЙСА
   ============================================================================ */

.color-scheme-hacker {
    color: #00ff00;
    background-color: #000000;
    border-color: #00ff00;
}

.color-scheme-matrix {
    color: #00ff00;
    background-color: #000000;
    border-color: #00ff00;
}

.color-scheme-cyberpunk {
    color: #00ffff;
    background-color: #000022;
    border-color: #ff00ff;
}

.color-scheme-terminal {
    color: #00ff00;
    background-color: #000000;
    border-color: #00ff00;
}

.color-scheme-dark {
    color: #cccccc;
    background-color: #111111;
    border-color: #444444;
}

.color-scheme-neon {
    color: #ffffff;
    background-color: #0a0a1a;
    border-color: #00ffff;
    text-shadow: 0 0 10px currentColor;
}

/* ============================================================================
   ЭФФЕКТЫ ДЛЯ ТЕКСТА
   ============================================================================ */

.glow-effect {
    text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00;
}

.error-text {
    color: #ff0000;
    font-weight: bold;
    text-shadow: 0 0 5px #ff0000;
}

.success-text {
    color: #00ff00;
    font-weight: bold;
    text-shadow: 0 0 5px #00ff00;
}

.warning-text {
    color: #ffff00;
    font-weight: bold;
    text-shadow: 0 0 5px #ffff00;
}

.info-text {
    color: #00ffff;
    font-weight: bold;
    text-shadow: 0 0 5px #00ffff;
}

/* ============================================================================
   КОМПОНЕНТЫ ИГРЫ
   ============================================================================ */

/* Панель задач */
.task-panel {
    background-color: #0a0a1a;
    border: 2px solid #00bfff;
    border-radius: 8px;
}

.task-item {
    background-color: #001122;
    border: 1px solid #0088cc;
    border-radius: 5px;
    padding: 10px;
    margin: 5px;
}

.task-item-completed {
    background-color: #002200;
    border: 1px solid #00aa00;
    color: #00aa00;
}

.task-item-failed {
    background-color: #220000;
    border: 1px solid #aa0000;
    color: #ff5555;
}

/* Панель статистики */
.stats-panel {
    background-color: #0a0a0a;
    border: 2px solid #ffff00;
    border-radius: 8px;
}

.stat-item {
    padding: 5px;
    margin: 2px;
    border-bottom: 1px solid #333;
}

.stat-item:last-child {
    border-bottom: none;
}

.stat-name {
    color: #00ffff;
}

.stat-value {
    color: #ffff00;
    font-weight: bold;
}

/* Инвентарь */
.inventory-panel {
    background-color: #0a0a0a;
    border: 2px solid #ff8800;
    border-radius: 8px;
}

.inventory-item {
    background-color: #111100;
    border: 1px solid #ffaa00;
    border-radius: 5px;
    padding: 8px;
    margin: 3px;
}

/* Персонаж */
.character-panel {
    background-color: #0a0a0a;
    border: 2px solid #aa00aa;
    border-radius: 8px;
}

.stat-bar {
    background-color: #001100;
    border: 1px solid #00ff00;
    border-radius: 3px;
    height: 10px;
}

.stat-bar-fill {
    background-color: #00ff00;
    border-radius: 2px;
}

/* ============================================================================
   МЕДИА-ЗАПРОСЫ ДЛЯ АДАПТИВНОСТИ
   ============================================================================ */

@media (max-width: 800px) {
    .menu-button {
        font-size: 11px;
        padding: 6px 10px;
        min-height: 32px;
    }
    
    .game-title {
        font-size: 20px;
    }
    
    QTabBar::tab {
        padding: 4px 8px;
        font-size: 10px;
    }
    
    .time-hour, .time-minute {
        font-size: 18px;
    }
    
    .time-date {
        font-size: 11px;
    }
    
    .neon-header {
        font-size: 18px;
        letter-spacing: 2px;
    }
}

@media (max-width: 500px) {
    .menu-button {
        font-size: 10px;
        padding: 5px 8px;
        min-height: 30px;
    }
    
    .game-title {
        font-size: 18px;
    }
    
    QTabBar::tab {
        padding: 3px 6px;
        font-size: 9px;
    }
    
    .time-hour, .time-minute {
        font-size: 16px;
    }
    
    .time-date {
        font-size: 10px;
    }
    
    .neon-header {
        font-size: 16px;
        letter-spacing: 1px;
    }
}

/* ============================================================================
   СПЕЦИАЛЬНЫЕ ЭФФЕКТЫ
   ============================================================================ */

/* Эффект печатной машинки */
@keyframes typewriter {
    from { width: 0; }
    to { width: 100%; }
}

.typewriter {
    overflow: hidden;
    white-space: nowrap;
    animation: typewriter 3s steps(40, end);
}

/* Эффект загрузки */
@keyframes loading-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-spinner {
    border: 3px solid #00ff00;
    border-top: 3px solid transparent;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    animation: loading-spin 1s linear infinite;
}

/* Эффект глитча */
@keyframes glitch {
    0% {
        transform: translate(0);
    }
    20% {
        transform: translate(-2px, 2px);
    }
    40% {
        transform: translate(-2px, -2px);
    }
    60% {
        transform: translate(2px, 2px);
    }
    80% {
        transform: translate(2px, -2px);
    }
    100% {
        transform: translate(0);
    }
}

.glitch-effect {
    animation: glitch 0.3s infinite;
}

/* Эффект сканирования */
@keyframes scan-line {
    0% {
        transform: translateY(-100%);
    }
    100% {
        transform: translateY(100vh);
    }
}

.scan-line {
    position: absolute;
    width: 100%;
    height: 2px;
    background: linear-gradient(to bottom, transparent, #00ff00, transparent);
    animation: scan-line 2s linear infinite;
}

/* ============================================================================
   ВСПЛЫВАЮЩИЕ ПОДСКАЗКИ
   ============================================================================ */

QToolTip {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    border-radius: 3px;
    padding: 8px;
    font-size: 11px;
    max-width: 300px;
}

QToolTip[rich="true"] {
    background-color: #0a0a1a;
    border: 2px solid #00ffff;
    border-radius: 5px;
    padding: 12px;
    font-size: 12px;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

/* ============================================================================
   СТАТУСНЫЕ ИНДИКАТОРЫ
   ============================================================================ */

.status-online {
    color: #00ff00;
    font-weight: bold;
    text-shadow: 0 0 5px #00ff00;
}

.status-offline {
    color: #ff0000;
    font-weight: bold;
    text-shadow: 0 0 5px #ff0000;
}

.status-warning {
    color: #ffff00;
    font-weight: bold;
    text-shadow: 0 0 5px #ffff00;
}

.status-critical {
    color: #ff00ff;
    font-weight: bold;
    animation: blink 0.5s infinite;
}

/* ============================================================================
   ГРАДИЕНТНЫЕ ТЕКСТЫ
   ============================================================================ */

.gradient-text-cyber {
    background: linear-gradient(
        90deg,
        #ff0066,
        #ff9900,
        #ffff00,
        #00ff00,
        #00ffff,
        #0066ff
    );
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-weight: bold;
}

.gradient-text-neon {
    background: linear-gradient(
        90deg,
        #ff00ff,
        #00ffff,
        #ffff00
    );
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

/* ============================================================================
   ЗАВЕРШАЮЩИЕ СТИЛИ
   ============================================================================ */

/* Стили для печати */
@media print {
    QPushButton, QMenuBar, QToolBar {
        display: none;
    }
    
    QTextEdit {
        border: none;
        background-color: white;
        color: black;
    }
}

/* Отключение анимаций для пользователей с предпочтениями */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* ============================================================================
   СТИЛИ БРАУЗЕРА (НОВЫЕ ДОБАВЛЕНИЯ)
   ============================================================================ */

/* Главное окно браузера */
BrowserWindow {
    background-color: #0a0a1a;
    border: 3px solid #00bfff;
    border-radius: 10px;
}

/* Адресная строка браузера */
BrowserUrlBar {
    background-color: #1a1a2e;
    border-bottom: 2px solid #00bfff;
    padding: 5px;
}

BrowserUrlBar QPushButton {
    background-color: #2a2a3e;
    color: #cccccc;
    border: 2px solid #00bfff;
    border-radius: 5px;
    font-weight: bold;
    font-size: 14px;
    min-width: 30px;
    min-height: 30px;
}

BrowserUrlBar QPushButton:hover {
    background-color: #3a3a4e;
    border-color: #00ffff;
    color: #ffffff;
}

BrowserUrlBar QPushButton:pressed {
    background-color: #1a1a2e;
}

BrowserUrlBar QLineEdit {
    background-color: #000000;
    color: #00ffff;
    border: 2px solid #0088cc;
    border-radius: 5px;
    padding: 8px;
    font-family: 'Source Code Pro';
    font-size: 13px;
    selection-background-color: #0088cc;
}

BrowserUrlBar QLineEdit:focus {
    border: 2px solid #00ffff;
    background-color: #001122;
}

/* Область просмотра браузера */
BrowserView {
    background-color: #000000;
    color: #ffffff;
    border: none;
    font-family: Arial, sans-serif;
    font-size: 14px;
}

BrowserView QScrollBar:vertical {
    background: #1a1a2e;
    width: 14px;
    border-radius: 7px;
}

BrowserView QScrollBar::handle:vertical {
    background: #00bfff;
    min-height: 30px;
    border-radius: 7px;
}

BrowserView QScrollBar::handle:vertical:hover {
    background: #00ffff;
}

BrowserView a {
    color: #00ffff;
    text-decoration: none;
}

BrowserView a:hover {
    color: #ffff00;
    text-decoration: underline;
}

/* Кнопки на сайтах браузера */
.browser-button {
    background: linear-gradient(90deg, #00ff00, #00cc00);
    color: black;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
    font-size: 16px;
}

.browser-button:hover {
    background: linear-gradient(90deg, #00cc00, #009900);
    transform: scale(1.05);
}

.browser-button-danger {
    background: linear-gradient(90deg, #ff0000, #cc0000);
    color: white;
}

.browser-button-danger:hover {
    background: linear-gradient(90deg, #cc0000, #990000);
}

/* Карточки товаров в браузере */
.browser-product-card {
    background: #1a1a2e;
    border: 2px solid #00ffff;
    border-radius: 10px;
    padding: 15px;
    margin: 10px;
}

.browser-product-card:hover {
    border-color: #ffff00;
    box-shadow: 0 0 15px rgba(255, 255, 0, 0.3);
}

.browser-price-old {
    color: #ff4444;
    text-decoration: line-through;
    font-size: 14px;
}

.browser-price-new {
    color: #00ff00;
    font-size: 24px;
    font-weight: bold;
    text-shadow: 0 0 5px #00ff00;
}

.browser-discount {
    background: #ff0066;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    font-weight: bold;
    display: inline-block;
}

/* Формы в браузере */
.browser-form {
    background: rgba(0, 50, 100, 0.3);
    border: 2px solid #0088ff;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
}

.browser-form input {
    background: #002244;
    color: white;
    border: 1px solid #0088ff;
    border-radius: 5px;
    padding: 10px;
    width: 100%;
    margin: 8px 0;
}

.browser-form input:focus {
    border: 2px solid #00ffff;
    background: #003366;
}

.browser-form label {
    color: #aaddff;
    font-weight: bold;
    margin-top: 15px;
    display: block;
}

/* Предупреждения в браузере */
.browser-warning {
    background: rgba(255, 0, 0, 0.2);
    border: 2px solid #ff0000;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
    color: #ff8888;
}

.browser-warning h3 {
    color: #ff0000;
    margin-top: 0;
}

.browser-info {
    background: rgba(0, 255, 255, 0.1);
    border: 2px solid #00ffff;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
    color: #aaffff;
}

.browser-success {
    background: rgba(0, 255, 0, 0.1);
    border: 2px solid #00ff00;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
    color: #aaffaa;
}

/* Заголовки сайтов в браузере */
.browser-site-header {
    background: linear-gradient(90deg, #0066cc, #0099ff);
    color: white;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 25px;
    text-align: center;
    text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.browser-site-header h1 {
    font-size: 32px;
    margin: 0;
    color: white;
}

.browser-site-header p {
    font-size: 16px;
    margin: 10px 0 0 0;
    opacity: 0.9;
}

/* Сетка товаров/профилей в браузере */
.browser-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin: 25px 0;
}

/* Эффекты для браузера */
@keyframes browser-pulse {
    0% { opacity: 0.8; }
    50% { opacity: 1; }
    100% { opacity: 0.8; }
}

.browser-alert {
    animation: browser-pulse 2s infinite;
    background: #ff0000;
    color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    font-size: 18px;
}

/* Таймеры в браузере */
.browser-timer {
    font-size: 36px;
    color: #ffff00;
    text-align: center;
    font-family: 'Source Code Pro', monospace;
    text-shadow: 0 0 10px #ffff00;
    background: rgba(0, 0, 0, 0.5);
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #ffff00;
}

/* Модальные окна в браузере */
.browser-modal {
    background: #0a0a2a;
    border: 3px solid #00ffff;
    border-radius: 15px;
    padding: 30px;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1000;
    box-shadow: 0 0 50px rgba(0, 255, 255, 0.5);
}

.browser-modal-overlay {
    background: rgba(0, 0, 0, 0.7);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 999;
}

/* Статус бар браузера */
BrowserStatusBar {
    background-color: #1a1a2e;
    color: #00ffff;
    font-family: 'Source Code Pro';
    font-size: 11px;
}

/* Кнопки навигации браузера */
.browser-nav-button {
    background-color: #2a2a3e;
    color: #cccccc;
    border: 2px solid #00bfff;
    border-radius: 5px;
    padding: 8px;
    font-weight: bold;
    font-size: 14px;
    min-width: 40px;
    min-height: 30px;
}

.browser-nav-button:hover {
    background-color: #3a3a4e;
    border-color: #00ffff;
    color: #ffffff;
}

.browser-nav-button:disabled {
    background-color: #1a1a1a;
    border-color: #555555;
    color: #777777;
}

/* Панель закладок браузера */
.browser-bookmarks-bar {
    background-color: #1a1a2e;
    border-bottom: 1px solid #00bfff;
    padding: 5px;
}

.browser-bookmark {
    background-color: #2a2a3e;
    color: #cccccc;
    border: 1px solid #0088cc;
    border-radius: 3px;
    padding: 4px 8px;
    margin: 0 2px;
    font-size: 11px;
}

.browser-bookmark:hover {
    background-color: #3a3a4e;
    border-color: #00ffff;
    color: #ffffff;
}

/* Индикатор безопасности браузера */
.browser-security-indicator {
    color: #00ff00;
    font-weight: bold;
    font-size: 12px;
}

.browser-security-indicator.insecure {
    color: #ff0000;
}

.browser-security-indicator.warning {
    color: #ffff00;
}

/* Адаптивность браузера */
@media (max-width: 800px) {
    .browser-site-header h1 {
        font-size: 24px;
    }
    
    .browser-grid {
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 15px;
    }
    
    .browser-button {
        padding: 10px 20px;
        font-size: 14px;
    }
    
    .browser-nav-button {
        min-width: 35px;
        min-height: 25px;
        font-size: 12px;
    }
}

@media (max-width: 500px) {
    .browser-site-header {
        padding: 15px;
    }
    
    .browser-site-header h1 {
        font-size: 20px;
    }
    
    .browser-grid {
        grid-template-columns: 1fr;
    }
    
    .browser-form {
        padding: 15px;
    }
    
    .browser-nav-button {
        min-width: 30px;
        min-height: 20px;
        font-size: 10px;
        padding: 4px;
    }
}

/* Анимации для браузера */
@keyframes browser-loading {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.browser-loading-spinner {
    border: 3px solid #00bfff;
    border-top: 3px solid transparent;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: browser-loading 1s linear infinite;
}

/* Эффект печати в браузере */
.browser-typewriter {
    overflow: hidden;
    white-space: nowrap;
    animation: typewriter 2s steps(30, end);
    font-family: 'Courier New', monospace;
}

/* Подсветка кода в браузере */
.browser-code {
    background-color: #001122;
    border: 1px solid #0088cc;
    border-radius: 5px;
    padding: 15px;
    font-family: 'Source Code Pro', monospace;
    font-size: 12px;
    color: #00ffff;
    overflow-x: auto;
}

/* Таблицы в браузере */
.browser-table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}

.browser-table th {
    background-color: #002244;
    color: #00ffff;
    padding: 10px;
    border: 1px solid #0088cc;
    text-align: left;
}

.browser-table td {
    background-color: #001122;
    color: #cccccc;
    padding: 8px;
    border: 1px solid #0088cc;
}

.browser-table tr:hover td {
    background-color: #002244;
}

/* Панель инструментов браузера */
.browser-toolbar {
    background-color: #1a1a2e;
    border-bottom: 2px solid #00bfff;
    padding: 8px;
    display: flex;
    gap: 10px;
}

.browser-toolbar-button {
    background-color: #2a2a3e;
    color: #cccccc;
    border: 1px solid #0088cc;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 12px;
    cursor: pointer;
}

.browser-toolbar-button:hover {
    background-color: #3a3a4e;
    border-color: #00ffff;
    color: #ffffff;
}

.browser-toolbar-button.active {
    background-color: #0088cc;
    border-color: #00ffff;
    color: #ffffff;
}

/* Панель вкладок браузера */
.browser-tab-bar {
    background-color: #1a1a2e;
    border-bottom: 2px solid #00bfff;
    padding: 5px 5px 0 5px;
    display: flex;
    overflow-x: auto;
}

.browser-tab {
    background-color: #2a2a3e;
    color: #cccccc;
    border: 1px solid #0088cc;
    border-bottom: none;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    padding: 8px 15px;
    margin-right: 2px;
    font-size: 12px;
    white-space: nowrap;
    cursor: pointer;
}

.browser-tab:hover {
    background-color: #3a3a4e;
    border-color: #00ffff;
    color: #ffffff;
}

.browser-tab.active {
    background-color: #0088cc;
    border-color: #00ffff;
    color: #ffffff;
    font-weight: bold;
}

.browser-tab-close {
    margin-left: 8px;
    color: #ff8888;
    font-weight: bold;
    cursor: pointer;
}

.browser-tab-close:hover {
    color: #ff0000;
}

/* Контекстное меню браузера */
.browser-context-menu {
    background-color: #1a1a2e;
    border: 2px solid #00bfff;
    border-radius: 5px;
    padding: 5px;
    min-width: 150px;
}

.browser-context-menu-item {
    padding: 8px 12px;
    color: #cccccc;
    font-size: 12px;
    cursor: pointer;
}

.browser-context-menu-item:hover {
    background-color: #2a2a3e;
    color: #ffffff;
}

.browser-context-menu-separator {
    height: 1px;
    background-color: #00bfff;
    margin: 5px 0;
}

/* Панель загрузок браузера */
.browser-downloads-panel {
    background-color: #0a0a1a;
    border: 2px solid #00bfff;
    border-radius: 8px;
    padding: 15px;
}

.browser-download-item {
    background-color: #1a1a2e;
    border: 1px solid #0088cc;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
}

.browser-download-progress {
    background-color: #001122;
    height: 10px;
    border-radius: 5px;
    margin-top: 5px;
    overflow: hidden;
}

.browser-download-progress-bar {
    background-color: #00bfff;
    height: 100%;
    border-radius: 5px;
}

/* Панель истории браузера */
.browser-history-panel {
    background-color: #0a0a1a;
    border: 2px solid #00bfff;
    border-radius: 8px;
    padding: 15px;
}

.browser-history-item {
    background-color: #1a1a2e;
    border: 1px solid #0088cc;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 5px;
    cursor: pointer;
}

.browser-history-item:hover {
    background-color: #2a2a3e;
    border-color: #00ffff;
}

/* Панель настроек браузера */
.browser-settings-panel {
    background-color: #0a0a1a;
    border: 2px solid #00bfff;
    border-radius: 8px;
    padding: 20px;
}

.browser-settings-category {
    background-color: #1a1a2e;
    border: 1px solid #0088cc;
    border-radius: 5px;
    padding: 15px;
    margin-bottom: 15px;
}

.browser-settings-title {
    color: #00ffff;
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 10px;
}

.browser-settings-option {
    margin-bottom: 10px;
}

.browser-settings-label {
    color: #cccccc;
    font-size: 13px;
    margin-bottom: 5px;
}

/* Уведомления браузера */
.browser-notification {
    background-color: #1a1a2e;
    border: 2px solid #00bfff;
    border-radius: 8px;
    padding: 15px;
    position: fixed;
    bottom: 20px;
    right: 20px;
    max-width: 300px;
    z-index: 1000;
    box-shadow: 0 0 20px rgba(0, 191, 255, 0.5);
}

.browser-notification-title {
    color: #00ffff;
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 5px;
}

.browser-notification-message {
    color: #cccccc;
    font-size: 12px;
}

.browser-notification-close {
    position: absolute;
    top: 5px;
    right: 5px;
    color: #ff8888;
    cursor: pointer;
    font-weight: bold;
}

.browser-notification-close:hover {
    color: #ff0000;
}

/* Всплывающие окна браузера */
.browser-popup {
    background-color: #0a0a1a;
    border: 3px solid #00bfff;
    border-radius: 10px;
    padding: 20px;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1001;
    box-shadow: 0 0 30px rgba(0, 191, 255, 0.7);
    min-width: 300px;
    max-width: 500px;
}

.browser-popup-overlay {
    background-color: rgba(0, 0, 0, 0.7);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
}

/* Полоса прокрутки браузера (кастомизация) */
.browser-scrollbar:vertical {
    background-color: #1a1a2e;
    width: 12px;
    border-radius: 6px;
}

.browser-scrollbar::handle:vertical {
    background-color: #00bfff;
    border-radius: 6px;
    min-height: 30px;
}

.browser-scrollbar::handle:vertical:hover {
    background-color: #00ffff;
}

.browser-scrollbar::add-line:vertical,
.browser-scrollbar::sub-line:vertical {
    background-color: #1a1a2e;
}

.browser-scrollbar:horizontal {
    background-color: #1a1a2e;
    height: 12px;
    border-radius: 6px;
}

.browser-scrollbar::handle:horizontal {
    background-color: #00bfff;
    border-radius: 6px;
    min-width: 30px;
}

.browser-scrollbar::handle:horizontal:hover {
    background-color: #00ffff;
}

/* Стили для темной темы браузера */
.browser-dark-theme {
    background-color: #000000;
    color: #ffffff;
}

.browser-dark-theme a {
    color: #00ffff;
}

.browser-dark-theme a:hover {
    color: #ffff00;
}

/* Стили для светлой темы браузера */
.browser-light-theme {
    background-color: #ffffff;
    color: #000000;
}

.browser-light-theme a {
    color: #0066cc;
}

.browser-light-theme a:hover {
    color: #ff6600;
}

/* Стили для высокой контрастности */
.browser-high-contrast {
    background-color: #000000;
    color: #ffff00;
}

.browser-high-contrast a {
    color: #00ffff;
    text-decoration: underline;
}

.browser-high-contrast a:hover {
    color: #ff00ff;
}

/* Стили для режима чтения */
.browser-reading-mode {
    background-color: #f5f5dc;
    color: #000000;
    font-family: 'Georgia', serif;
    font-size: 18px;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
    padding: 40px;
}

.browser-reading-mode h1,
.browser-reading-mode h2,
.browser-reading-mode h3 {
    color: #333333;
    font-family: 'Times New Roman', serif;
}

/* Индикатор загрузки страницы */
.browser-page-loading {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: #00bfff;
    animation: browser-loading-progress 2s linear infinite;
}

@keyframes browser-loading-progress {
    0% { width: 0%; }
    50% { width: 70%; }
    100% { width: 100%; }
}

/* Эффект фокуса для элементов браузера */
.browser-focus-effect:focus {
    outline: 2px solid #00ffff;
    outline-offset: 2px;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

/* Эффект выделения текста в браузере */
.browser-selection {
    background-color: #00bfff;
    color: #000000;
}

/* Эффект наведения на интерактивные элементы */
.browser-hover-effect:hover {
    transform: translateY(-2px);
    transition: transform 0.2s ease;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

/* Анимация появления элементов браузера */
@keyframes browser-fade-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.browser-fade-in {
    animation: browser-fade-in 0.3s ease;
}

/* Анимация исчезновения элементов браузера */
@keyframes browser-fade-out {
    from { opacity: 1; transform: translateY(0); }
    to { opacity: 0; transform: translateY(10px); }
}

.browser-fade-out {
    animation: browser-fade-out 0.3s ease;
}

/* Эффект пульсации для важных элементов */
@keyframes browser-important-pulse {
    0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(255, 0, 0, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
}

.browser-important-pulse {
    animation: browser-important-pulse 1.5s infinite;
}

/* Эффект мигания для срочных уведомлений */
@keyframes browser-blink-alert {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.browser-blink-alert {
    animation: browser-blink-alert 1s infinite;
}

/* Градиентные фоны для браузера */
.browser-gradient-bg-cyber {
    background: linear-gradient(135deg, #000022, #220044, #000022);
}

.browser-gradient-bg-matrix {
    background: linear-gradient(135deg, #001100, #003300, #001100);
}

.browser-gradient-bg-neon {
    background: linear-gradient(135deg, #0a0a1a, #1a0a2a, #0a1a1a);
}

/* Стили для разделителей в браузере */
.browser-divider {
    height: 1px;
    background: linear-gradient(90deg, 
        transparent, 
        #00bfff, 
        #00ffff, 
        #00bfff, 
        transparent);
    margin: 20px 0;
}

/* Стили для иконок в браузере */
.browser-icon {
    width: 24px;
    height: 24px;
    display: inline-block;
    vertical-align: middle;
    margin-right: 8px;
}

.browser-icon-home { background-color: #00bfff; }
.browser-icon-back { background-color: #0088cc; }
.browser-icon-forward { background-color: #0088cc; }
.browser-icon-reload { background-color: #00cc00; }
.browser-icon-download { background-color: #ff9900; }
.browser-icon-bookmark { background-color: #ff00ff; }
.browser-icon-history { background-color: #9900ff; }
.browser-icon-settings { background-color: #cccccc; }
.browser-icon-close { background-color: #ff4444; }

/* Стили для бейджей в браузере */
.browser-badge {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 10px;
    font-size: 10px;
    font-weight: bold;
    margin-left: 5px;
    vertical-align: super;
}

.browser-badge-new {
    background-color: #ff0000;
    color: #ffffff;
}

.browser-badge-update {
    background-color: #ff9900;
    color: #000000;
}

.browser-badge-beta {
    background-color: #00cc00;
    color: #000000;
}

.browser-badge-premium {
    background-color: #ff00ff;
    color: #ffffff;
}

/* Стили для подсказок в браузере */
.browser-tooltip {
    background-color: #0a0a1a;
    color: #00ffff;
    border: 1px solid #00bfff;
    border-radius: 5px;
    padding: 8px;
    font-size: 11px;
    max-width: 250px;
    box-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
}

/* Стили для счетчиков в браузере */
.browser-counter {
    display: inline-block;
    min-width: 20px;
    height: 20px;
    line-height: 20px;
    text-align: center;
    background-color: #ff0000;
    color: #ffffff;
    border-radius: 10px;
    font-size: 11px;
    font-weight: bold;
    margin-left: 5px;
}

/* Стили для аватаров в браузере */
.browser-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid #00bfff;
    overflow: hidden;
}

.browser-avatar-small {
    width: 24px;
    height: 24px;
}

.browser-avatar-large {
    width: 60px;
    height: 60px;
}

/* Стили для рейтингов в браузере */
.browser-rating {
    color: #ff9900;
    font-size: 16px;
}

.browser-rating-star {
    display: inline-block;
    margin-right: 2px;
}

/* Стили для тегов в браузере */
.browser-tag {
    display: inline-block;
    padding: 3px 8px;
    background-color: #1a1a2e;
    color: #cccccc;
    border: 1px solid #0088cc;
    border-radius: 12px;
    font-size: 11px;
    margin: 2px;
}

.browser-tag:hover {
    background-color: #2a2a3e;
    border-color: #00ffff;
    color: #ffffff;
}

/* Стили для хлебных крошек в браузере */
.browser-breadcrumb {
    font-size: 12px;
    color: #cccccc;
    margin-bottom: 10px;
}

.browser-breadcrumb-item {
    color: #00ffff;
    text-decoration: none;
}

.browser-breadcrumb-item:hover {
    color: #ffff00;
    text-decoration: underline;
}

.browser-breadcrumb-separator {
    margin: 0 5px;
    color: #888888;
}

/* Стили для постраничной навигации в браузере */
.browser-pagination {
    display: flex;
    justify-content: center;
    margin: 20px 0;
}

.browser-page-link {
    padding: 5px 10px;
    margin: 0 2px;
    background-color: #1a1a2e;
    color: #cccccc;
    border: 1px solid #0088cc;
    border-radius: 3px;
    text-decoration: none;
}

.browser-page-link:hover {
    background-color: #2a2a3e;
    border-color: #00ffff;
    color: #ffffff;
}

.browser-page-link.active {
    background-color: #0088cc;
    border-color: #00ffff;
    color: #ffffff;
    font-weight: bold;
}

/* Стили для выпадающих списков в браузере */
.browser-dropdown {
    background-color: #1a1a2e;
    border: 1px solid #0088cc;
    border-radius: 5px;
    padding: 8px;
    color: #cccccc;
    font-size: 12px;
    min-width: 150px;
}

.browser-dropdown:hover {
    border-color: #00ffff;
}

.browser-dropdown-option {
    padding: 8px;
    cursor: pointer;
}

.browser-dropdown-option:hover {
    background-color: #2a2a3e;
    color: #ffffff;
}

/* Стили для переключателей в браузере */
.browser-switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 24px;
}

.browser-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.browser-switch-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #2a2a3e;
    border: 1px solid #0088cc;
    border-radius: 24px;
    transition: .4s;
}

.browser-switch-slider:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 4px;
    bottom: 3px;
    background-color: #cccccc;
    border-radius: 50%;
    transition: .4s;
}

.browser-switch input:checked + .browser-switch-slider {
    background-color: #0088cc;
    border-color: #00ffff;
}

.browser-switch input:checked + .browser-switch-slider:before {
    transform: translateX(26px);
    background-color: #ffffff;
}

/* Стили для ползунков в браузере */
.browser-slider {
    -webkit-appearance: none;
    width: 100%;
    height: 8px;
    background: #1a1a2e;
    border: 1px solid #0088cc;
    border-radius: 4px;
    outline: none;
}

.browser-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px;
    height: 20px;
    background: #00bfff;
    border: 1px solid #00ffff;
    border-radius: 50%;
    cursor: pointer;
}

.browser-slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: #00bfff;
    border: 1px solid #00ffff;
    border-radius: 50%;
    cursor: pointer;
}

/* Стили для индикатора выполнения в браузере */
.browser-progress {
    width: 100%;
    height: 20px;
    background-color: #1a1a2e;
    border: 1px solid #0088cc;
    border-radius: 10px;
    overflow: hidden;
}

.browser-progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #0088cc, #00bfff, #00ffff);
    border-radius: 10px;
    transition: width 0.3s ease;
}

/* Стили для индикатора загрузки контента */
.browser-content-loading {
    text-align: center;
    padding: 40px;
    color: #00ffff;
}

.browser-content-loading-spinner {
    border: 4px solid #1a1a2e;
    border-top: 4px solid #00bfff;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: browser-loading 1s linear infinite;
    margin: 0 auto 20px;
}

/* Стили для сообщений об ошибках в браузере */
.browser-error-message {
    background-color: rgba(255, 0, 0, 0.1);
    border: 2px solid #ff0000;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    color: #ff8888;
}

.browser-error-code {
    font-family: 'Source Code Pro', monospace;
    background-color: #000000;
    padding: 10px;
    border-radius: 5px;
    margin-top: 10px;
    overflow-x: auto;
}

/* Стили для сообщений об успехе в браузере */
.browser-success-message {
    background-color: rgba(0, 255, 0, 0.1);
    border: 2px solid #00ff00;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    color: #88ff88;
}

/* Стили для информационных сообщений в браузере */
.browser-info-message {
    background-color: rgba(0, 191, 255, 0.1);
    border: 2px solid #00bfff;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    color: #88ccff;
}

/* Стили для предупреждений в браузере */
.browser-caution-message {
    background-color: rgba(255, 255, 0, 0.1);
    border: 2px solid #ffff00;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    color: #ffff88;
}

/* Стили для отключенных элементов в браузере */
.browser-disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
}

/* Стили для скрытых элементов в браузере */
.browser-hidden {
    display: none !important;
}

/* Стили для видимых элементов в браузере */
.browser-visible {
    display: block !important;
}

/* Стили для элементов, требующих внимания */
.browser-attention-required {
    border: 2px solid #ff0000 !important;
    animation: browser-blink-alert 1s infinite;
}

/* Стили для элементов, помеченных как важные */
.browser-important {
    font-weight: bold;
    color: #ff0000;
}

/* Стили для элементов, помеченных как новые */
.browser-new {
    position: relative;
}

.browser-new::after {
    content: "NEW";
    position: absolute;
    top: -5px;
    right: -5px;
    background-color: #ff0000;
    color: #ffffff;
    font-size: 8px;
    padding: 2px 4px;
    border-radius: 3px;
    font-weight: bold;
}

/* Стили для элементов, помеченных как обновленные */
.browser-updated {
    position: relative;
}

.browser-updated::after {
    content: "UPDATED";
    position: absolute;
    top: -5px;
    right: -5px;
    background-color: #ff9900;
    color: #000000;
    font-size: 8px;
    padding: 2px 4px;
    border-radius: 3px;
    font-weight: bold;
}

/* Стили для элементов, помеченных как популярные */
.browser-popular {
    position: relative;
}

.browser-popular::after {
    content: "HOT";
    position: absolute;
    top: -5px;
    right: -5px;
    background-color: #ff00ff;
    color: #ffffff;
    font-size: 8px;
    padding: 2px 4px;
    border-radius: 3px;
    font-weight: bold;
}

/* Стили для элементов с ограниченным доступом */
.browser-restricted {
    opacity: 0.7;
    position: relative;
}

.browser-restricted::before {
    content: "🔒";
    position: absolute;
    top: 5px;
    right: 5px;
    font-size: 12px;
}

/* Стили для элементов с премиум доступом */
.browser-premium {
    position: relative;
    border: 2px solid #ffd700 !important;
}

.browser-premium::before {
    content: "⭐";
    position: absolute;
    top: 5px;
    right: 5px;
    font-size: 12px;
}

/* Стили для анимированных фонов браузера */
.browser-animated-bg-matrix {
    background: linear-gradient(135deg, #001100, #003300, #001100);
    background-size: 400% 400%;
    animation: browser-gradient-matrix 10s ease infinite;
}

@keyframes browser-gradient-matrix {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.browser-animated-bg-cyber {
    background: linear-gradient(135deg, #000022, #220044, #000022);
    background-size: 400% 400%;
    animation: browser-gradient-cyber 10s ease infinite;
}

@keyframes browser-gradient-cyber {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.browser-animated-bg-neon {
    background: linear-gradient(135deg, #0a0a1a, #1a0a2a, #0a1a1a);
    background-size: 400% 400%;
    animation: browser-gradient-neon 10s ease infinite;
}

@keyframes browser-gradient-neon {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Стили для эффекта параллакса в браузере */
.browser-parallax-container {
    position: relative;
    overflow: hidden;
    height: 300px;
}

.browser-parallax-layer {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.browser-parallax-background {
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect width="100" height="100" fill="%23001122"/><circle cx="20" cy="20" r="2" fill="%2300bfff" opacity="0.5"/><circle cx="50" cy="40" r="3" fill="%2300ffff" opacity="0.5"/><circle cx="80" cy="60" r="2" fill="%230088cc" opacity="0.5"/></svg>');
    background-size: 100px 100px;
    transform: translateZ(-1px) scale(2);
}

/* Стили для эффекта стекла (glassmorphism) в браузере */
.browser-glass-effect {
    background: rgba(26, 26, 46, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 191, 255, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Стили для эффекта неона в браузере */
.browser-neon-text {
    color: #ffffff;
    text-shadow: 
        0 0 5px currentColor,
        0 0 10px currentColor,
        0 0 15px currentColor,
        0 0 20px currentColor;
}

.browser-neon-border {
    border: 2px solid #00ffff;
    box-shadow: 
        0 0 5px #00ffff,
        0 0 10px #00ffff,
        0 0 15px #00ffff inset;
}

/* Стили для эффекта голограммы в браузере */
.browser-hologram-effect {
    background: linear-gradient(
        to bottom,
        transparent,
        rgba(0, 255, 255, 0.1) 20%,
        rgba(0, 255, 255, 0.3) 50%,
        rgba(0, 255, 255, 0.1) 80%,
        transparent
    );
    background-size: 100% 200%;
    animation: hologram-scan 3s linear infinite;
    border: 1px solid rgba(0, 255, 255, 0.5);
}

/* Стили для эффекта киберпанк в браузере */
.browser-cyberpunk-effect {
    background: linear-gradient(135deg, #000022, #220044);
    border: 2px solid #ff00ff;
    box-shadow: 
        0 0 10px #ff00ff,
        0 0 20px #ff00ff,
        0 0 30px #ff00ff inset;
    position: relative;
    overflow: hidden;
}

.browser-cyberpunk-effect::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        45deg,
        transparent 30%,
        rgba(255, 0, 255, 0.1) 50%,
        transparent 70%
    );
    animation: browser-cyber-scan 2s linear infinite;
}

@keyframes browser-cyber-scan {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

/* Стили для эффекта терминала в браузере */
.browser-terminal-effect {
    background-color: #000000;
    color: #00ff00;
    font-family: 'Source Code Pro', monospace;
    border: 3px solid #00ff00;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
    position: relative;
}

.browser-terminal-effect::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, 
        transparent, 
        #00ff00, 
        transparent);
    animation: browser-terminal-scan 2s linear infinite;
}

@keyframes browser-terminal-scan {
    0% { top: 0; }
    100% { top: 100%; }
}

/* Стили для эффекта глитча в браузере */
.browser-glitch-effect {
    position: relative;
}

.browser-glitch-effect::before,
.browser-glitch-effect::after {
    content: attr(data-text);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.browser-glitch-effect::before {
    left: 2px;
    text-shadow: -2px 0 #ff00ff;
    clip: rect(24px, 550px, 90px, 0);
    animation: browser-glitch-anim 5s infinite linear alternate-reverse;
}

.browser-glitch-effect::after {
    left: -2px;
    text-shadow: -2px 0 #00ffff;
    clip: rect(85px, 550px, 140px, 0);
    animation: browser-glitch-anim2 5s infinite linear alternate-reverse;
}

@keyframes browser-glitch-anim {
    0% { clip: rect(42px, 9999px, 44px, 0); }
    5% { clip: rect(12px, 9999px, 59px, 0); }
    10% { clip: rect(48px, 9999px, 29px, 0); }
    15% { clip: rect(42px, 9999px, 73px, 0); }
    20% { clip: rect(63px, 9999px, 27px, 0); }
    25% { clip: rect(34px, 9999px, 55px, 0); }
    30% { clip: rect(86px, 9999px, 73px, 0); }
    35% { clip: rect(20px, 9999px, 20px, 0); }
    40% { clip: rect(26px, 9999px, 60px, 0); }
    45% { clip: rect(25px, 9999px, 66px, 0); }
    50% { clip: rect(57px, 9999px, 98px, 0); }
    55% { clip: rect(5px, 9999px, 46px, 0); }
    60% { clip: rect(82px, 9999px, 31px, 0); }
    65% { clip: rect(54px, 9999px, 27px, 0); }
    70% { clip: rect(28px, 9999px, 99px, 0); }
    75% { clip: rect(45px, 9999px, 69px, 0); }
    80% { clip: rect(23px, 9999px, 85px, 0); }
    85% { clip: rect(54px, 9999px, 84px, 0); }
    90% { clip: rect(45px, 9999px, 47px, 0); }
    95% { clip: rect(37px, 9999px, 20px, 0); }
    100% { clip: rect(4px, 9999px, 91px, 0); }
}

@keyframes browser-glitch-anim2 {
    0% { clip: rect(65px, 9999px, 100px, 0); }
    5% { clip: rect(52px, 9999px, 74px, 0); }
    10% { clip: rect(79px, 9999px, 85px, 0); }
    15% { clip: rect(75px, 9999px, 5px, 0); }
    20% { clip: rect(67px, 9999px, 61px, 0); }
    25% { clip: rect(14px, 9999px, 79px, 0); }
    30% { clip: rect(1px, 9999px, 66px, 0); }
    35% { clip: rect(86px, 9999px, 30px, 0); }
    40% { clip: rect(23px, 9999px, 98px, 0); }
    45% { clip: rect(85px, 9999px, 72px, 0); }
    50% { clip: rect(71px, 9999px, 75px, 0); }
    55% { clip: rect(2px, 9999px, 48px, 0); }
    60% { clip: rect(30px, 9999px, 16px, 0); }
    65% { clip: rect(59px, 9999px, 50px, 0); }
    70% { clip: rect(41px, 9999px, 62px, 0); }
    75% { clip: rect(2px, 9999px, 82px, 0); }
    80% { clip: rect(47px, 9999px, 73px, 0); }
    85% { clip: rect(3px, 9999px, 27px, 0); }
    90% { clip: rect(40px, 9999px, 86px, 0); }
    95% { clip: rect(45px, 9999px, 77px, 0); }
    100% { clip: rect(19px, 9999px, 29px, 0); }
}

/* ФИНАЛЬНЫЕ СТИЛИ ДЛЯ БРАУЗЕРА - ОБЕСПЕЧИВАЮТ ПОЛНУЮ ИНТЕГРАЦИЮ С ИГРОЙ */

/* Соответствие цветовой схеме игры */
.browser-integrated {
    background-color: #0a0a0a;
    color: #00ff00;
    border-color: #00ff00;
    font-family: 'Source Code Pro', monospace;
}

/* Эффекты, соответствующие игре */
.browser-game-effect {
    text-shadow: 0 0 5px #00ff00;
    box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
}

/* Анимации, соответствующие игре */
.browser-game-animation {
    animation: time-blink 1s infinite;
}

/* Стили для соответствия тематике игры */
.browser-game-theme {
    background: linear-gradient(135deg, #000000, #001100);
    border: 2px solid #00ff00;
    color: #00ff00;
    font-family: 'Source Code Pro', monospace;
}

/* Эффект сканирования как в игре */
.browser-game-scanline {
    position: relative;
    overflow: hidden;
}

.browser-game-scanline::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, 
        transparent, 
        #00ff00, 
        transparent);
    animation: browser-game-scan 2s linear infinite;
}

@keyframes browser-game-scan {
    0% { top: 0; }
    100% { top: 100%; }
}

/* Эффект свечения как в игре */
.browser-game-glow {
    text-shadow: 
        0 0 5px #00ff00,
        0 0 10px #00ff00,
        0 0 15px #00ff00;
    animation: browser-game-glow-pulse 2s infinite;
}

@keyframes browser-game-glow-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

/* Стили для кнопок, соответствующие игре */
.browser-game-button {
    background-color: #002200;
    color: #00ff00;
    border: 2px solid #00ff00;
    padding: 8px 12px;
    font-weight: bold;
    border-radius: 4px;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: 'Source Code Pro', monospace;
}

.browser-game-button:hover {
    background-color: #004400;
    border-color: #00ff00;
    color: #ffffff;
    border-width: 3px;
}

/* Стили для полей ввода, соответствующие игре */
.browser-game-input {
    background-color: #001100;
    color: #00ff00;
    border: 2px solid #00ff00;
    padding: 8px;
    border-radius: 4px;
    font-size: 12px;
    font-family: 'Source Code Pro', monospace;
}

.browser-game-input:focus {
    border: 2px solid #00ffff;
    background-color: #002200;
    color: #ffffff;
}

/* Стили для панелей, соответствующие игре */
.browser-game-panel {
    background-color: #0a0a0a;
    border: 1px solid #00ff00;
    border-radius: 5px;
    padding: 10px;
}

/* Стили для заголовков, соответствующие игре */
.browser-game-header {
    color: #00bfff;
    font-size: 24px;
    font-weight: bold;
    text-shadow: 0 0 10px #00bfff;
    font-family: 'Source Code Pro', monospace;
}

/* Полная интеграция стилей браузера с игрой завершена */
"""