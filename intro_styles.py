# intro_styles.py - Современные стили для нового интро
INTRO_STYLES = """
/* Современные минималистичные стили */
QWidget {
    background-color: #0a0f19;
    font-family: 'Segoe UI', 'Arial', sans-serif;
}

/* Плавные анимации */
@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes fadeOut {
    0% { opacity: 1; transform: scale(1); }
    100% { opacity: 0; transform: scale(0.98); }
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

@keyframes pulse {
    0% { opacity: 0.4; }
    50% { opacity: 1.0; }
    100% { opacity: 0.4; }
}

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

@keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes wave {
    0%, 100% { transform: translateX(0); }
    50% { transform: translateX(10px); }
}

/* Контейнеры */
.glass-panel {
    background: rgba(20, 25, 40, 0.7);
    border: 1px solid rgba(100, 150, 255, 0.2);
    border-radius: 12px;
    backdrop-filter: blur(10px);
    padding: 20px;
}

.glass-panel-light {
    background: rgba(30, 35, 50, 0.5);
    border: 1px solid rgba(100, 150, 255, 0.1);
    border-radius: 8px;
    backdrop-filter: blur(5px);
}

/* Текст */
.holo-title {
    color: #ffffff;
    font-size: 44px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-shadow: 0 0 20px rgba(0, 120, 255, 0.5);
}

.holo-subtitle {
    color: #a0c8ff;
    font-size: 26px;
    font-weight: 300;
    letter-spacing: 1px;
}

.system-text {
    color: #ffffff;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 16px;
    line-height: 1.5;
}

.system-text-dim {
    color: #8899cc;
    font-family: 'Consolas', monospace;
    font-size: 14px;
}

.console-text {
    color: #00ff88;
    font-family: 'Consolas', monospace;
    font-size: 14px;
    text-shadow: 0 0 5px #00ff88;
}

/* Кнопки */
.holo-button {
    background: linear-gradient(135deg, #0066cc, #0099ff);
    border: none;
    border-radius: 8px;
    color: white;
    padding: 14px 28px;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 20px rgba(0, 102, 204, 0.4);
}

.holo-button:hover {
    background: linear-gradient(135deg, #0099ff, #00ccff);
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 8px 25px rgba(0, 153, 255, 0.5);
}

.holo-button:pressed {
    background: linear-gradient(135deg, #0055aa, #0088ee);
    transform: translateY(-1px) scale(0.98);
    box-shadow: 0 2px 15px rgba(0, 102, 204, 0.3);
}

.holo-button:disabled {
    background: linear-gradient(135deg, #333344, #444455);
    color: #8888aa;
    box-shadow: none;
    transform: none;
}

/* Индикаторы */
.status-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: #00cc66;
    box-shadow: 0 0 15px #00cc66;
}

.status-indicator-offline {
    background-color: #ff4444;
    box-shadow: 0 0 15px #ff4444;
}

.status-indicator-pending {
    background-color: #ffaa00;
    box-shadow: 0 0 15px #ffaa00;
    animation: pulse 1.5s infinite;
}

.status-indicator-warning {
    background-color: #ff8800;
    box-shadow: 0 0 15px #ff8800;
    animation: pulse 2s infinite;
}

/* Прогресс-бары */
.holo-progress {
    background-color: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: 6px;
    height: 10px;
}

.holo-progress::chunk {
    background: linear-gradient(90deg, #0066cc, #0099ff, #00ccff);
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Карточки */
.data-card {
    background: rgba(30, 35, 50, 0.3);
    border: 1px solid rgba(100, 150, 255, 0.1);
    border-radius: 10px;
    padding: 18px;
    transition: all 0.3s ease;
}

.data-card:hover {
    background: rgba(40, 45, 60, 0.5);
    border-color: rgba(100, 150, 255, 0.3);
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 100, 255, 0.2);
}

/* Анимированные элементы */
.float-animation {
    animation: float 3s ease-in-out infinite;
}

.shimmer-text {
    background: linear-gradient(90deg, 
        rgba(255,255,255,0) 0%,
        rgba(255,255,255,0.6) 50%,
        rgba(255,255,255,0) 100%);
    background-size: 1000px 100%;
    animation: shimmer 2s infinite linear;
}

.wave-animation {
    animation: wave 2s ease-in-out infinite;
}

/* Спиннеры */
.holo-spinner {
    border: 4px solid rgba(0, 102, 204, 0.2);
    border-top: 4px solid #0099ff;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    animation: rotate 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}

.holo-spinner-small {
    border: 3px solid rgba(0, 102, 204, 0.2);
    border-top: 3px solid #0099ff;
    border-radius: 50%;
    width: 32px;
    height: 32px;
    animation: rotate 0.8s linear infinite;
}

/* Сетка */
.grid-line {
    border: none;
    border-top: 1px solid rgba(100, 150, 255, 0.15);
    margin: 12px 0;
}

.grid-dot {
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background-color: rgba(100, 150, 255, 0.3);
}

/* Переменные темы */
:root {
    --primary-color: #0066cc;
    --secondary-color: #0099ff;
    --accent-color: #00ccff;
    --success-color: #00cc66;
    --warning-color: #ffaa00;
    --error-color: #ff4444;
    --bg-dark: #0a0f19;
    --bg-medium: #1a1f2a;
    --bg-light: #2a2f3a;
    --text-primary: #ffffff;
    --text-secondary: #a0c8ff;
    --text-dim: #8899cc;
}

/* Утилитарные классы */
.text-gradient {
    background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.text-gradient-reverse {
    background: linear-gradient(90deg, var(--accent-color), var(--primary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.glow-effect {
    box-shadow: 0 0 20px rgba(0, 153, 255, 0.4);
}

.glow-effect-strong {
    box-shadow: 0 0 30px rgba(0, 153, 255, 0.6);
}

.glow-effect-subtle {
    box-shadow: 0 0 15px rgba(0, 153, 255, 0.2);
}

/* Заголовки */
.section-header {
    color: var(--text-primary);
    font-size: 24px;
    font-weight: 600;
    border-left: 4px solid var(--primary-color);
    padding-left: 15px;
    margin: 20px 0 15px 0;
}

.subsection-header {
    color: var(--text-secondary);
    font-size: 18px;
    font-weight: 500;
    margin: 15px 0 10px 0;
}

/* Списки */
.system-list {
    background: rgba(30, 35, 50, 0.2);
    border-radius: 8px;
    padding: 10px;
}

.system-list-item {
    padding: 10px 15px;
    border-bottom: 1px solid rgba(100, 150, 255, 0.1);
    color: var(--text-dim);
}

.system-list-item:last-child {
    border-bottom: none;
}

.system-list-item:hover {
    background: rgba(100, 150, 255, 0.1);
    color: var(--text-secondary);
}

/* Адаптивность */
@media (max-width: 1024px) {
    .holo-title {
        font-size: 36px;
    }
    
    .holo-subtitle {
        font-size: 22px;
    }
    
    .system-text {
        font-size: 14px;
    }
}

@media (max-width: 768px) {
    .holo-title {
        font-size: 28px;
    }
    
    .holo-subtitle {
        font-size: 18px;
    }
    
    .holo-button {
        padding: 12px 20px;
        font-size: 14px;
    }
}

@media (max-width: 480px) {
    .holo-title {
        font-size: 24px;
    }
    
    .holo-subtitle {
        font-size: 16px;
    }
    
    .glass-panel {
        padding: 15px;
    }
}

/* Полосы прокрутки */
QScrollBar:vertical {
    background: rgba(30, 35, 50, 0.3);
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: rgba(100, 150, 255, 0.5);
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(100, 150, 255, 0.7);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: rgba(30, 35, 50, 0.3);
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background: rgba(100, 150, 255, 0.5);
    border-radius: 5px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background: rgba(100, 150, 255, 0.7);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Поля ввода */
.system-input {
    background: rgba(30, 35, 50, 0.5);
    border: 1px solid rgba(100, 150, 255, 0.3);
    border-radius: 6px;
    padding: 10px 15px;
    color: var(--text-primary);
    font-size: 14px;
    selection-background-color: var(--primary-color);
}

.system-input:focus {
    border: 1px solid var(--secondary-color);
    box-shadow: 0 0 10px rgba(0, 153, 255, 0.3);
}

.system-input:disabled {
    background: rgba(30, 35, 50, 0.2);
    border-color: rgba(100, 150, 255, 0.1);
    color: var(--text-dim);
}

/* Переключатели */
.system-toggle {
    background: rgba(30, 35, 50, 0.5);
    border: 1px solid rgba(100, 150, 255, 0.3);
    border-radius: 15px;
    width: 60px;
    height: 30px;
}

.system-toggle::indicator {
    background: rgba(100, 150, 255, 0.5);
    border-radius: 13px;
    width: 26px;
    height: 26px;
    margin: 1px;
}

.system-toggle:checked {
    background: rgba(0, 153, 255, 0.3);
    border-color: var(--secondary-color);
}

.system-toggle:checked::indicator {
    background: var(--secondary-color);
    transform: translateX(30px);
}

/* Для пользователей, предпочитающих уменьшенное движение */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
"""