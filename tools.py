import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

def get_disk_space():
    """Возвращает информацию о свободном месте на диске."""
    try:
        total, used, free = shutil.disk_usage("/")
        total_gb = total // (2**30)
        used_gb = used // (2**30)
        free_gb = free // (2**30)
        return f"Всего: {total_gb} ГБ, Занято: {used_gb} ГБ, Свободно: {free_gb} ГБ"
    except Exception as e:
        return f"Ошибка при получении места: {e}"

def find_old_screenshots(days=14):
    """Ищет файлы в папке Изображения старше указанного количества дней."""
    # Пробуем найти стандартную папку Изображения
    image_dir = Path.home() / "Изображения"
    if not image_dir.exists():
        image_dir = Path.home() / "Pictures"
    if not image_dir.exists():
        return "Папка с изображениями не найдена."
    
    cutoff_date = datetime.now() - timedelta(days=days)
    old_files = []
    
    try:
        for file in image_dir.iterdir():
            if file.is_file():
                # Берём дату последнего изменения файла
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                if mtime < cutoff_date:
                    # Проверяем, что это похоже на скриншот (по имени)
                    name_lower = file.name.lower()
                    if "screen" in name_lower or "снимок" in name_lower or "screenshot" in name_lower:
                        size_mb = file.stat().st_size / (1024 * 1024)
                        old_files.append(f"{file.name} (изменён {mtime.strftime('%d.%m.%Y')}, {size_mb:.1f} МБ)")
        
        if not old_files:
            return "Старых скриншотов не найдено."
        
        result = f"Найдено старых скриншотов ({len(old_files)}):\n"
        result += "\n".join(old_files)
        return result
    except Exception as e:
        return f"Ошибка при поиске файлов: {e}"

def get_largest_files(limit=5):
    """Находит самые большие файлы в домашней папке."""
    home_dir = Path.home()
    file_sizes = []
    
    try:
        # Ищем файлы (не заходя в системные папки и скрытые)
        for root, dirs, files in os.walk(home_dir):
            # Пропускаем скрытые папки (начинаются с точки)
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for f in files:
                filepath = Path(root) / f
                try:
                    if filepath.is_file():
                        size = filepath.stat().st_size
                        file_sizes.append((size, filepath))
                except (PermissionError, OSError):
                    continue
                    
        # Сортируем по убыванию размера и берём топ
        file_sizes.sort(reverse=True, key=lambda x: x[0])
        
        result = f"Топ {limit} самых больших файлов:\n"
        for size, path in file_sizes[:limit]:
            size_mb = size / (1024 * 1024)
            # Сокращаем путь для красоты
            short_path = str(path).replace(str(Path.home()), "~")
            result += f"{short_path} — {size_mb:.1f} МБ\n"
        return result
    except Exception as e:
        return f"Ошибка при поиске больших файлов: {e}"
