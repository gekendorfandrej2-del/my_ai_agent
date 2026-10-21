import sys
import io
from datetime import datetime
from pathlib import Path
import os

# Импортируем наши уже готовые инструменты
from tools import get_disk_space, find_old_screenshots, get_largest_files

def main():
    # Устанавливаем кодировку для вывода (чтобы русские буквы не ломались при запуске из cron)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    report_lines = []
    
    # 1. Заголовок с датой
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    report_lines.append(f"📊 ОТЧЕТ О СОСТОЯНИИ СИСТЕМЫ (от {now})")
    report_lines.append("=" * 50)
    
    # 2. Место на диске
    report_lines.append("\n💾 МЕСТО НА ДИСКЕ:")
    report_lines.append(get_disk_space())
    
    # 3. Старые скриншоты
    report_lines.append("\n🖼️  СТАРЫЕ СКРИНШОТЫ (старше 14 дней):")
    screenshots = find_old_screenshots()
    if "Найдено" in screenshots:
        # Если скринов много, выводим только первые 5 для краткости
        lines = screenshots.split("\n")
        if len(lines) > 6:
            report_lines.append("\n".join(lines[:6]))
            report_lines.append(f"... и еще {len(lines) - 6} файлов.")
        else:
            report_lines.append(screenshots)
    else:
        report_lines.append(screenshots)
        
    # 4. Самые большие файлы
    report_lines.append("\n📦 САМЫЕ БОЛЬШИЕ ФАЙЛЫ (Топ-5):")
    report_lines.append(get_largest_files(5))
    
    # 5. Новые файлы за последние 7 дней
    report_lines.append("\n🆕 НОВЫЕ ФАЙЛЫ ЗА ПОСЛЕДНИЕ 7 ДНЕЙ:")
    home_dir = Path.home()
    new_files = []
    cutoff = datetime.now().timestamp() - (7 * 24 * 60 * 60) # 7 дней назад
    
    # Ищем в рабочих папках (Документы, Загрузки, Рабочий стол)
    folders_to_check = [home_dir / "Документы", home_dir / "Загрузки", home_dir / "Рабочий стол"]
    for folder in folders_to_check:
        if folder.exists():
            for file in folder.rglob("*"):
                if file.is_file() and file.stat().st_mtime > cutoff:
                    new_files.append(str(file).replace(str(home_dir), "~"))
    
    if new_files:
        report_lines.append(f"Найдено {len(new_files)} новых файлов. Вот первые 5:")
        for f in new_files[:5]:
            report_lines.append(f" - {f}")
    else:
        report_lines.append("Новых файлов не найдено.")

    # Сохраняем отчет в файл
    report_text = "\n".join(report_lines)
    report_path = home_dir / "ai_agent" / "last_report.txt"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
        
    print(f"Отчет успешно сохранен в: {report_path}")
    print(report_text)

if __name__ == "__main__":
    main()
