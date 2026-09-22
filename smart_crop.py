from PIL import Image
import numpy as np


def smart_crop(image_path, output_path, padding=20, threshold=25,
               min_content_pixels=10, crop_right=False, right_padding=30):
    """
    Обрезка скриншота Discord-сообщения.

    Всегда обрезает пустое пространство сверху/снизу.
    Если crop_right=True, дополнительно обрезает пустое пространство справа
    (полезно для сообщений без вложений — убирает фон справа от текста).

    Args:
        image_path: путь к исходному изображению
        output_path: путь для сохранения результата
        padding: отступ от контента (px) по вертикали
        threshold: порог разницы с фоном для детекции контента
        min_content_pixels: мин. кол-во "контентных" пикселей
        crop_right: обрезать ли пустое пространство справа
        right_padding: отступ справа (px), больше padding
    """
    img = Image.open(image_path)
    pixels = np.array(img)
    height, width = pixels.shape[:2]

    # Автоопределение цвета фона по углам изображения
    corners = [
        pixels[0, 0], pixels[0, width - 1],
        pixels[height - 1, 0], pixels[height - 1, width - 1]
    ]
    bg_color = np.median(corners, axis=0).astype(np.uint8)[:3]

    # Маска: пиксели, отличающиеся от фона более чем на threshold в любом канале
    diff = np.abs(pixels[:, :, :3].astype(int) - bg_color.astype(int))
    mask = diff.max(axis=2) > threshold

    # Вертикальная обрезка (строки)
    row_content_counts = np.sum(mask, axis=1)
    rows_with_content = np.where(row_content_counts > min_content_pixels)[0]

    if len(rows_with_content) == 0:
        print("⚠️ Контент не найден, возвращаю оригинал")
        img.save(output_path)
        return img

    top = max(0, int(rows_with_content[0]) - padding)
    bottom = min(height, int(rows_with_content[-1]) + padding)

    # Горизонтальная обрезка (столбцы) — только если crop_right=True
    left = 0
    right = width

    if crop_right:
        col_threshold = max(min_content_pixels, height // 40)
        col_content_counts = np.sum(mask, axis=0)
        cols_with_content = np.where(col_content_counts > col_threshold)[0]
        if len(cols_with_content) > 0:
            right = min(width, int(cols_with_content[-1]) + right_padding)

    cropped = img.crop((left, top, right, bottom))
    cropped.save(output_path)

    print(f"✅ Обрезано: {height}px → {bottom - top}px (верх={top}, низ={bottom})"
          + (f", справа: {width}px → {right}px" if crop_right else ""))
    return cropped
