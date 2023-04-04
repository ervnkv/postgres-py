import psycopg2
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
        
    # TASK 1 - Get all subscribers w/o comments
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.name 
            FROM users u 
            WHERE u.id IN (SELECT s.subscriber_user_id FROM subscribers s) 
            AND u.id NOT IN (SELECT c.user_id FROM comments c)
        """)

        rows = cursor.fetchall()
        print('TASK #1 - All subscribers w/o comments: ',rows)

    # TASK 2 - Get 10 latest comments from subscribers to a given user.
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT comments.text
            FROM users
            JOIN subscribers ON users.id = subscribers.user_id
            JOIN comments ON subscribers.subscriber_user_id = comments.user_id
            WHERE users.name = %s
            ORDER BY comments.created DESC, comments.id DESC
            LIMIT 10;
        """, ('Oliver', ))
        # fetch all the rows
        rows = cursor.fetchall()

        print('TASK #2 - 10 latest comments from subscribers to a user: ',rows)

    # TASK 3 - Get 10 latest comments from subscribers to a given user (effective)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT comments.text
            FROM users
            JOIN LATERAL (
                SELECT *
                FROM subscribers
                WHERE users.id = subscribers.user_id
                LIMIT 1
            ) AS subscriber ON true
            JOIN comments ON subscriber.subscriber_user_id = comments.user_id
            WHERE users.name = %s
            ORDER BY comments.created DESC, comments.id DESC
            LIMIT 10;
        """, ('Oliver', ))
        # fetch all the rows
        rows = cursor.fetchall()

        print('TASK #3 - (effective) 10 latest comments from subscribers to a user: ',rows)

except Exception as ex:
    print('ERROR with PostgreSQL', ex)
finally:
    if connection:
        connection.close()
        print('Connection close')