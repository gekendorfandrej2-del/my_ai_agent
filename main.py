import os
from dotenv import load_dotenv
from gigachat import GigaChat
from agent import run_agent, AVAILABLE_TOOLS

load_dotenv()

client_secret = os.getenv("GIGACHAT_CLIENT_SECRET")
scope = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

if not client_secret:
    print("ОШИБКА: Не найден ключ в .env")
    exit(1)

print("Подключение к GigaChat...")

try:
    giga = GigaChat(
        credentials=client_secret,
        scope=scope,
        verify_ssl_certs=False,
        model="GigaChat-2"
    )
    print("Успешно подключено!")
    print("Напишите 'выход' для завершения.\n")
except Exception as e:
    print(f"Ошибка при подключении: {e}")
    exit(1)

chat_history = []

while True:
    try:
        user_input = input("Вы: ")
        
        if user_input.lower() in ["выход", "exit", "quit"]:
            print("До встречи!")
            break
        
        if not user_input.strip():
            continue

        answer = run_agent(giga, user_input, chat_history)
        if "удалить" in answer.lower() or "удаления" in answer.lower():
            confirm = input("⚠️  Подтвердите удаление (да/нет): ")
            if confirm.lower() in ["да", "yes", "y"]:
                from tools import confirm_and_delete
                # Извлекаем имена файлов из ответа (ищем строки с .png или .jpg)
                files = [line.split(" (")[0].strip() for line in answer.split("\n") if ".png" in line or ".jpg" in line]
                if files:
                    result = confirm_and_delete(files)
                    print(f"✅ {result}\n")
                else:
                    print("Не удалось извлечь имена файлов из ответа.\n")
            else:
                print("❌ Удаление отменено.\n")
        print(f"Агент: {answer}\n")

    except KeyboardInterrupt:
        print("\nЗавершение работы...")
        break
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}\n")
