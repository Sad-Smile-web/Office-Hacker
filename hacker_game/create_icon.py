# create_icon.py
from PIL import Image, ImageDraw
import os

def create_icon():
    """Создать иконку для игры"""
    
    # Создаем изображение 256x256
    img = Image.new('RGB', (256, 256), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Рисуем зеленый символ хакера
    draw.rectangle([64, 64, 192, 192], outline=(0, 255, 0), width=8)
    draw.line([96, 96, 160, 160], fill=(0, 255, 0), width=8)
    draw.line([160, 96, 96, 160], fill=(0, 255, 0), width=8)
    draw.text((128, 128), "H", fill=(0, 255, 0), anchor="mm")
    
    # Сохраняем в разных форматах
    os.makedirs("assets/icons", exist_ok=True)
    img.save("assets/icons/hack_icon.png")
    
    # Создаем ICO файл
    img.save("assets/icons/hack_icon.ico", format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
    
    print("[УСПЕХ] Иконки созданы в assets/icons/")

if __name__ == "__main__":
    create_icon()