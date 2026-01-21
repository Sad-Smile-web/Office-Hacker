# create_sounds.py
import os
import numpy as np
from pathlib import Path
import wave
import struct

def create_dummy_sounds():
    """Создать простые звуки для игры"""
    sound_dir = Path("assets/sounds")
    sound_dir.mkdir(parents=True, exist_ok=True)
    
    print("Создание звуковых файлов...")
    
    # 1. typing.wav
    create_sine_wave(sound_dir / "typing.wav", 1200, 0.07)
    
    # 2. click.wav  
    create_sine_wave(sound_dir / "click.wav", 800, 0.1)
    
    # 3. success.wav
    create_sine_wave(sound_dir / "success.wav", 1200, 0.5, sweep_up=True)
    
    # 4. error.wav
    create_sine_wave(sound_dir / "error.wav", 400, 0.3, sweep_down=True)
    
    # 5. hack.wav
    create_complex_sound(sound_dir / "hack.wav", duration=2.0)
    
    # 6. scan.wav
    create_sweep_sound(sound_dir / "scan.wav", 500, 1500, 1.5)
    
    # 7. notification.wav
    create_two_tone(sound_dir / "notification.wav", 800, 1200, 0.3)
    
    # 8. startup.wav
    create_startup_sound(sound_dir / "startup.wav")
    
    # 9. shutdown.wav
    create_shutdown_sound(sound_dir / "shutdown.wav")
    
    # 10. background.wav (простой цикл)
    create_background_music(sound_dir / "background.wav")
    
    print("Все звуковые файлы созданы!")

def create_sine_wave(filepath, freq, duration, sweep_up=False, sweep_down=False):
    """Создать синусоидальную волну"""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    if sweep_up:
        # Восходящий тон
        freq_sweep = np.linspace(freq * 0.5, freq * 1.5, len(t))
        wave = 0.7 * np.sin(2 * np.pi * freq_sweep * t)
    elif sweep_down:
        # Нисходящий тон
        freq_sweep = np.linspace(freq * 1.5, freq * 0.5, len(t))
        wave = 0.7 * np.sin(2 * np.pi * freq_sweep * t)
    else:
        # Постоянный тон
        wave = 0.7 * np.sin(2 * np.pi * freq * t)
    
    # Огибающая
    envelope = np.exp(-t * 3) * (1 - np.exp(-t * 50))
    wave *= envelope
    
    # Стерео
    stereo = np.column_stack((wave, wave))
    
    # Сохраняем
    save_wave(filepath, stereo, sample_rate)

def create_sweep_sound(filepath, start_freq, end_freq, duration):
    """Создать sweeping звук"""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Sweep частоты
    freq = np.linspace(start_freq, end_freq, len(t))
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    
    # Огибающая
    envelope = np.exp(-t * 2) * (1 - np.exp(-t * 20))
    wave *= envelope
    
    # Стерео
    stereo = np.column_stack((wave, wave))
    
    save_wave(filepath, stereo, sample_rate)

def create_two_tone(filepath, freq1, freq2, duration):
    """Создать двухтональный звук"""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    wave1 = 0.4 * np.sin(2 * np.pi * freq1 * t)
    wave2 = 0.4 * np.sin(2 * np.pi * freq2 * t)
    
    # Второй тон появляется позже
    delay = int(sample_rate * duration * 0.3)
    wave2_padded = np.concatenate([np.zeros(delay), wave2[:len(wave2)-delay]])
    
    wave = wave1 + wave2_padded
    
    # Огибающая
    envelope = np.exp(-t * 4)
    wave *= envelope
    
    # Стерео
    stereo = np.column_stack((wave, wave))
    
    save_wave(filepath, stereo, sample_rate)

def create_complex_sound(filepath, duration=2.0):
    """Создать сложный звук взлома"""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Основной тон с изменяющейся частотой
    main_freq = 300 + 100 * np.sin(2 * np.pi * 2 * t)
    main_wave = 0.3 * np.sin(2 * np.pi * main_freq * t)
    
    # Высокочастотные пики
    high_wave = 0.1 * np.sin(2 * np.pi * 2000 * t) * np.random.random(len(t))
    
    # Низкочастотный ритм
    rhythm = 0.2 * np.sin(2 * np.pi * 5 * t)
    
    wave = main_wave + high_wave + rhythm
    
    # Огибающая
    envelope = np.exp(-t * 1) * (1 - np.exp(-t * 10))
    wave *= envelope
    
    # Стерео с небольшим разделением
    left = wave * 0.9
    right = wave * 1.1
    
    stereo = np.column_stack((left, right))
    
    save_wave(filepath, stereo, sample_rate)

def create_startup_sound(filepath):
    """Создать звук запуска"""
    sample_rate = 44100
    duration = 3.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Нарастающий гул
    freq_rise = np.linspace(50, 200, len(t))
    main_wave = 0.5 * np.sin(2 * np.pi * freq_rise * t)
    
    # Системные звуки
    system_sounds = []
    for i in range(5):
        start = i * 0.4
        if start < duration:
            idx_start = int(start * sample_rate)
            idx_end = min(idx_start + int(0.1 * sample_rate), len(t))
            if idx_end > idx_start:
                freq = 800 + i * 200
                sys_wave = 0.2 * np.sin(2 * np.pi * freq * t[idx_start:idx_end])
                system_sounds.append((idx_start, idx_end, sys_wave))
    
    # Добавляем системные звуки
    for idx_start, idx_end, sys_wave in system_sounds:
        main_wave[idx_start:idx_end] += sys_wave
    
    # Огибающая
    envelope = np.exp(-t * 0.5) * (1 - np.exp(-t * 10))
    main_wave *= envelope
    
    # Завершающий тон
    final_tone = 0.3 * np.sin(2 * np.pi * 1000 * t) * np.exp(-(t - 2.5) ** 2 * 100)
    main_wave += final_tone
    
    stereo = np.column_stack((main_wave, main_wave))
    save_wave(filepath, stereo, sample_rate)

def create_shutdown_sound(filepath):
    """Создать звук выключения"""
    sample_rate = 44100
    duration = 2.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Затухающий тон
    freq_fall = np.linspace(200, 50, len(t))
    main_wave = 0.4 * np.sin(2 * np.pi * freq_fall * t)
    
    # Огибающая
    envelope = np.exp(-t * 3)
    main_wave *= envelope
    
    # Финальный щелчок
    click = np.zeros(len(t))
    click[-int(0.05*sample_rate):] = 0.3 * np.random.random(int(0.05*sample_rate))
    
    wave = main_wave + click
    
    stereo = np.column_stack((wave, wave))
    save_wave(filepath, stereo, sample_rate)

def create_background_music(filepath):
    """Создать простую фоновую музыку"""
    sample_rate = 44100
    duration = 30.0  # 30 секунд для цикла
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Аккорды (Am, F, C, G)
    chords = [
        [220.00, 261.63, 329.63],  # A minor
        [174.61, 220.00, 261.63],  # F
        [261.63, 329.63, 392.00],  # C
        [196.00, 246.94, 293.66]   # G
    ]
    
    wave = np.zeros(len(t))
    
    # Каждый аккорд длится 2 секунды
    chord_duration = 2.0
    samples_per_chord = int(chord_duration * sample_rate)
    
    for i in range(4):
        start_idx = i * samples_per_chord
        end_idx = min(start_idx + samples_per_chord, len(t))
        
        if start_idx < len(t):
            chord_t = t[start_idx:end_idx] - t[start_idx]
            chord_wave = np.zeros(len(chord_t))
            
            for freq in chords[i]:
                chord_wave += 0.1 * np.sin(2 * np.pi * freq * chord_t)
            
            # Огибающая для плавного перехода
            env = np.exp(-chord_t * 0.5) * (1 - np.exp(-chord_t * 20))
            chord_wave *= env
            
            wave[start_idx:end_idx] = chord_wave
    
    # Басовый тон
    bass_freq = 55
    bass_wave = 0.05 * np.sin(2 * np.pi * bass_freq * t)
    wave += bass_wave
    
    # Мягкий бит каждую секунду
    for i in range(int(duration)):
        beat_start = i * sample_rate
        beat_end = min(beat_start + int(0.05 * sample_rate), len(t))
        if beat_start < len(t):
            beat = 0.1 * np.random.random(beat_end - beat_start)
            wave[beat_start:beat_end] += beat
    
    # Нормализуем
    max_val = np.max(np.abs(wave))
    if max_val > 0:
        wave = wave / max_val * 0.3
    
    stereo = np.column_stack((wave, wave))
    
    # Сохраняем как WAV
    save_wave(filepath, stereo, sample_rate)

def save_wave(filepath, stereo_array, sample_rate):
    """Сохранить звук в WAV файл с помощью wave модуля"""
    # Конвертируем в 16-битный PCM
    max_val = np.max(np.abs(stereo_array))
    if max_val > 0:
        stereo_array = stereo_array / max_val * 32767
    
    stereo_array = stereo_array.astype(np.int16)
    
    # Сохраняем с помощью wave модуля
    n_channels = 2  # стерео
    sampwidth = 2   # 16 бит = 2 байта
    
    with wave.open(str(filepath), 'w') as wav_file:
        wav_file.setnchannels(n_channels)
        wav_file.setsampwidth(sampwidth)
        wav_file.setframerate(sample_rate)
        
        # Преобразуем массив в байты
        frames = stereo_array.tobytes()
        wav_file.writeframes(frames)

if __name__ == "__main__":
    create_dummy_sounds()