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



    # create table 1 - users (id INT, name TEXT)
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE users(
                id SERIAL PRIMARY KEY,
                name TEXT)"""
        )
        print('Table users created')

    # create table 2 - subscribers (user_id INT, subscriber_user_id INT)
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE subscribers(
                user_id INT REFERENCES users(id),
                subscriber_user_id INT REFERENCES users(id),
                UNIQUE (user_id, subscriber_user_id))"""
        )
        print('Table subscribers created')

    # create table 3 - comments(id INT, user_id INT, text TEXT, created TIMESTAMPTZ)
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE comments(
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),
                text TEXT,
                created TIMESTAMPTZ)"""
        )
        print('Table comments created')
        


except Exception as ex:
    print('ERROR with PostgreSQL', ex)
finally:
    if connection:
        connection.close()
        print('Connection close')