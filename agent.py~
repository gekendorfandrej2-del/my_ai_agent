import json
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole, Function, FunctionParameters
from tools import get_disk_space, find_old_screenshots, get_largest_files, confirm_and_delete, list_directory, delete_item, find_new_files

AVAILABLE_TOOLS = {
    "get_disk_space": get_disk_space,
    "find_old_screenshots": find_old_screenshots,
    "get_largest_files": get_largest_files,
    "confirm_and_delete": confirm_and_delete,
    "list_directory": list_directory,
    "delete_item": delete_item,
    "find_new_files": find_new_files,
}

def get_tool_descriptions():
    return [
        Function(
            name="get_disk_space",
            description="Узнаёт, сколько всего, занято и свободно места на диске.",
            parameters=FunctionParameters(type="object", properties={}, required=[])
        ),
        Function(
            name="find_old_screenshots",
            description="Ищет старые скриншоты (старше 14 дней) в папке Изображения и показывает их список.",
            parameters=FunctionParameters(type="object", properties={}, required=[])
        ),
        Function(
            name="get_largest_files",
            description="Показывает список самых больших файлов в домашней папке.",
            parameters=FunctionParameters(
                type="object",
                properties={"limit": {"type": "integer", "description": "Сколько файлов показать"}},
                required=[]
            )
        ),
        Function(
            name="confirm_and_delete",
            description="Удаляет указанные файлы из папки Изображения. Вызывай эту функцию, когда пользователь подтверждает удаление.",
            parameters=FunctionParameters(
                type="object",
                properties={
                    "files_to_delete": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Список имён файлов для удаления"
                    }
                },
                required=["files_to_delete"]
            )
        ),
                Function(
            name="list_directory",
            description="Показывает список файлов и папок в указанном каталоге.",
            parameters=FunctionParameters(
                type="object",
                properties={
                    "dir_path": {"type": "string", "description": "Путь к каталогу (например, '~/Загрузки' или '~/Документы')"}
                },
                required=["dir_path"]
            )
        ),
        Function(
            name="delete_item",
            description="Удаляет файл или папку по указанному пути. Вызывать ТОЛЬКО после того, как пользователь подтвердил удаление.",
            parameters=FunctionParameters(
                type="object",
                properties={
                    "item_path": {"type": "string", "description": "Полный путь к файлу или папке для удаления"}
                },
                required=["item_path"]
            )
        ),
        Function(
            name="find_new_files",
            description="Ищет новые файлы (созданные или измененные) за последние несколько дней в папках Документы, Загрузки и Рабочий стол.",
            parameters=FunctionParameters(
                type="object",
                properties={
                    "days": {"type": "integer", "description": "За сколько дней искать (по умолчанию 7)"}
                },
                required=[]
            )
        )
    ]
def run_agent(giga: GigaChat, user_message: str, chat_history: list) -> str:
    chat_history.append(Messages(role=MessagesRole.USER, content=user_message))
    
    payload = Chat(
        messages=chat_history,
        function_call="auto",
        functions=get_tool_descriptions(),
        model="GigaChat-2"
    )
    
    response = giga.chat(payload)
    
    if response.choices[0].finish_reason == "function_call":
        function_call = response.choices[0].message.function_call
        function_name = function_call.name
        
        # --- ПРАВИЛЬНАЯ ОБРАБОТКА АРГУМЕНТОВ ---
        raw_args = function_call.arguments
        if raw_args is None:
            arguments = {}
        elif isinstance(raw_args, dict):
            arguments = raw_args
        else:
            arguments = json.loads(raw_args)
        # ---------------------------------------

        print(f"[Агент решил использовать инструмент: {function_name}]")

        if function_name == "confirm_and_delete":
            confirm = input("⚠️  Вы уверены, что хотите удалить эти файлы? (да/нет): ")
            if confirm.lower() not in ["да", "yes", "y"]:
                return "Удаление отменено пользователем."

                # Проверка для удаления конкретного файла/папки
        if function_name == "delete_item":
            confirm = input(f"⚠️  Вы уверены, что хотите удалить '{arguments.get('item_path')}'? (да/нет): ")
            if confirm.lower() not in ["да", "yes", "y"]:
                return "Удаление отменено пользователем."    


        if function_name in AVAILABLE_TOOLS:
            try:
                if arguments:
                    result = AVAILABLE_TOOLS[function_name](**arguments)
                else:
                    result = AVAILABLE_TOOLS[function_name]()
            except Exception as e:
                result = f"Ошибка при выполнении {function_name}: {e}"
        else:
            result = f"Неизвестный инструмент: {function_name}"
        
        chat_history.append(response.choices[0].message)
        result_json = json.dumps({"result": str(result)}, ensure_ascii=False)
        chat_history.append(Messages(role=MessagesRole.FUNCTION, content=result_json, name=function_name))
        
        final_payload = Chat(messages=chat_history, function_call="none", model="GigaChat-2")
        final_response = giga.chat(final_payload)
        final_answer = final_response.choices[0].message.content
        
        chat_history.append(final_response.choices[0].message)
        return final_answer
    else:
        answer = response.choices[0].message.content
        chat_history.append(response.choices[0].message)
        return answer
