# audio_manager.py
import pygame
import os
import json
from pathlib import Path
import sys
import time
import random
import numpy as np

class AudioManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if not self.initialized:
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                self.config = self.load_config()
                self.sounds = {}
                self.music_enabled = True
                self.sfx_enabled = True
                self.volume = self.config["audio"]["volume"] / 100
                self.load_sounds()
                self.initialized = True
                print("[АУДИО] Аудио менеджер инициализирован")
            except Exception as e:
                print(f"[АУДИО] Ошибка инициализации: {e}")
                # Создаем заглушки даже при ошибке
                self.initialized = True
                self.config = {"audio": {"enabled": False, "volume": 70}}
                self.sounds = {}
    
    def load_config(self):
        """Загрузить конфигурацию"""
        default_config = {
            "audio": {
                "enabled": True,
                "volume": 70,
                "typing_sounds": True,
                "background_music": True,
                "effects_volume": 80,
                "music_volume": 60,
                "ui_sounds": True,
                "voice_effects": True
            }
        }
        
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                    if "audio" in loaded_config:
                        default_config["audio"].update(loaded_config["audio"])
        except Exception as e:
            print(f"[АУДИО] Ошибка загрузки конфига: {e}")
        
        return default_config
    
    def load_sounds(self):
        """Загрузить звуки"""
        sound_dir = Path("assets/sounds")
        sound_dir.mkdir(exist_ok=True)
        
        # Основные звуки
        sound_files = {
            "typing": "typing.wav",
            "click": "click.wav",
            "success": "success.wav",
            "error": "error.wav",
            "hack": "hack.wav",
            "scan": "scan.wav",
            "notification": "notification.wav",
            "startup": "startup.wav",
            "shutdown": "shutdown.wav"
        }
        
        for name, filename in sound_files.items():
            path = sound_dir / filename
            if path.exists():
                try:
                    self.sounds[name] = pygame.mixer.Sound(str(path))
                    print(f"[АУДИО] Звук загружен: {name}")
                except Exception as e:
                    print(f"[АУДИО] Ошибка загрузки звука {filename}: {e}")
                    # Создаем заглушку
                    self.create_dummy_sound(name)
            else:
                print(f"[АУДИО] Файл звука не найден: {filename}")
                self.create_dummy_sound(name)
        
        # Фоновая музыка (теперь .wav вместо .mp3)
        music_path = sound_dir / "background.wav"
        if music_path.exists():
            try:
                pygame.mixer.music.load(str(music_path))
                print("[АУДИО] Фоновая музыка загружена")
            except Exception as e:
                print(f"[АУДИО] Ошибка загрузки музыки: {e}")
        else:
            print("[АУДИО] Фоновая музыка не найдена")
    
    def create_dummy_sound(self, name):
        """Создать заглушку для отсутствующего звука"""
        try:
            sample_rate = 44100
            
            if name == "typing":
                duration = 0.07
                freq = 1200
            elif name == "click":
                duration = 0.1
                freq = 800
            elif name == "success":
                duration = 0.5
                freq = 1200
            elif name == "error":
                duration = 0.3
                freq = 400
            elif name == "hack":
                duration = 2.0
                freq = 600
            elif name == "scan":
                duration = 1.5
                freq = 300
            elif name == "notification":
                duration = 0.3
                freq = 1000
            elif name == "startup":
                duration = 3.0
                freq = 800
            elif name == "shutdown":
                duration = 2.0
                freq = 400
            else:
                duration = 0.15
                freq = 600
            
            # Создаем простой звук
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = 0.3 * np.sin(2 * np.pi * freq * t)
            
            # Огибающая
            envelope = np.exp(-t * 3) * (1 - np.exp(-t * 50))
            wave *= envelope
            
            # Конвертируем в 16-битный PCM
            wave = (wave * 32767).astype(np.int16)
            
            # Создаем стерео звук
            stereo = np.column_stack((wave, wave))
            
            # Создаем звук через pygame
            self.sounds[name] = pygame.sndarray.make_sound(stereo)
        except Exception as e:
            print(f"[АУДИО] Ошибка создания заглушки {name}: {e}")
            # Создаем пустой звук
            try:
                self.sounds[name] = pygame.Sound(buffer=bytes([0] * 4410))
            except:
                self.sounds[name] = None
    
    def play_sound(self, name, volume_multiplier=1.0):
        """Воспроизвести звуковой эффект"""
        if not self.sfx_enabled or name not in self.sounds or self.sounds[name] is None:
            return
        
        try:
            sound = self.sounds[name]
            # Устанавливаем громкость
            calculated_volume = (self.volume * self.config["audio"]["effects_volume"] / 100) * volume_multiplier
            sound.set_volume(min(1.0, calculated_volume / 100.0))
            sound.play()
        except Exception as e:
            print(f"[АУДИО] Ошибка воспроизведения звука {name}: {e}")
    
    def play_music(self, loop=True):
        """Воспроизвести фоновую музыку"""
        if not self.music_enabled:
            return
        
        try:
            music_volume = min(1.0, (self.volume * self.config["audio"]["music_volume"] / 100) / 100.0)
            pygame.mixer.music.set_volume(music_volume)
            if loop:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play(1)
        except Exception as e:
            print(f"[АУДИО] Ошибка воспроизведения музыки: {e}")
    
    def stop_music(self):
        """Остановить музыку"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    def pause_music(self):
        """Приостановить музыку"""
        try:
            pygame.mixer.music.pause()
        except:
            pass
    
    def unpause_music(self):
        """Возобновить музыку"""
        try:
            pygame.mixer.music.unpause()
        except:
            pass
    
    def update_settings(self, config):
        """Обновить настройки аудио"""
        try:
            if "audio" in config:
                self.config["audio"].update(config["audio"])
                
                # Обновляем громкость
                self.volume = self.config["audio"]["volume"] / 100
                
                # Обновляем громкость музыки
                music_volume = min(1.0, (self.volume * self.config["audio"]["music_volume"] / 100) / 100.0)
                pygame.mixer.music.set_volume(music_volume)
                
                # Обновляем громкость всех звуков
                for sound in self.sounds.values():
                    if sound is not None:
                        sound_volume = min(1.0, (self.volume * self.config["audio"]["effects_volume"] / 100) / 100.0)
                        sound.set_volume(sound_volume)
                
                # Включаем/выключаем музыку
                if self.config["audio"]["background_music"]:
                    if not pygame.mixer.music.get_busy():
                        self.play_music()
                else:
                    self.stop_music()
                
                self.music_enabled = self.config["audio"]["background_music"]
                self.sfx_enabled = self.config["audio"]["enabled"]
                
        except Exception as e:
            print(f"[АУДИО] Ошибка обновления настроек: {e}")
    
    def typing_sound(self):
        """Звук печати"""
        if self.config["audio"]["typing_sounds"]:
            self.play_sound("typing", 0.3)
    
    def click_sound(self):
        """Звук клика"""
        if self.config["audio"]["ui_sounds"]:
            self.play_sound("click", 0.5)
    
    def success_sound(self):
        """Звук успеха"""
        self.play_sound("success")
    
    def error_sound(self):
        """Звук ошибки"""
        self.play_sound("error")
    
    def hack_sound(self):
        """Звук взлома"""
        self.play_sound("hack")
    
    def scan_sound(self):
        """Звук сканирования"""
        self.play_sound("scan")
    
    def notification_sound(self):
        """Звук уведомления"""
        self.play_sound("notification")
    
    def startup_sound(self):
        """Звук запуска"""
        self.play_sound("startup")
    
    def shutdown_sound(self):
        """Звук выключения"""
        self.play_sound("shutdown")
    
    def set_master_volume(self, volume):
        """Установить общую громкость"""
        self.volume = max(0, min(1, volume))
        self.update_settings({"audio": {"volume": self.volume * 100}})
    
    def fade_out_music(self, duration=1000):
        """Плавное выключение музыки"""
        try:
            pygame.mixer.music.fadeout(duration)
        except:
            pass
    
    def is_playing(self):
        """Проверить, играет ли музыка"""
        try:
            return pygame.mixer.music.get_busy()
        except:
            return False
    
    def cleanup(self):
        """Очистка ресурсов"""
        try:
            pygame.mixer.quit()
        except:
            pass