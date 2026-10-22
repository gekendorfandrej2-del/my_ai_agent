import subprocess
import os

def get_cache_size():
    """Узнает размер кэша apt в мегабайтах."""
    cache_dir = "/var/cache/apt/archives/"
    total_size = 0
    if os.path.exists(cache_dir):
        for dirpath, dirnames, filenames in os.walk(cache_dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024) # Переводим в МБ

def main():
    print("🧹 Подготовка к очистке кэша пакетов (apt)...")
    
    # 1. Показываем, сколько места занимает кэш
    size_before = get_cache_size()
    print(f"Текущий размер кэша: {size_before:.1f} МБ")
    
    if size_before == 0:
        print("Кэш уже пуст. Очистка не требуется.")
        return

    # 2. Запрашиваем подтверждение
    confirm = input("Вы уверены, что хотите очистить кэш? (да/нет): ")
    if confirm.lower() not in ["да", "yes", "y"]:
        print("Очистка отменена.")
        return

    # 3. Выполняем очистку через sudo
    print("Выполняется очистка... (возможно, потребуется ввести пароль администратора)")
    try:
        # Команда apt-get clean удаляет все скачанные пакеты из кэша
        subprocess.run(["sudo", "apt-get", "clean"], check=True)
        
        # Проверяем результат
        size_after = get_cache_size()
        freed = size_before - size_after
        print(f"✅ Очистка завершена!")
        print(f"Освобождено: {freed:.1f} МБ")
        print(f"Текущий размер кэша: {size_after:.1f} МБ")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при выполнении очистки: {e}")
    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()
