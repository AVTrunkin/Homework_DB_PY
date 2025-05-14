import psycopg2

def create_db():
    with psycopg2.connect(database="netology_db", user="postgres", password="Qwedsa66!") as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DROP TABLE clients CASCADE;
            DROP TABLE phones;
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                email VARCHAR(100) UNIQUE
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                phone_id SERIAL PRIMARY KEY,
                client_id INT REFERENCES clients(client_id) ON DELETE CASCADE,
                phone VARCHAR(15)
            );
            """)
            conn.commit()

def add_client(first_name, last_name, email):
    with psycopg2.connect(database="netology_db", user="postgres", password="Qwedsa66!") as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO clients (first_name, last_name, email)
                VALUES (%s, %s, %s);
                """, (first_name, last_name, email))
            conn.commit()
            # return cur.fetchone()[0]


def add_phone(client_id, phone):
    with psycopg2.connect(database="netology_db", user="postgres", password="Qwedsa66!") as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO phones (client_id, phone) 
            VALUES (%s, %s);
            """, (client_id, phone))
            conn.commit()

def change_client(client_id, first_name=None, last_name=None, email=None, phone=None):
    with psycopg2.connect(database="netology_db", user="postgres", password="Qwedsa66!") as conn:
        with conn.cursor() as cur:
            if first_name:
                cur.execute('UPDATE clients SET first_name = %s WHERE client_id = %s;', (first_name, client_id))
            if last_name:
                cur.execute('UPDATE clients SET last_name = %s WHERE client_id = %s;', (last_name, client_id))
            if email:
                cur.execute('UPDATE clients SET email = %s WHERE client_id = %s;', (email, client_id))
            # cur.execute("""
            # UPDATE clients SET first_name=%s, last_name=%s
            # WHERE id=%s;
            # """, (first_name, last_name, client_id))
            # cur.execute("""
            # SELECT * FROM clients;
            # """)
            # cur.execute("""
            # UPDATE phone_numbers SET phones=%s
            # WHERE client_id=%s;
            # """, (phones, client_id))
            # cur.execute("""
            # SELECT * FROM phone_numbers;
            # """)
            conn.commit()


def delete_phone(phone_id):
    with psycopg2.connect(database="netology_db", user="postgres", password="Qwedsa66!") as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DELETE FROM phones 
            WHERE phone_id=%s;
            """, (phone_id,))
            conn.commit()

def delete_client(client_id):
    with psycopg2.connect(database="netology_db", user="postgres", password="Qwedsa66!") as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DELETE FROM clients WHERE client_id=%s;
            """, (client_id,))
            conn.commit()

def find_client(first_name=None, last_name=None, email=None, phone=None):
    with psycopg2.connect(database="netology_db", user="postgres", password="Qwedsa66!") as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT clients.client_id, first_name, last_name, email 
            FROM clients
            LEFT JOIN phones ON clients.client_id = phones.client_id 
            WHERE first_name ILIKE %s OR last_name ILIKE %s 
            OR email ILIKE %s OR phone ILIKE %s;
            """, (f'%{first_name}%', f'%{last_name}%', f'%{email}%', f'%{phone}%'))
            return cur.fetchall()


if __name__ == '__main__':

    # Создаем структуру базы данных
    create_db()

    # Добавляем нового клиента
    client_id = add_client('Иван', 'Иванов', 'ivanov@mail.com')

    # Добавляем телефоны для этого клиента
    add_phone(client_id, '1234567890')
    add_phone(client_id, '0987654321')

    # Добавляем нового клиента
    client_id = add_client('Петр', 'Петров', 'petrov@mail.com')

    # Добавляем телефоны для этого клиента
    add_phone(client_id, '2345678901')
    add_phone(client_id, '3456789012')
    # Обновляем данные о клиенте
    change_client(client_id, email='ivanov_updated@mail.com')

    # Находим клиента по имени
    clients = find_client('Иван')
    print(clients)

    # Удаляем один из телефонов
    delete_phone(1)  # Укажите корректный ID телефона для удаления

    # Удаляем клиента
    delete_client(client_id)

