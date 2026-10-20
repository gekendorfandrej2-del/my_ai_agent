import os
from dotenv import load_dotenv
from gigachat import GigaChat
from agent import run_agent

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
    print("Успешно подключено! Я умею проверять место на диске и искать старые скриншоты.")
    print("Напишите 'выход' для завершения.\n")
except Exception as e:
    print(f"Ошибка при подключении: {e}")
    exit(1)

# История диалога (хранит все сообщения, чтобы агент помнил контекст)
chat_history = []

# Основной цикл
while True:
    try:
        user_input = input("Вы: ")
        
        if user_input.lower() in ["выход", "exit", "quit"]:
            print("До встречи!")
            break
        
        if not user_input.strip():
            continue

        # Передаём управление агенту
        answer = run_agent(giga, user_input, chat_history)
        print(f"Агент: {answer}\n")

    except KeyboardInterrupt:
        print("\nЗавершение работы...")
        break
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}\n")
