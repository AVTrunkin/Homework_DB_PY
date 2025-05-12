import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE clients CASCADE;
        DROP TABLE phone_numbers;
        """)
        cur.execute("""
        CREATE TABLE clients(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) UNIQUE NOT NULL,
            last_name VARCHAR(40) UNIQUE NOT NULL,
            email VARCHAR(40) UNIQUE NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE phone_numbers(
            client_id INTEGER REFERENCES clients (id),
            phones TEXT UNIQUE,
            location TEXT,
            PRIMARY KEY (client_id, phone_number)
        );
        """)


def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO clients (first_name, last_name, email)
            VALUES ('Иван', 'Иванов', 'qwerty@mail.ru'),
                    ('Петр', 'Петров', 'qwerty2@mail.ru'),
                    ('Сергей', 'Сергеев', 'qwerty3@mail.ru');
            """)
    return cur.fetchall()

def add_phone(conn, client_id, phones, location):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone_numbers (client_id, phones, location) 
        VALUES (1, '1234567890', 'mobile'),
                (1, '2345678901', 'work'),
                (2, '3456789012', 'mobile'),
                (3, '4567890123', 'mobile'), 
                (3, '5678901234', 'home'),
                (3, '6789012345', 'work');
        """)
    return cur.fetchall()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE clients SET first_name=%s, last_name=%s  
        WHERE id=%s;
        """, ('Семен', 'Семенов', 1))
        cur.execute("""
        SELECT * FROM clients;
        """)
        # print(cur.fetchall())

        cur.execute("""
        UPDATE phone_numbers SET phones=%s, location=%s  
        WHERE client_id=%s;
        """, ('87653907654', 'home', 2))
        cur.execute("""
        SELECT * FROM phone_numbers;
        """)
        # print(cur.fetchall())
    return cur.fetchall()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_numbers 
        WHERE client_id=%s;
        """, (2,))
        cur.execute("""
        SELECT * FROM phone_numbers;
        """)
        # print(cur.fetchall())
    return cur.fetchall()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
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
        # print(cur.fetchall())
    return cur.fetchall()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT first_name, last_name, email, phones 
        FROM clients, phone_numbers 
        WHERE first_name=%s;
        """, ('Петр',))
            # print(cur.fetchone())
        cur.execute("""
        SELECT first_name, last_name, email, phones 
        FROM clients, phone_numbers 
        WHERE last_name=%s;
        """, ('Семенов',))
            # print(cur.fetchone())
        cur.execute("""
        SELECT first_name, last_name, email, phones 
        FROM clients, phone_numbers 
        WHERE email=%s;
        """, ('qwerty3@mail.ru',))
            # print(cur.fetchone())
        cur.execute("""
        SELECT first_name, last_name, email, phones 
        FROM clients, phone_numbers 
        WHERE phones=%s;
        """, ('1234567890',))
    return cur.fetchone()


if __name__ == '__main__':
    with psycopg2.connect(database="netology_db", user="postgres", password="Qwedsa66!") as conn:
        print (add_client(conn,'иван', 'Иванов', 'qwerty2@mail.ru'))
        print (add_phone(conn, '1', '1234567890'))
        print (change_client (conn, '1', 'Jon', 'Varon', 'samual@mail.com'))
        print (delete_phone (conn, '1', '89109467816'))
        print (delete_client(conn, '1'))
        print (find_client(conn, 'Иванов'))




conn.close()