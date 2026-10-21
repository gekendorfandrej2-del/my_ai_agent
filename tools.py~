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
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                if mtime < cutoff_date:
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
        for root, dirs, files in os.walk(home_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for f in files:
                filepath = Path(root) / f
                try:
                    if filepath.is_file():
                        size = filepath.stat().st_size
                        file_sizes.append((size, filepath))
                except (PermissionError, OSError):
                    continue
                    
        file_sizes.sort(reverse=True, key=lambda x: x[0])
        
        result = f"Топ {limit} самых больших файлов:\n"
        for size, path in file_sizes[:limit]:
            size_mb = size / (1024 * 1024)
            short_path = str(path).replace(str(Path.home()), "~")
            result += f"{short_path} — {size_mb:.1f} МБ\n"
        return result
    except Exception as e:
        return f"Ошибка при поиске больших файлов: {e}"

def delete_old_screenshots(days=14):
    """Удаляет старые скриншоты (с подтверждением в main.py)."""
    image_dir = Path.home() / "Изображения"
    if not image_dir.exists():
        image_dir = Path.home() / "Pictures"
    if not image_dir.exists():
        return "Папка с изображениями не найдена."
    
    cutoff_date = datetime.now() - timedelta(days=days)
    deleted_names = []
    
    try:
        for file in image_dir.iterdir():
            if file.is_file():
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                if mtime < cutoff_date:
                    name_lower = file.name.lower()
                    if "screen" in name_lower or "снимок" in name_lower or "screenshot" in name_lower:
                        deleted_names.append(file.name)
        
        if not deleted_names:
            return "Файлов для удаления не найдено."
        
        return f"Найдено {len(deleted_names)} файлов для удаления:\n" + "\n".join(deleted_names)
    except Exception as e:
        return f"Ошибка при поиске: {e}"

def confirm_and_delete(files_to_delete):
    """
    Удаляет файлы из списка, если они находятся в папке Изображения.
    Это защита: функция не удалит файлы из других папок.
    """
    image_dir = Path.home() / "Изображения"
    if not image_dir.exists():
        image_dir = Path.home() / "Pictures"
    
    deleted_count = 0
    errors = []
    
    for filename in files_to_delete:
        filepath = image_dir / filename
        if filepath.exists() and filepath.is_file():
            try:
                filepath.unlink()
                deleted_count += 1
            except Exception as e:
                errors.append(f"{filename}: {e}")
        else:
            errors.append(f"{filename}: файл не найден")
    
    if errors:
        return f"Удалено: {deleted_count}. Ошибки: {'; '.join(errors)}"
    return f"Успешно удалено файлов: {deleted_count}."
