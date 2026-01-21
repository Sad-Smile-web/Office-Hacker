# install_sounds.py
import os
from pathlib import Path
import numpy as np
import pygame
import wave
import struct

def create_dummy_sounds():
    """Создать заглушки для отсутствующих звуков"""
    sound_dir = Path("assets/sounds")
    sound_dir.mkdir(parents=True, exist_ok=True)
    
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    
    sounds = {
        "typing": (1000, 0.05),
        "click": (800, 0.1),
        "success": (1200, 0.2),
        "error": (400, 0.3),
        "hack": (600, 0.5),
        "scan": (300, 1.0),
        "notification": (1000, 0.15),
        "startup": (800, 0.8),
        "shutdown": (400, 0.8)
    }
    
    for name, (freq, duration) in sounds.items():
        filepath = sound_dir / f"{name}.wav"
        if not filepath.exists():
            print(f"Создаю звук: {name}")
            create_wave_file(filepath, freq, duration)
    
    print("Заглушки созданы в assets/sounds/")

def create_wave_file(filename, frequency, duration):
    """Создать WAV файл с синусоидальной волной"""
    sample_rate = 44100
    frames = int(duration * sample_rate)
    
    # Создаем синусоидальную волну
    t = np.linspace(0, duration, frames, False)
    wave_data = np.sin(2 * np.pi * frequency * t) * 0.3
    
    # Добавляем эффект затухания
    envelope = np.exp(-t * 2)
    wave_data *= envelope
    
    # Конвертируем в 16-битный PCM
    wave_data = (wave_data * 32767).astype(np.int16)
    
    # Создаем стерео звук
    stereo_data = np.column_stack((wave_data, wave_data))
    
    # Сохраняем в WAV файл
    with wave.open(str(filename), 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        # Конвертируем в байты
        byte_data = b''.join(
            struct.pack('<hh', left, right) 
            for left, right in stereo_data
        )
        
        wav_file.writeframes(byte_data)

if __name__ == "__main__":
    create_dummy_sounds()