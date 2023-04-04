# Инициализация проекта
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt

# Настройка проекта
В файле config.py прописать параметры базы данных PostgresSQL

# Использование
## 1. generate_tables.py
Создает 3 таблицы в базе данных:
- users (id INT, name TEXT)

        ID пользователя, 
        Имя пользователя
- subscribers (user_id INT, subscriber_user_id INT)

        ID пользователя, 
        ID его подписчика
- comments (id INT, user_id INT, text TEXT, created TIMESTAMPTZ)

        ID комментария,
        ID пользователя, который его оставил,
        Текст комментария,
        Дата создания комментария

## 2. generate_rows.py
Заполняет 3 таблицы данными:
- users (id INT, name TEXT) 
 
        Добавляет пользователей из переменной NAMES
    
- subscribers (user_id INT, subscriber_user_id INT)

        Добавляет пользователей и подписчиков, так чтобы ID подписчика было больше ID пользователя
        
- comments (id INT, user_id INT, text TEXT, created TIMESTAMPTZ)
 
        Добавляет по 20 комментариев для пользователей, начиная с ID=4

## 3. main.py
Выполняет 3 SQL запроса к таблицам (три задачи):
- TASK 1. Напишите запрос, который бы вывел всех подписчиков без единого комментария.
- TASK 2. Напишите запрос, который возвращает десять последних комментариев подписчиков заданного пользователя.
- TASK 3. Перепишите запрос из задания 2, который работает эффективнее, если бы количество пользователей и их комментариев было очень большим (подзапрос LATERAL).


