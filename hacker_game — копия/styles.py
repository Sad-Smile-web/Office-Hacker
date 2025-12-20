# styles.py
STYLES = """
/* styles.py - Полный файл стилей для "Офисный Хакер" */

/* Основные стили для приложения */
QMainWindow {
    background-color: #000000;
    border: 1px solid #00ff00;
}

QWidget {
    color: #00ff00;
    font-family: 'Source Code Pro', monospace;
    background-color: transparent;
}

/* Стили для кнопок */
QPushButton {
    background-color: #002200;
    color: #00ff00;
    border: 1px solid #00ff00;
    padding: 5px;
    font-weight: bold;
    border-radius: 3px;
}

QPushButton:hover {
    background-color: #004400;
    border-color: #00ff00;
}

QPushButton:pressed {
    background-color: #001100;
    border-color: #00aa00;
}

QPushButton:disabled {
    background-color: #001100;
    color: #008800;
    border-color: #008800;
}

/* Стили для текстовых полей */
QLineEdit {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    padding: 5px;
    border-radius: 3px;
}

QLineEdit:focus {
    border: 1px solid #00ff00;
    background-color: #002200;
}

QTextEdit {
    background-color: #000000;
    color: #00ff00;
    border: 1px solid #00ff00;
    padding: 5px;
    border-radius: 3px;
}

QTextEdit:focus {
    border: 1px solid #00ff00;
}

/* Стили для меток */
QLabel {
    color: #00ff00;
    background-color: transparent;
}

QLabel[important="true"] {
    color: #ffff00;
    font-weight: bold;
}

QLabel[title="true"] {
    color: #00bfff;
    font-size: 24px;
    font-weight: bold;
}

/* Стили для фреймов */
QFrame {
    border: 1px solid #00ff00;
    border-radius: 5px;
    background-color: #0a0a0a;
}

QFrame[flat="true"] {
    border: none;
    background-color: transparent;
}

/* Стили для полос прокрутки */
QScrollBar:vertical {
    background: #001100;
    width: 15px;
    border-radius: 7px;
}

QScrollBar::handle:vertical {
    background: #00aa00;
    min-height: 20px;
    border-radius: 7px;
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
    height: 15px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background: #00aa00;
    min-width: 20px;
    border-radius: 7px;
}

/* Стили для слайдеров */
QSlider::groove:horizontal {
    border: 1px solid #00ff00;
    height: 8px;
    background: #001100;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: #00ff00;
    width: 18px;
    margin: -5px 0;
    border-radius: 9px;
}

/* Стили для меню */
QMenuBar {
    background-color: #001100;
    color: #00ff00;
    border-bottom: 1px solid #00ff00;
}

QMenuBar::item:selected {
    background-color: #003300;
}

QMenu {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    padding: 5px;
}

QMenu::item:selected {
    background-color: #003300;
}

QMenu::separator {
    height: 1px;
    background-color: #00ff00;
    margin: 5px 0;
}

/* Специальные классы виджетов */
TerminalWidget {
    background-color: #000000;
    border: 2px solid #00ff00;
}

TerminalWidget QTextEdit {
    border: none;
}

TerminalWidget QLineEdit {
    border-left: none;
    border-right: none;
    border-bottom: none;
}

OfficeView {
    background-color: #101020;
    border: 2px solid #00ff00;
    border-radius: 5px;
}

/* Стили для кастомизированных классов */
.title {
    font-size: 18px;
    font-weight: bold;
    color: #00ff00;
    text-decoration: underline;
}

.glow-effect {
    text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00;
}

.error {
    color: #ff0000;
    font-weight: bold;
}

.success {
    color: #00ff00;
    font-weight: bold;
}

.warning {
    color: #ffff00;
    font-weight: bold;
}

.security-log {
    background-color: #000000;
    color: #ff0000;
    font-family: 'Courier New', monospace;
    font-size: 10px;
    border: 1px solid #ff0000;
}

/* Анимации */
@keyframes blink {
    0% { color: #ff0000; }
    50% { color: #880000; }
    100% { color: #ff0000; }
}

.blink {
    animation: blink 1s infinite;
}

@keyframes pulse {
    0% { opacity: 0.7; }
    50% { opacity: 1; }
    100% { opacity: 0.7; }
}

.pulse {
    animation: pulse 2s infinite;
}

/* Стили для меню кнопок */
.menu-button {
    background-color: #003300;
    color: #00ff00;
    border: 2px solid #00ff00;
    padding: 10px;
    font-size: 14px;
    font-weight: bold;
    min-height: 40px;
    border-radius: 5px;
    text-align: center;
}

.menu-button:hover {
    background-color: #005500;
    border-color: #ffff00;
    color: #ffff00;
}

.menu-button:pressed {
    background-color: #001100;
}

.game-title {
    font-size: 36px;
    font-weight: bold;
    color: #00ff00;
    text-shadow: 0 0 10px #00ff00;
    letter-spacing: 2px;
}

/* Стили для статусной строки */
.status-bar {
    background-color: #001100;
    color: #00ff00;
    border-top: 1px solid #00ff00;
    font-size: 11px;
}

/* Стили для разделителей */
.separator {
    background-color: #00ff00;
    height: 1px;
    margin: 10px 0;
}

.separator-horizontal {
    background-color: #00ff00;
    width: 1px;
    margin: 0 10px;
}

/* Стили для выпадающих списков */
QComboBox {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    padding: 3px;
    border-radius: 3px;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
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
    border: 1px solid #00ff00;
    selection-background-color: #003300;
}

/* Стили для чекбоксов */
QCheckBox {
    color: #00ff00;
    spacing: 5px;
}

QCheckBox::indicator {
    width: 13px;
    height: 13px;
    border: 1px solid #00ff00;
    border-radius: 3px;
}

QCheckBox::indicator:checked {
    background-color: #00ff00;
}

QCheckBox::indicator:unchecked:hover {
    border: 1px solid #ffff00;
}

/* Стили для радиокнопок */
QRadioButton {
    color: #00ff00;
    spacing: 5px;
}

QRadioButton::indicator {
    width: 13px;
    height: 13px;
    border: 1px solid #00ff00;
    border-radius: 7px;
}

QRadioButton::indicator:checked {
    background-color: #00ff00;
}

QRadioButton::indicator:unchecked:hover {
    border: 1px solid #ffff00;
}

/* Стили для вкладок */
QTabWidget::pane {
    border: 1px solid #00ff00;
    background-color: #000000;
    border-radius: 5px;
}

QTabBar::tab {
    background-color: #001100;
    color: #00ff00;
    padding: 5px 10px;
    border: 1px solid #00ff00;
    margin-right: 2px;
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
}

QTabBar::tab:selected {
    background-color: #003300;
    font-weight: bold;
    border-bottom: none;
}

QTabBar::tab:hover {
    background-color: #002200;
}

QTabBar::tab:!selected {
    margin-top: 2px;
}

/* Стили для прогресс-баров */
QProgressBar {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    border-radius: 3px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #00ff00;
    border-radius: 2px;
}

/* Стили для списков */
QListView, QTreeView, QTableView {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    border-radius: 3px;
    outline: none;
}

QListView::item:selected, QTreeView::item:selected, QTableView::item:selected {
    background-color: #003300;
}

QListView::item:hover, QTreeView::item:hover, QTableView::item:hover {
    background-color: #002200;
}

/* Стили для группы элементов */
QGroupBox {
    color: #00ff00;
    border: 1px solid #00ff00;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
}

/* Стили для диалоговых окон */
QDialog {
    background-color: #000000;
    border: 2px solid #00ff00;
}

QMessageBox {
    background-color: #000000;
    color: #00ff00;
}

QMessageBox QLabel {
    color: #00ff00;
}

QMessageBox QPushButton {
    min-width: 80px;
}

/* Стили для панели инструментов */
QToolBar {
    background-color: #001100;
    border: 1px solid #00ff00;
    spacing: 3px;
    padding: 2px;
}

QToolButton {
    background-color: #002200;
    color: #00ff00;
    border: 1px solid #00ff00;
    border-radius: 3px;
    padding: 5px;
}

QToolButton:hover {
    background-color: #004400;
}

QToolButton:pressed {
    background-color: #001100;
}

/* Стили для спинбоксов */
QSpinBox, QDoubleSpinBox {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    padding: 3px;
    border-radius: 3px;
}

QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: #003300;
    border: 1px solid #00ff00;
    width: 15px;
}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #004400;
}

/* Стили для календаря */
QCalendarWidget {
    background-color: #001100;
    color: #00ff00;
}

QCalendarWidget QToolButton {
    background-color: #002200;
}

QCalendarWidget QMenu {
    background-color: #001100;
}

/* Стили для главного меню */
.menu-left-panel {
    background-color: #0a0a0a;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 20px;
}

.menu-right-panel {
    background-color: #0a0a0a;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 20px;
}

.game-description {
    background-color: #101010;
    color: #a0a0a0;
    border: 1px solid #333;
    border-radius: 5px;
    padding: 20px;
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
}

/* Стили для панели задач */
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

/* Стили для инвентаря */
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

/* Стили для персонажа */
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

/* Стили для окон */
.window-title {
    color: #00bfff;
    font-size: 16px;
    font-weight: bold;
    padding: 5px;
    background-color: #001133;
    border-bottom: 1px solid #00bfff;
}

.window-content {
    background-color: #000000;
    padding: 10px;
}

/* Стили для модальных окон */
.modal-overlay {
    background-color: rgba(0, 0, 0, 0.8);
}

.modal-window {
    background-color: #0a0a0a;
    border: 2px solid #00ff00;
    border-radius: 10px;
}

/* Стили для сетевого сканера */
.network-scanner {
    background-color: #000a1a;
    border: 2px solid #0088ff;
    border-radius: 8px;
}

.device-online {
    color: #00ff00;
}

.device-offline {
    color: #ff0000;
}

.device-suspicious {
    color: #ffff00;
    animation: blink 2s infinite;
}

/* Стили для терминала команд */
.terminal-command {
    color: #00ffff;
    font-weight: bold;
}

.terminal-output {
    color: #00ff00;
}

.terminal-error {
    color: #ff5555;
}

.terminal-success {
    color: #55ff55;
}

.terminal-warning {
    color: #ffff55;
}

/* Стили для навыков */
.skill-beginner {
    color: #00ff00;
}

.skill-intermediate {
    color: #00bfff;
}

.skill-advanced {
    color: #ff00ff;
}

.skill-expert {
    color: #ff8800;
}

.skill-master {
    color: #ffff00;
    text-shadow: 0 0 5px #ffff00;
}

/* Стили для времени */
.time-display {
    color: #00ffff;
    font-family: 'Source Code Pro', monospace;
    font-size: 14px;
    font-weight: bold;
}

/* Стили для денег */
.money-display {
    color: #ffff00;
    font-weight: bold;
}

/* Стили для репутации */
.reputation-high {
    color: #00ff00;
}

.reputation-medium {
    color: #ffff00;
}

.reputation-low {
    color: #ff0000;
}

/* Стили для кнопок действий */
.action-button {
    background-color: #003366;
    color: #00ffff;
    border: 2px solid #00ffff;
    border-radius: 5px;
    padding: 8px;
    font-weight: bold;
    min-height: 30px;
}

.action-button:hover {
    background-color: #004488;
    border-color: #00ffff;
}

.action-button-danger {
    background-color: #660000;
    color: #ff5555;
    border: 2px solid #ff5555;
}

.action-button-danger:hover {
    background-color: #880000;
    border-color: #ff8888;
}

.action-button-success {
    background-color: #006600;
    color: #55ff55;
    border: 2px solid #55ff55;
}

.action-button-success:hover {
    background-color: #008800;
    border-color: #88ff88;
}

/* Стили для уведомлений */
.notification-info {
    background-color: #001133;
    color: #00aaff;
    border: 1px solid #00aaff;
    border-radius: 5px;
    padding: 10px;
}

.notification-warning {
    background-color: #332200;
    color: #ffaa00;
    border: 1px solid #ffaa00;
    border-radius: 5px;
    padding: 10px;
}

.notification-error {
    background-color: #330000;
    color: #ff5555;
    border: 1px solid #ff5555;
    border-radius: 5px;
    padding: 10px;
    animation: blink 1s infinite;
}

.notification-success {
    background-color: #003300;
    color: #55ff55;
    border: 1px solid #55ff55;
    border-radius: 5px;
    padding: 10px;
}

/* Стили для карты офиса */
.office-map {
    background-color: #050510;
    border: 2px solid #00ff00;
    border-radius: 5px;
}

.map-player {
    color: #00ffff;
    font-weight: bold;
}

.map-computer {
    color: #00ff00;
}

.map-server {
    color: #ff00ff;
}

.map-security {
    color: #ff0000;
}

.map-printer {
    color: #ff8800;
}

/* Стили для панели инструментов хакинга */
.hacking-tool {
    background-color: #001122;
    border: 1px solid #0088ff;
    border-radius: 5px;
    padding: 5px;
    margin: 2px;
}

.hacking-tool-active {
    background-color: #002244;
    border: 2px solid #00ffff;
}

.hacking-tool-disabled {
    background-color: #001111;
    border: 1px solid #008888;
    color: #008888;
}

/* Стили для аватара персонажа */
.avatar-frame {
    border: 3px solid #00bfff;
    border-radius: 50%;
    padding: 5px;
    background-color: #001133;
}

.avatar-image {
    border-radius: 50%;
}

/* Стили для панели квестов */
.quest-panel {
    background-color: #0a0a1a;
    border: 2px solid #aa00aa;
    border-radius: 8px;
}

.quest-active {
    background-color: #001122;
    border-left: 4px solid #00bfff;
    padding: 10px;
    margin: 5px;
}

.quest-completed {
    background-color: #002200;
    border-left: 4px solid #00ff00;
    padding: 10px;
    margin: 5px;
    opacity: 0.7;
}

.quest-failed {
    background-color: #220000;
    border-left: 4px solid #ff0000;
    padding: 10px;
    margin: 5px;
    opacity: 0.7;
}

/* Стили для эмулятора терминала */
.terminal-emulator {
    background-color: #000000;
    color: #00ff00;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    border: 2px solid #00ff00;
    border-radius: 5px;
}

.prompt-user {
    color: #00ffff;
}

.prompt-host {
    color: #ffff00;
}

.prompt-path {
    color: #ff8800;
}

.command-cursor {
    background-color: #00ff00;
    color: #000000;
}

/* Стили для панели чата */
.chat-panel {
    background-color: #000a0a;
    border: 2px solid #00aaaa;
    border-radius: 8px;
}

.chat-message-user {
    background-color: #001133;
    border-left: 3px solid #00bfff;
    padding: 8px;
    margin: 5px;
    border-radius: 0 5px 5px 0;
}

.chat-message-npc {
    background-color: #003311;
    border-left: 3px solid #00ff88;
    padding: 8px;
    margin: 5px;
    border-radius: 0 5px 5px 0;
}

.chat-message-system {
    background-color: #331100;
    border-left: 3px solid #ff8800;
    padding: 8px;
    margin: 5px;
    border-radius: 0 5px 5px 0;
}

/* Стили для мини-игр */
.minigame-panel {
    background-color: #050505;
    border: 2px solid #ff00ff;
    border-radius: 8px;
}

.minigame-grid {
    background-color: #001100;
    border: 1px solid #00ff00;
}

.minigame-cell {
    border: 1px solid #008800;
}

.minigame-cell-active {
    background-color: #00ff00;
}

/* Стили для панели статистики */
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

/* Стили для анимаций загрузки */
.loading-spinner {
    color: #00ff00;
    font-size: 24px;
}

.loading-text {
    color: #00ff00;
    font-size: 14px;
}

/* Стили для всплывающих подсказок */
QToolTip {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    border-radius: 3px;
    padding: 5px;
    font-size: 11px;
}

/* Стили для выбора файлов */
QFileDialog {
    background-color: #000000;
    color: #00ff00;
}

QFileDialog QTreeView, QFileDialog QListView {
    background-color: #001100;
    color: #00ff00;
}

/* Стили для цветовой схемы */
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

/* Стили для почтового клиента */
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

.mail-button-reply {
    background-color: rgba(42, 62, 42, 0.9);
    border: 1px solid #44ff44;
}

.mail-button-reply:hover {
    background-color: rgba(50, 200, 50, 0.8);
    border-color: #88ff88;
}

.mail-button-back {
    background-color: rgba(68, 0, 68, 0.8);
    color: #cccccc;
    border: 1px solid #8a2be2;
    padding: 8px;
    font-weight: bold;
    border-radius: 6px;
    font-size: 12px;
}

.mail-button-back:hover {
    background-color: rgba(100, 50, 200, 0.8);
    border-color: #9370db;
    color: #ffffff;
}

.mail-stats {
    color: #cccccc;
    font-size: 12px;
    padding: 5px;
}

/* Стили для QListWidget в почте */
QListWidget {
    background-color: #000000;
    border: 1px solid #4b0082;
    border-radius: 5px;
    padding: 5px;
    color: #cccccc;
    font-size: 12px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #333333;
}

QListWidget::item:selected {
    background-color: #4b0082;
    border: 1px solid #9370db;
    border-radius: 3px;
}

QListWidget::item:hover {
    background-color: #2d004d;
}

/* Стили для кнопки почты на левой панели */
.mail-left-button {
    background-color: rgba(42, 42, 62, 0.9);
    color: #cccccc;
    border: 1px solid #8a2be2;
    padding: 8px;
    font-weight: bold;
    border-radius: 6px;
    margin-top: 5px;
    font-size: 12px;
}

.mail-left-button:hover {
    background-color: rgba(100, 50, 200, 0.8);
    border-color: #9370db;
    color: #ffffff;
    border-width: 2px;
}

.mail-left-button:pressed {
    background-color: rgba(70, 30, 150, 0.9);
}

/* Стили для TimeWidget */
TimeWidget {
    background-color: transparent;
    margin: 10px 0px;
}

/* Анимация мигания для разделителя времени */
@keyframes time-blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.time-separator {
    animation: time-blink 1s infinite;
}

/* Анимация пульсации времени */
@keyframes time-pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}

.time-pulse {
    animation: time-pulse 2s infinite;
}

/* Стили для разных времен дня */
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

/* Стили для прогресс-бара времени */
.time-progress-bar {
    background-color: rgba(20, 30, 40, 0.8);
    border: 1px solid #333;
    border-radius: 12px;
}

.time-progress-fill {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1dd1a1, stop:0.5 #00bfff, stop:1 #54a0ff);
    border-radius: 10px;
}

/* Стили для меток времени */
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

/* Медиа-запросы для адаптивности */
@media (max-width: 800px) {
    .menu-button {
        font-size: 12px;
        padding: 8px;
        min-height: 35px;
    }
    
    .game-title {
        font-size: 24px;
    }
    
    QTabBar::tab {
        padding: 3px 6px;
        font-size: 11px;
    }
    
    .time-hour, .time-minute {
        font-size: 20px;
    }
    
    .time-date {
        font-size: 12px;
    }
}

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
"""