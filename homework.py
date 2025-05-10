import psycopg2


with psycopg2.connect(database='netology_db', user='postgres', password='Qwedsa66!') as conn:
    with conn.cursor() as cur:
        # удаление таблиц
        cur.execute("""
        DROP TABLE clients CASCADE;
        DROP TABLE phone_numbers;
        """)

        # создание таблиц
        cur.execute("""
        CREATE TABLE clients(
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(40) UNIQUE NOT NULL,
            lastname VARCHAR(40) UNIQUE NOT NULL,
            email VARCHAR(40) UNIQUE NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE phone_numbers(
            client_id INTEGER REFERENCES clients (id),
            phone_number TEXT UNIQUE NOT NULL,
            location TEXT NOT NULL,
            PRIMARY KEY (client_id, phone_number)
        );
        """)
        conn.commit()  # фиксируем в БД

        # наполнение таблиц (C из CRUD)
        cur.execute("""
        INSERT INTO clients (firstname, lastname, email) 
        VALUES ('Иван', 'Иванов', 'qwerty@mail.ru'), 
               ('Петр', 'Петров', 'qwerty2@mail.ru'),
               ('Сергей', 'Сергеев', 'qwerty3@mail.ru');
        """)

        cur.execute("""
        INSERT INTO phone_numbers (client_id, phone_number, location) 
        VALUES (1, '1234567890', 'mobile'),
               (1, '2345678901', 'work'),
               (2, '3456789012', 'mobile'),
               (3, '4567890123', 'mobile'), 
               (3, '5678901234', 'home'),
               (3, '6789012345', 'work');
        """)
        conn.commit()  # фиксируем в БД

        # обновление данных
        cur.execute("""
        UPDATE clients SET firstname=%s, lastname=%s  
        WHERE id=%s;
        """, ('Семен', 'Семенов', 1))
        cur.execute("""
        SELECT * FROM clients;
        """)
        print(cur.fetchall())

        cur.execute("""
        UPDATE phone_numbers SET phone_number=%s, location=%s  
        WHERE client_id=%s;
        """, ('87653907654', 'home', 2))
        cur.execute("""
        SELECT * FROM phone_numbers;
        """)
        print(cur.fetchall())

    # удаление данных
        cur.execute("""
        DELETE FROM phone_numbers 
        WHERE client_id=%s;
        """, (2,))
        cur.execute("""
        SELECT * FROM phone_numbers;
        """)
        print(cur.fetchall())  # запрос данных автоматически зафиксирует изменения

        cur.execute("""
        DELETE FROM phone_numbers 
        WHERE client_id=%s;
        """, (1,))
        cur.execute("""
        DELETE FROM clients WHERE id=%s;
        """, (1,))
        cur.execute("""
        SELECT * FROM clients;
        """)
        print(cur.fetchall())  # запрос данных автоматически зафиксирует изменения

    # поиск
        cur.execute("""
        SELECT firstname, lastname, email, phone_number 
        FROM clients, phone_numbers 
        WHERE firstname=%s;
        """, ('Петр',))
        print(cur.fetchone())
        cur.execute("""
        SELECT firstname, lastname, email, phone_number 
        FROM clients, phone_numbers 
        WHERE lastname=%s;
        """, ('Семенов',))
        print(cur.fetchone())
        cur.execute("""
        SELECT firstname, lastname, email, phone_number 
        FROM clients, phone_numbers 
        WHERE email=%s;
        """, ('qwerty3@mail.ru',))
        print(cur.fetchone())
        cur.execute("""
        SELECT firstname, lastname, email, phone_number 
        FROM clients, phone_numbers 
        WHERE phone_number=%s;
        """, ('1234567890',))
        print(cur.fetchone())

conn.close()