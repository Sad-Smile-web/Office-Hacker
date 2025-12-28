# ui/settings_widget.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QSlider, QFrame,
                               QCheckBox, QComboBox, QGroupBox, QScrollArea, QMessageBox)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QPen, QBrush
import json
import os
import random
import math

from simple_translation import translation

class SettingsWidget(QWidget):
    settings_changed = Signal(dict)
    language_changed = Signal(str)
    back_to_menu = Signal()
    
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.parent = parent
        self.config = config if config else self.load_default_config()
        
        if "game" not in self.config:
            self.config["game"] = {}
        if "language" not in self.config["game"]:
            self.config["game"]["language"] = "ru"
        
        self.init_ui()
        self.setup_effects()
        
        self.load_ui_from_config()
        
        translation.on_language_changed(self.retranslate_ui)
    
    def load_default_config(self):
        """Загрузить значения по умолчанию"""
        return {
            "game": {
                "difficulty": 2,
                "autosave_interval": 300,
                "enable_tutorial": True,
                "language": "ru"
            },
            "graphics": {
                "enable_effects": True,
                "glitch_effects": True,
                "window_width": 1200,
                "window_height": 800,
                "display_mode": "fullscreen",
                "vsync": True,
                "effect_intensity": 70
            },
            "audio": {
                "enabled": True,
                "volume": 70,
                "master_volume": 70,
                "typing_sounds": True,
                "background_music": True,
                "effects_volume": 80,
                "music_volume": 60,
                "voice_effects": True,
                "environment_sounds": True,
                "dynamic_range": "normal"
            },
            "game_time": {
                "time_speed": 1.0,
                "real_time_seconds_per_game_minute": 10,
                "auto_pause_in_menus": True,
                "show_time_widget": True
            }
        }
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        self.title_label = QLabel(translation.t("settings.title"))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #00bfff;
            margin-bottom: 20px;
            text-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
        """)
        main_layout.addWidget(self.title_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: rgba(0, 17, 34, 0.5);
                width: 12px;
                border-radius: 6px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 191, 255, 0.7);
                min-height: 30px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 255, 255, 0.9);
            }
        """)
        
        self.settings_container = QWidget()
        self.settings_container.setStyleSheet("background-color: transparent;")
        self.settings_layout = QVBoxLayout()
        self.settings_layout.setSpacing(15)
        
        group_style = """
            QGroupBox {
                color: #00bfff;
                border: 2px solid rgba(0, 191, 255, 0.5);
                border-radius: 8px;
                margin-top: 15px;
                padding: 20px;
                font-weight: bold;
                background-color: rgba(10, 20, 40, 0.7);
                font-size: 14px;
                backdrop-filter: blur(5px);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                padding: 5px 15px;
                background-color: rgba(0, 34, 68, 0.8);
                border-radius: 4px;
                color: #00ffff;
            }
        """
        
        checkbox_style = """
            QCheckBox {
                color: #cccccc;
                padding: 10px 8px;
                font-size: 13px;
                spacing: 12px;
                min-height: 28px;
                background-color: transparent;
            }
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                border: 2px solid #00bfff;
                border-radius: 5px;
                background-color: rgba(0, 34, 68, 0.5);
            }
            QCheckBox::indicator:checked {
                background-color: #00bfff;
                image: url(:/icons/check.svg);
            }
            QCheckBox:hover {
                color: #ffffff;
                background-color: rgba(0, 100, 200, 0.2);
                border-radius: 4px;
            }
            QCheckBox::indicator:hover {
                border-color: #00ffff;
            }
        """
        
        slider_style = """
            QSlider::groove:horizontal {
                border: 1px solid #00bfff;
                height: 16px;
                background: rgba(0, 17, 51, 0.5);
                border-radius: 8px;
            }
            QSlider::handle:horizontal {
                background: qradialgradient(
                    cx:0.5, cy:0.5, radius:0.5,
                    fx:0.3, fy:0.3,
                    stop:0 #00ffff,
                    stop:1 #00bfff
                );
                width: 28px;
                margin: -6px 0;
                border-radius: 14px;
                height: 28px;
                border: 2px solid #ffffff;
            }
            QSlider::handle:horizontal:hover {
                background: qradialgradient(
                    cx:0.5, cy:0.5, radius:0.5,
                    fx:0.3, fy:0.3,
                    stop:0 #ffffff,
                    stop:1 #00ffff
                );
                width: 30px;
                border: 2px solid #00ffff;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00bfff,
                    stop:1 #00ffff
                );
                border-radius: 8px;
            }
        """
        
        combo_style = """
            QComboBox {
                background-color: rgba(0, 17, 51, 0.7);
                color: #00bfff;
                border: 1px solid #00bfff;
                border-radius: 5px;
                padding: 10px;
                font-size: 13px;
                min-width: 200px;
                min-height: 38px;
                backdrop-filter: blur(5px);
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
                background-color: rgba(0, 34, 68, 0.5);
                border-radius: 0 5px 5px 0;
            }
            QComboBox::down-arrow {
                border-left: 7px solid transparent;
                border-right: 7px solid transparent;
                border-top: 7px solid #00bfff;
            }
            QComboBox:hover {
                border-color: #00ffff;
                background-color: rgba(0, 34, 68, 0.8);
            }
            QComboBox QAbstractItemView {
                background-color: rgba(0, 17, 51, 0.9);
                color: #00bfff;
                border: 1px solid #00bfff;
                selection-background-color: rgba(0, 100, 200, 0.7);
                selection-color: #ffffff;
            }
        """
        
        self.language_group = QGroupBox(translation.t("settings.language_group"))
        self.language_group.setStyleSheet(group_style)
        language_layout = QVBoxLayout()
        language_layout.setSpacing(15)
        
        language_selector_layout = QHBoxLayout()
        self.language_label = QLabel(translation.t("settings.language"))
        self.language_label.setStyleSheet("""
            color: #cccccc; 
            font-size: 13px; 
            min-width: 180px; 
            min-height: 38px;
            padding-left: 5px;
        """)
        
        self.language_combo = QComboBox()
        self.language_combo.setStyleSheet(combo_style)
        
        self.language_combo.addItem("🇷🇺 Русский", "ru")
        self.language_combo.addItem("en English", "en")
        self.language_combo.addItem("🇪🇸 Español", "sp")
        
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        
        language_selector_layout.addWidget(self.language_label)
        language_selector_layout.addWidget(self.language_combo)
        language_selector_layout.addStretch()
        
        language_layout.addLayout(language_selector_layout)
        self.language_group.setLayout(language_layout)
        self.settings_layout.addWidget(self.language_group)
        
        self.graphics_group = QGroupBox(translation.t("settings.graphics"))
        self.graphics_group.setStyleSheet(group_style)
        graphics_layout = QVBoxLayout()
        graphics_layout.setSpacing(15)
        
        display_layout = QHBoxLayout()
        self.display_label = QLabel(translation.t("settings.display_mode"))
        self.display_label.setStyleSheet("""
            color: #cccccc; 
            font-size: 13px; 
            min-width: 180px; 
            min-height: 38px;
            padding-left: 5px;
        """)
        self.display_combo = QComboBox()
        self.display_combo.currentIndexChanged.connect(self.update_config)
        self.display_combo.setStyleSheet(combo_style)
        display_layout.addWidget(self.display_label)
        display_layout.addWidget(self.display_combo)
        display_layout.addStretch()
        graphics_layout.addLayout(display_layout)
        
        effects_layout = QVBoxLayout()
        effects_layout.setSpacing(8)
        
        self.effects_check = QCheckBox(translation.t("settings.visual_effects"))
        self.effects_check.stateChanged.connect(self.update_config)
        self.effects_check.setStyleSheet(checkbox_style)
        effects_layout.addWidget(self.effects_check)
        
        self.glitch_check = QCheckBox(translation.t("settings.glitch_effects"))
        self.glitch_check.stateChanged.connect(self.update_config)
        self.glitch_check.setStyleSheet(checkbox_style)
        effects_layout.addWidget(self.glitch_check)
        
        self.vsync_check = QCheckBox(translation.t("settings.vsync"))
        self.vsync_check.stateChanged.connect(self.update_config)
        self.vsync_check.setStyleSheet(checkbox_style)
        effects_layout.addWidget(self.vsync_check)
        
        graphics_layout.addLayout(effects_layout)
        
        intensity_layout = QHBoxLayout()
        self.intensity_label = QLabel(translation.t("settings.effect_intensity"))
        self.intensity_label.setStyleSheet("""
            color: #cccccc; 
            font-size: 13px; 
            min-width: 180px; 
            min-height: 38px;
            padding-left: 5px;
        """)
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setRange(0, 100)
        self.intensity_slider.valueChanged.connect(self.update_config)
        self.intensity_slider.setStyleSheet(slider_style)
        self.intensity_slider.setMinimumHeight(38)
        
        self.intensity_value = QLabel()
        self.intensity_value.setStyleSheet("""
            color: #00bfff; 
            font-size: 13px; 
            min-width: 50px; 
            min-height: 38px;
            font-weight: bold;
        """)
        self.intensity_slider.valueChanged.connect(
            lambda v: self.intensity_value.setText(f"{v}%")
        )
        
        intensity_layout.addWidget(self.intensity_label)
        intensity_layout.addWidget(self.intensity_slider)
        intensity_layout.addWidget(self.intensity_value)
        graphics_layout.addLayout(intensity_layout)
        
        resolution_layout = QHBoxLayout()
        self.resolution_label = QLabel(translation.t("settings.resolution"))
        self.resolution_label.setStyleSheet("""
            color: #cccccc; 
            font-size: 13px; 
            min-width: 180px; 
            min-height: 38px;
            padding-left: 5px;
        """)
        self.resolution_combo = QComboBox()
        self.resolution_combo.currentTextChanged.connect(self.update_resolution)
        self.resolution_combo.setStyleSheet(combo_style)
        
        resolution_layout.addWidget(self.resolution_label)
        resolution_layout.addWidget(self.resolution_combo)
        resolution_layout.addStretch()
        graphics_layout.addLayout(resolution_layout)
        
        self.graphics_group.setLayout(graphics_layout)
        self.settings_layout.addWidget(self.graphics_group)
        
        self.audio_group = QGroupBox(translation.t("settings.audio"))
        self.audio_group.setStyleSheet(group_style)
        audio_layout = QVBoxLayout()
        audio_layout.setSpacing(15)
        
        self.audio_check = QCheckBox(translation.t("settings.enable_audio"))
        self.audio_check.stateChanged.connect(self.update_config)
        self.audio_check.setStyleSheet(checkbox_style)
        audio_layout.addWidget(self.audio_check)
        
        volume_layout = QHBoxLayout()
        self.volume_label = QLabel(translation.t("settings.master_volume"))
        self.volume_label.setStyleSheet("""
            color: #cccccc; 
            font-size: 13px; 
            min-width: 180px; 
            min-height: 38px;
            padding-left: 5px;
        """)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.valueChanged.connect(self.update_config)
        self.volume_slider.setStyleSheet(slider_style)
        self.volume_slider.setMinimumHeight(38)
        
        self.volume_value = QLabel()
        self.volume_value.setStyleSheet("""
            color: #00bfff; 
            font-size: 13px; 
            min-width: 50px; 
            min-height: 38px;
            font-weight: bold;
        """)
        self.volume_slider.valueChanged.connect(
            lambda v: self.volume_value.setText(f"{v}%")
        )
        
        volume_layout.addWidget(self.volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_value)
        audio_layout.addLayout(volume_layout)
        
        master_volume_layout = QHBoxLayout()
        self.master_volume_label = QLabel(translation.t("settings.master_volume"))
        self.master_volume_label.setStyleSheet("""
            color: #cccccc; 
            font-size: 13px; 
            min-width: 180px; 
            min-height: 38px;
            padding-left: 5px;
        """)
        self.master_volume_slider = QSlider(Qt.Horizontal)
        self.master_volume_slider.setRange(0, 100)
        self.master_volume_slider.valueChanged.connect(self.update_config)
        self.master_volume_slider.setStyleSheet(slider_style)
        self.master_volume_slider.setMinimumHeight(38)
        
        self.master_volume_value = QLabel()
        self.master_volume_value.setStyleSheet("""
            color: #00bfff; 
            font-size: 13px; 
            min-width: 50px; 
            min-height: 38px;
            font-weight: bold;
        """)
        self.master_volume_slider.valueChanged.connect(
            lambda v: self.master_volume_value.setText(f"{v}%")
        )
        
        master_volume_layout.addWidget(self.master_volume_label)
        master_volume_layout.addWidget(self.master_volume_slider)
        master_volume_layout.addWidget(self.master_volume_value)
        audio_layout.addLayout(master_volume_layout)
        
        effects_volume_layout = QHBoxLayout()
        self.effects_volume_label = QLabel(translation.t("settings.effects_volume"))
        self.effects_volume_label.setStyleSheet("""
            color: #cccccc; 
            font-size: 13px; 
            min-width: 180px; 
            min-height: 38px;
            padding-left: 5px;
        """)
        self.effects_volume_slider = QSlider(Qt.Horizontal)
        self.effects_volume_slider.setRange(0, 100)
        self.effects_volume_slider.valueChanged.connect(self.update_config)
        self.effects_volume_slider.setStyleSheet(slider_style)
        self.effects_volume_slider.setMinimumHeight(38)
        
        self.effects_volume_value = QLabel()
        self.effects_volume_value.setStyleSheet("""
            color: #00bfff; 
            font-size: 13px; 
            min-width: 50px; 
            min-height: 38px;
            font-weight: bold;
        """)
        self.effects_volume_slider.valueChanged.connect(
            lambda v: self.effects_volume_value.setText(f"{v}%")
        )
        
        effects_volume_layout.addWidget(self.effects_volume_label)
        effects_volume_layout.addWidget(self.effects_volume_slider)
        effects_volume_layout.addWidget(self.effects_volume_value)
        audio_layout.addLayout(effects_volume_layout)
        
        music_volume_layout = QHBoxLayout()
        self.music_volume_label = QLabel(translation.t("settings.music_volume"))
        self.music_volume_label.setStyleSheet("""
            color: #cccccc; 
            font-size: 13px; 
            min-width: 180px; 
            min-height: 38px;
            padding-left: 5px;
        """)
        self.music_volume_slider = QSlider(Qt.Horizontal)
        self.music_volume_slider.setRange(0, 100)
        self.music_volume_slider.valueChanged.connect(self.update_config)
        self.music_volume_slider.setStyleSheet(slider_style)
        self.music_volume_slider.setMinimumHeight(38)
        
        self.music_volume_value = QLabel()
        self.music_volume_value.setStyleSheet("""
            color: #00bfff; 
            font-size: 13px; 
            min-width: 50px; 
            min-height: 38px;
            font-weight: bold;
        """)
        self.music_volume_slider.valueChanged.connect(
            lambda v: self.music_volume_value.setText(f"{v}%")
        )
        
        music_volume_layout.addWidget(self.music_volume_label)
        music_volume_layout.addWidget(self.music_volume_slider)
        music_volume_layout.addWidget(self.music_volume_value)
        audio_layout.addLayout(music_volume_layout)
        
        sound_effects_layout = QVBoxLayout()
        sound_effects_layout.setSpacing(8)
        
        self.typing_sounds_check = QCheckBox(translation.t("settings.typing_sounds"))
        self.typing_sounds_check.stateChanged.connect(self.update_config)
        self.typing_sounds_check.setStyleSheet(checkbox_style)
        sound_effects_layout.addWidget(self.typing_sounds_check)
        
        self.music_check = QCheckBox(translation.t("settings.background_music"))
        self.music_check.stateChanged.connect(self.update_config)
        self.music_check.setStyleSheet(checkbox_style)
        sound_effects_layout.addWidget(self.music_check)
        
        self.voice_check = QCheckBox(translation.t("settings.voice_effects"))
        self.voice_check.stateChanged.connect(self.update_config)
        self.voice_check.setStyleSheet(checkbox_style)
        sound_effects_layout.addWidget(self.voice_check)
        
        self.environment_check = QCheckBox(translation.t("settings.environment_sounds"))
        self.environment_check.stateChanged.connect(self.update_config)
        self.environment_check.setStyleSheet(checkbox_style)
        sound_effects_layout.addWidget(self.environment_check)
        
        audio_layout.addLayout(sound_effects_layout)
        
        # Динамический диапазон
        dynamic_range_layout = QHBoxLayout()
        self.dynamic_range_label = QLabel(translation.t("settings.dynamic_range"))
        self.dynamic_range_label.setStyleSheet("""
            color: #cccccc; 
            font-size: 13px; 
            min-width: 180px; 
            min-height: 38px;
            padding-left: 5px;
        """)
        self.dynamic_range_combo = QComboBox()
        self.dynamic_range_combo.currentTextChanged.connect(self.update_config)
        self.dynamic_range_combo.setStyleSheet(combo_style)
        
        dynamic_range_layout.addWidget(self.dynamic_range_label)
        dynamic_range_layout.addWidget(self.dynamic_range_combo)
        dynamic_range_layout.addStretch()
        audio_layout.addLayout(dynamic_range_layout)
        
        self.audio_group.setLayout(audio_layout)
        self.settings_layout.addWidget(self.audio_group)
        
        # ================================
        # Группа игрового времени
        # ================================
        self.time_group = QGroupBox(translation.t("settings.game_time"))
        self.time_group.setStyleSheet(group_style)
        time_layout = QVBoxLayout()
        time_layout.setSpacing(15)
        
        # Скорость времени
        time_speed_layout = QHBoxLayout()
        self.time_speed_label = QLabel(translation.t("settings.time_speed"))
        self.time_speed_label.setStyleSheet("""
            color: #cccccc; 
            font-size: 13px; 
            min-width: 180px; 
            min-height: 38px;
            padding-left: 5px;
        """)
        self.time_speed_slider = QSlider(Qt.Horizontal)
        self.time_speed_slider.setRange(1, 50)
        self.time_speed_slider.valueChanged.connect(self.update_config)
        self.time_speed_slider.setStyleSheet(slider_style)
        self.time_speed_slider.setMinimumHeight(38)
        
        self.time_speed_value = QLabel()
        self.time_speed_value.setStyleSheet("""
            color: #00bfff; 
            font-size: 13px; 
            min-width: 50px; 
            min-height: 38px;
            font-weight: bold;
        """)
        self.time_speed_slider.valueChanged.connect(
            lambda v: self.time_speed_value.setText(f"{v/10:.1f}x")
        )
        
        time_speed_layout.addWidget(self.time_speed_label)
        time_speed_layout.addWidget(self.time_speed_slider)
        time_speed_layout.addWidget(self.time_speed_value)
        time_layout.addLayout(time_speed_layout)
        
        # Авто-пауза в меню
        self.auto_pause_check = QCheckBox(translation.t("settings.auto_pause"))
        self.auto_pause_check.stateChanged.connect(self.update_config)
        self.auto_pause_check.setStyleSheet(checkbox_style)
        time_layout.addWidget(self.auto_pause_check)
        
        # Показывать виджет времени
        self.show_time_check = QCheckBox(translation.t("settings.show_time_widget"))
        self.show_time_check.stateChanged.connect(self.update_config)
        self.show_time_check.setStyleSheet(checkbox_style)
        time_layout.addWidget(self.show_time_check)
        
        self.time_group.setLayout(time_layout)
        self.settings_layout.addWidget(self.time_group)
        
        # Кнопки действий
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.settings_save_btn = QPushButton(translation.t("settings.apply"))
        self.settings_save_btn.clicked.connect(self.save_settings)
        self.settings_save_btn.setMinimumHeight(45)
        self.settings_save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0066aa, stop:0.5 #004488, stop:1 #002266);
                color: #00ffff;
                border: 2px solid #00bfff;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                min-height: 45px;
                border-radius: 8px;
                text-align: center;
                letter-spacing: 0.5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0088cc, stop:0.5 #0066aa, stop:1 #004488);
                border-color: #00ffff;
                color: #ffffff;
                border-width: 3px;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #002244, stop:0.5 #001133, stop:1 #000022);
                border-color: #00bfff;
            }
        """)
        
        self.settings_default_btn = QPushButton(translation.t("settings.reset"))
        self.settings_default_btn.clicked.connect(self.reset_defaults)
        self.settings_default_btn.setMinimumHeight(45)
        self.settings_default_btn.setStyleSheet(self.settings_save_btn.styleSheet())
        
        self.settings_test_btn = QPushButton(translation.t("settings.test_sound"))
        self.settings_test_btn.clicked.connect(self.test_sound)
        self.settings_test_btn.setMinimumHeight(45)
        self.settings_test_btn.setStyleSheet(self.settings_save_btn.styleSheet())
        
        self.settings_back_btn = QPushButton(translation.t("settings.back"))
        self.settings_back_btn.clicked.connect(self.go_back)
        self.settings_back_btn.setMinimumHeight(45)
        self.settings_back_btn.setStyleSheet(self.settings_save_btn.styleSheet())
        
        buttons_layout.addWidget(self.settings_save_btn)
        buttons_layout.addWidget(self.settings_default_btn)
        buttons_layout.addWidget(self.settings_test_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.settings_back_btn)
        
        self.settings_layout.addLayout(buttons_layout)
        
        self.settings_container.setLayout(self.settings_layout)
        scroll_area.setWidget(self.settings_container)
        main_layout.addWidget(scroll_area)
        
        self.setLayout(main_layout)
        
    def load_ui_from_config(self):
        """Загружает значения из конфига в UI"""
        # Устанавливаем язык
        current_lang = self.config["game"].get("language", "ru")
        
        # Находим индекс языка в комбобоксе
        self.language_combo.blockSignals(True)
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_lang:
                self.language_combo.setCurrentIndex(i)
                break
        self.language_combo.blockSignals(False)
        
        # Разрешения
        resolutions = ["800x600", "1024x768", "1280x720", "1366x768", 
                      "1600x900", "1920x1080", "2560x1440", "3840x2160"]
        self.resolution_combo.clear()
        self.resolution_combo.addItems(resolutions)
        
        # Устанавливаем значения из конфига
        # Графика
        display_mode = self.config["graphics"].get("display_mode", "fullscreen")
        self.display_combo.blockSignals(True)
        self.display_combo.clear()
        self.display_combo.addItems([
            translation.t("settings.display_modes.fullscreen"),
            translation.t("settings.display_modes.windowed"),
            translation.t("settings.display_modes.borderless")
        ])
        if display_mode == "fullscreen":
            self.display_combo.setCurrentIndex(0)
        elif display_mode == "windowed":
            self.display_combo.setCurrentIndex(1)
        elif display_mode == "borderless":
            self.display_combo.setCurrentIndex(2)
        self.display_combo.blockSignals(False)
        
        self.effects_check.setChecked(self.config["graphics"].get("enable_effects", True))
        self.glitch_check.setChecked(self.config["graphics"].get("glitch_effects", True))
        self.vsync_check.setChecked(self.config["graphics"].get("vsync", True))
        self.intensity_slider.setValue(self.config["graphics"].get("effect_intensity", 70))
        self.intensity_value.setText(f"{self.config['graphics'].get('effect_intensity', 70)}%")
        
        current_res = f"{self.config['graphics'].get('window_width', 1200)}x{self.config['graphics'].get('window_height', 800)}"
        if current_res in [self.resolution_combo.itemText(i) for i in range(self.resolution_combo.count())]:
            self.resolution_combo.setCurrentText(current_res)
        else:
            self.resolution_combo.addItem(current_res)
            self.resolution_combo.setCurrentText(current_res)
        
        # Аудио
        self.audio_check.setChecked(self.config["audio"].get("enabled", True))
        self.volume_slider.setValue(self.config["audio"].get("volume", 70))
        self.volume_value.setText(f"{self.config['audio'].get('volume', 70)}%")
        self.master_volume_slider.setValue(self.config["audio"].get("master_volume", 70))
        self.master_volume_value.setText(f"{self.config['audio'].get('master_volume', 70)}%")
        self.typing_sounds_check.setChecked(self.config["audio"].get("typing_sounds", True))
        self.music_check.setChecked(self.config["audio"].get("background_music", True))
        self.effects_volume_slider.setValue(self.config["audio"].get("effects_volume", 80))
        self.effects_volume_value.setText(f"{self.config['audio'].get('effects_volume', 80)}%")
        self.music_volume_slider.setValue(self.config["audio"].get("music_volume", 60))
        self.music_volume_value.setText(f"{self.config['audio'].get('music_volume', 60)}%")
        self.voice_check.setChecked(self.config["audio"].get("voice_effects", True))
        self.environment_check.setChecked(self.config["audio"].get("environment_sounds", True))
        
        dynamic_range = self.config["audio"].get("dynamic_range", "normal")
        self.dynamic_range_combo.blockSignals(True)
        self.dynamic_range_combo.clear()
        self.dynamic_range_combo.addItems(["Нормальный", "Широкий", "Ночной"])
        if dynamic_range == "normal":
            self.dynamic_range_combo.setCurrentIndex(0)
        elif dynamic_range == "wide":
            self.dynamic_range_combo.setCurrentIndex(1)
        elif dynamic_range == "night":
            self.dynamic_range_combo.setCurrentIndex(2)
        self.dynamic_range_combo.blockSignals(False)
        
        # Игровое время
        self.time_speed_slider.setValue(int(self.config["game_time"].get("time_speed", 1.0) * 10))
        self.time_speed_value.setText(f"{self.config['game_time'].get('time_speed', 1.0):.1f}x")
        self.auto_pause_check.setChecked(self.config["game_time"].get("auto_pause_in_menus", True))
        self.show_time_check.setChecked(self.config["game_time"].get("show_time_widget", True))
    
    def on_language_changed(self):
        """Обработчик изменения языка в комбобоксе"""
        # Получаем выбранный язык
        language_code = self.language_combo.currentData()
        
        if language_code and language_code != self.config["game"].get("language", "ru"):
            # Обновляем конфиг
            self.config["game"]["language"] = language_code
            
            # Меняем язык в системе переводов
            translation.set_language(language_code)
            
            # Сохраняем конфиг сразу
            self.save_settings_silent()
            
            # Уведомляем главное окно
            self.language_changed.emit(language_code)
    
    def save_settings_silent(self):
        """Сохранить настройки без эффектов"""
        try:
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(f"[КОНФИГ] Язык изменен на: {self.config['game']['language']}")
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def retranslate_ui(self):
        """Обновить все тексты при смене языка"""
        # Заголовок
        self.title_label.setText(translation.t("settings.title"))
        
        # Группы
        self.language_group.setTitle(translation.t("settings.language_group"))
        self.graphics_group.setTitle(translation.t("settings.graphics"))
        self.audio_group.setTitle(translation.t("settings.audio"))
        self.time_group.setTitle(translation.t("settings.game_time"))
        
        # Метки
        self.language_label.setText(translation.t("settings.language"))
        self.display_label.setText(translation.t("settings.display_mode"))
        self.effects_check.setText(translation.t("settings.visual_effects"))
        self.glitch_check.setText(translation.t("settings.glitch_effects"))
        self.vsync_check.setText(translation.t("settings.vsync"))
        self.intensity_label.setText(translation.t("settings.effect_intensity"))
        self.resolution_label.setText(translation.t("settings.resolution"))
        
        # Аудио
        self.audio_check.setText(translation.t("settings.enable_audio"))
        self.volume_label.setText(translation.t("settings.master_volume"))
        self.master_volume_label.setText(translation.t("settings.master_volume"))
        self.effects_volume_label.setText(translation.t("settings.effects_volume"))
        self.music_volume_label.setText(translation.t("settings.music_volume"))
        self.typing_sounds_check.setText(translation.t("settings.typing_sounds"))
        self.music_check.setText(translation.t("settings.background_music"))
        self.voice_check.setText(translation.t("settings.voice_effects"))
        self.environment_check.setText(translation.t("settings.environment_sounds"))
        self.dynamic_range_label.setText(translation.t("settings.dynamic_range"))
        
        # Игровое время
        self.time_speed_label.setText(translation.t("settings.time_speed"))
        self.auto_pause_check.setText(translation.t("settings.auto_pause"))
        self.show_time_check.setText(translation.t("settings.show_time_widget"))
        
        # Обновляем комбобоксы
        self.display_combo.blockSignals(True)
        self.display_combo.clear()
        self.display_combo.addItems([
            translation.t("settings.display_modes.fullscreen"),
            translation.t("settings.display_modes.windowed"),
            translation.t("settings.display_modes.borderless")
        ])
        self.display_combo.blockSignals(False)
        
        # Обновляем кнопки
        self.settings_save_btn.setText(translation.t("settings.apply"))
        self.settings_default_btn.setText(translation.t("settings.reset"))
        self.settings_test_btn.setText(translation.t("settings.test_sound"))
        self.settings_back_btn.setText(translation.t("settings.back"))
        
        # Обновляем значения комбобокса выбора языка (чтобы названия были на выбранном языке)
        self.language_combo.blockSignals(True)
        current_lang = translation.language
        self.language_combo.setItemText(0, "🇷🇺 Русский" if current_lang == "ru" else "🇷🇺 Русский")
        self.language_combo.setItemText(1, "en English (70%)" if current_lang == "en" else "en English (70%)")
        self.language_combo.setItemText(2, "🇪🇸 Español (70%)" if current_lang == "sp" else "🇪🇸 Español (70%)")
        self.language_combo.blockSignals(False)
        
        # Обновляем тексты в комбобоксе динамического диапазона
        self.dynamic_range_combo.blockSignals(True)
        current_index = self.dynamic_range_combo.currentIndex()
        self.dynamic_range_combo.clear()
        self.dynamic_range_combo.addItems(["Нормальный", "Широкий", "Ночной"])
        self.dynamic_range_combo.setCurrentIndex(current_index)
        self.dynamic_range_combo.blockSignals(False)
    
    def setup_effects(self):
        """Настройка эффектов для виджета настроек"""
        # Таймер для эффектов
        self.effect_timer = QTimer()
        self.effect_timer.timeout.connect(self.update_effects)
        self.effect_timer.start(30)
        
        # Частицы для эффектов
        self.particles = []
        self.init_particles(30)
        
        # Эффект сканирующих линий
        self.scan_line_y = 0
        self.scan_line_speed = 2
        
        # Эффект пульсации
        self.pulse_value = 0.0
        self.pulse_direction = 1
        
    def init_particles(self, count):
        """Инициализация частиц"""
        for _ in range(count):
            self.particles.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.5, 2.0),
                'color': QColor(
                    random.randint(0, 100),
                    random.randint(150, 255),
                    random.randint(200, 255),
                    random.randint(30, 80)
                ),
                'direction': random.uniform(0, 2 * math.pi),
                'lifetime': random.randint(100, 300)
            })
            
    def update_effects(self):
        """Обновление всех эффектов"""
        # Обновление частиц
        for particle in self.particles:
            particle['x'] += math.cos(particle['direction']) * particle['speed']
            particle['y'] += math.sin(particle['direction']) * particle['speed']
            particle['lifetime'] -= 1
            
            if (particle['x'] < 0 or particle['x'] > self.width() or 
                particle['y'] < 0 or particle['y'] > self.height() or
                particle['lifetime'] <= 0):
                particle.update({
                    'x': random.randint(0, self.width()),
                    'y': random.randint(0, self.height()),
                    'lifetime': random.randint(100, 300)
                })
        
        # Обновление сканирующей линии
        self.scan_line_y = (self.scan_line_y + self.scan_line_speed) % (self.height() + 30)
        
        # Обновление пульсации
        self.pulse_value += 0.02 * self.pulse_direction
        if self.pulse_value >= 1.0:
            self.pulse_direction = -1
            self.pulse_value = 1.0
        elif self.pulse_value <= 0.0:
            self.pulse_direction = 1
            self.pulse_value = 0.0
        
        # Случайные глитчи
        if (self.config["graphics"].get("enable_effects", True) and 
            self.config["graphics"].get("glitch_effects", True) and 
            random.random() < 0.005):
            self.trigger_glitch_effect()
        
        self.update()
        
    def trigger_glitch_effect(self):
        """Активировать эффект глитча"""
        glitch_elements = [
            self.settings_save_btn,
            self.settings_default_btn,
            self.settings_test_btn,
            self.settings_back_btn
        ]
        
        for element in glitch_elements:
            if random.random() < 0.4:
                original_style = element.styleSheet()
                glitch_colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff"]
                glitch_color = random.choice(glitch_colors)
                
                glitch_style = f"""
                    border-color: {glitch_color};
                    color: {glitch_color};
                """
                
                element.setStyleSheet(original_style + glitch_style)
                
                QTimer.singleShot(200, lambda e=element, s=original_style: e.setStyleSheet(s))
    
    def paintEvent(self, event):
        """Отрисовка эффектов"""
        super().paintEvent(event)
        
        if not self.config["graphics"].get("enable_effects", True):
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Эффект частиц
        for particle in self.particles:
            alpha = particle['color'].alpha() * (particle['lifetime'] / 300.0)
            color = QColor(particle['color'])
            color.setAlpha(int(alpha))
            
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.setOpacity(0.3)
            painter.drawEllipse(
                int(particle['x']),
                int(particle['y']),
                particle['size'],
                particle['size']
            )
        
        # Сканирующие линии
        scan_height = 25
        scan_gradient = QLinearGradient(0, self.scan_line_y, 0, self.scan_line_y + scan_height)
        scan_gradient.setColorAt(0, QColor(0, 191, 255, 0))
        scan_gradient.setColorAt(0.3, QColor(0, 191, 255, int(100 * self.pulse_value)))
        scan_gradient.setColorAt(0.7, QColor(0, 191, 255, int(100 * self.pulse_value)))
        scan_gradient.setColorAt(1, QColor(0, 191, 255, 0))
        
        painter.setOpacity(0.2)
        painter.fillRect(0, self.scan_line_y, self.width(), scan_height, scan_gradient)
        
        # Эффект сетки
        grid_size = 50
        painter.setOpacity(0.05)
        painter.setPen(QPen(QColor(0, 191, 255, 50), 1))
        
        for x in range(0, self.width(), grid_size):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), grid_size):
            painter.drawLine(0, y, self.width(), y)
        
        # Свечение по краям
        edge_glow = QLinearGradient(0, 0, self.width(), 0)
        edge_glow.setColorAt(0, QColor(0, 191, 255, int(50 * self.pulse_value)))
        edge_glow.setColorAt(0.1, QColor(0, 191, 255, 0))
        edge_glow.setColorAt(0.9, QColor(0, 191, 255, 0))
        edge_glow.setColorAt(1, QColor(0, 191, 255, int(50 * self.pulse_value)))
        
        painter.setOpacity(0.1)
        painter.fillRect(0, 0, self.width(), self.height(), edge_glow)
        
        painter.setOpacity(1.0)
    
    def update_config(self):
        """Обновление конфигурации при изменении настроек"""
        # Графика
        self.config["graphics"]["enable_effects"] = self.effects_check.isChecked()
        self.config["graphics"]["glitch_effects"] = self.glitch_check.isChecked()
        self.config["graphics"]["vsync"] = self.vsync_check.isChecked()
        self.config["graphics"]["effect_intensity"] = self.intensity_slider.value()
        
        # Режим отображения
        display_index = self.display_combo.currentIndex()
        if display_index == 0:
            self.config["graphics"]["display_mode"] = "fullscreen"
        elif display_index == 1:
            self.config["graphics"]["display_mode"] = "windowed"
        elif display_index == 2:
            self.config["graphics"]["display_mode"] = "borderless"
        
        # Аудио
        self.config["audio"]["enabled"] = self.audio_check.isChecked()
        self.config["audio"]["volume"] = self.volume_slider.value()
        self.config["audio"]["master_volume"] = self.master_volume_slider.value()
        self.config["audio"]["typing_sounds"] = self.typing_sounds_check.isChecked()
        self.config["audio"]["background_music"] = self.music_check.isChecked()
        self.config["audio"]["effects_volume"] = self.effects_volume_slider.value()
        self.config["audio"]["music_volume"] = self.music_volume_slider.value()
        self.config["audio"]["voice_effects"] = self.voice_check.isChecked()
        self.config["audio"]["environment_sounds"] = self.environment_check.isChecked()
        
        # Динамический диапазон
        dynamic_range_index = self.dynamic_range_combo.currentIndex()
        if dynamic_range_index == 0:
            self.config["audio"]["dynamic_range"] = "normal"
        elif dynamic_range_index == 1:
            self.config["audio"]["dynamic_range"] = "wide"
        elif dynamic_range_index == 2:
            self.config["audio"]["dynamic_range"] = "night"
        
        # Игровое время
        self.config["game_time"]["time_speed"] = self.time_speed_slider.value() / 10.0
        self.config["game_time"]["auto_pause_in_menus"] = self.auto_pause_check.isChecked()
        self.config["game_time"]["show_time_widget"] = self.show_time_check.isChecked()
        
        # Отправляем сигнал с обновленными настройками
        self.settings_changed.emit(self.config)
    
    def update_resolution(self):
        """Обновление разрешения окна"""
        resolution = self.resolution_combo.currentText()
        if "x" in resolution:
            width, height = map(int, resolution.split("x"))
            self.config["graphics"]["window_width"] = width
            self.config["graphics"]["window_height"] = height
    
    def save_settings(self):
        """Сохранить настройки"""
        try:
            # Обновляем настройки из UI
            self.update_config()
            
            # Сохраняем в файл
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            print("[КОНФИГ] Настройки сохранены")
            
            # Эффект подтверждения
            if self.config["graphics"].get("enable_effects", True):
                original_style = self.settings_save_btn.styleSheet()
                success_style = """
                    border-color: #00ff00;
                    color: #00ff00;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #006600, stop:0.5 #004400, stop:1 #002200);
                """
                self.settings_save_btn.setStyleSheet(original_style + success_style)
                
                QTimer.singleShot(500, lambda: self.settings_save_btn.setStyleSheet(original_style))
            
            # Звук успеха
            if self.config["audio"].get("enabled", True):
                try:
                    from audio_manager import AudioManager
                    audio = AudioManager()
                    audio.success_sound()
                except:
                    pass
                    
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
            
            # Эффект ошибки
            if self.config["graphics"].get("enable_effects", True):
                original_style = self.settings_save_btn.styleSheet()
                error_style = """
                    border-color: #ff0000;
                    color: #ff0000;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #660000, stop:0.5 #440000, stop:1 #220000);
                """
                self.settings_save_btn.setStyleSheet(original_style + error_style)
                
                QTimer.singleShot(500, lambda: self.settings_save_btn.setStyleSheet(original_style))
    
    def reset_defaults(self):
        """Сброс настроек к значениям по умолчанию"""
        # Сбрасываем конфиг к значениям по умолчанию
        self.config = self.load_default_config()
        
        # Обновляем UI
        self.load_ui_from_config()
        
        # Эффект сброса
        if self.config["graphics"].get("enable_effects", True):
            for btn in [self.settings_save_btn, self.settings_default_btn, 
                       self.settings_test_btn, self.settings_back_btn]:
                original_style = btn.styleSheet()
                reset_style = """
                    border-color: #ffff00;
                    color: #ffff00;
                """
                btn.setStyleSheet(original_style + reset_style)
                QTimer.singleShot(300, lambda b=btn, s=original_style: b.setStyleSheet(s))
        
        # Звук сброса
        if self.config["audio"].get("enabled", True):
            try:
                from audio_manager import AudioManager
                audio = AudioManager()
                audio.click_sound()
            except:
                pass
        
        # Отправляем сигнал
        self.settings_changed.emit(self.config)
        
        # Показываем сообщение о сбросе
        QMessageBox.information(
            self,
            translation.t("settings.reset_message_title"),
            translation.t("settings.reset_message")
        )
    
    def test_sound(self):
        """Тест звука"""
        try:
            from audio_manager import AudioManager
            audio = AudioManager()
            
            # Воспроизводим последовательность звуков
            audio.click_sound()
            
            QTimer.singleShot(200, audio.typing_sound)
            QTimer.singleShot(400, audio.success_sound)
            QTimer.singleShot(600, audio.notification_sound)
            
            # Эффект теста
            if self.config["graphics"].get("enable_effects", True):
                original_style = self.settings_test_btn.styleSheet()
                test_style = """
                    border-color: #00ffff;
                    color: #00ffff;
                    animation: pulse 0.5s infinite;
                """
                self.settings_test_btn.setStyleSheet(original_style + test_style)
                QTimer.singleShot(800, lambda: self.settings_test_btn.setStyleSheet(original_style))
                
        except Exception as e:
            print(f"Ошибка теста звука: {e}")
    
    def go_back(self):
        """Вернуться в меню"""
        # Звук возврата
        if self.config["audio"].get("enabled", True):
            try:
                from audio_manager import AudioManager
                audio = AudioManager()
                audio.click_sound()
            except:
                pass
        
        self.back_to_menu.emit()