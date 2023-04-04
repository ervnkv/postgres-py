import psycopg2
from itertools import combinations
from datetime import datetime
from config import host, user, password, db_name, port

try:
    # connect to exist database
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        dbname=db_name,
        port=port
    )
    connection.autocommit = True
    
    # the cursor for performing database operations
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f'Server version: {cursor.fetchone()}')


    names = ["Sophia","Jackson","Olivia","Liam","Emma","Noah","Ava","Oliver","Isabella"]
    # Insert users into the "users" table from data.py
    with connection.cursor() as cursor:
        for user_name in names:
            cursor.execute("""
                INSERT INTO users (name)
                VALUES (%s)
            """, (user_name,))
        print('Users added')


    # Generate all combinations of users
    user_combinations = list(combinations(names, 2))
    # Insert subscribers into the "subscribers" table
    with connection.cursor() as cursor:
        for user1, user2 in user_combinations:
            cursor.execute("""
                INSERT INTO subscribers (user_id, subscriber_user_id)
                SELECT u1.id, u2.id
                FROM users u1, users u2
                WHERE u1.name = %s AND u2.name = %s
            """, (user1, user2))
        print('Subscribers added')


    # Insert comments into the "comments" table
    with connection.cursor() as cursor:
        for i in range(3, len(names)):
            user_name = names[i]
            for j in range(20):
                cursor.execute("""
                    INSERT INTO comments (user_id, text, created)
                    SELECT id, %s, %s
                    FROM users
                    WHERE name = %s
                """, (f"Comment {j+1}", datetime.now(), user_name))
        print('Comments added')

except Exception as ex:
    print('ERROR with PostgreSQL', ex)
finally:
    if connection:
        connection.close()
        print('Connection close')
