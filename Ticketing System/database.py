import sqlite3

def create_table():
    conn = sqlite3.connect('Reservation.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tickets (
            ticket_id INTEGER PRIMARY KEY,
            movie_name TEXT,
            ticket_quantity INTEGER,
            ticket_price INTEGER
        )''')

    conn.commit()
    conn.close()

def insert_Tickets():
    conn = sqlite3.connect('Reservation.db')
    cursor = conn.cursor()

    Tickets_data = [
        ('10', 'John Wick', 100, 175),
        ('11', 'Fast and Furious', 100, 175),
        ('12', 'Spiderman: Into Spiderverse', 100, 175),
        ('13', 'Mission Impossible: Dead Reckoning', 100, 175),
        ('14', 'Harry Potter', 100, 175),
        ('15', 'Mario Movie', 100, 175),
        ('16', 'DBZ: Movie', 100, 175)
    ]

    cursor.executemany('INSERT OR IGNORE INTO Tickets (ticket_id, movie_name, ticket_quantity, ticket_price) VALUES (?, ?, ?, ?)', Tickets_data)

    conn.commit()
    conn.close()


def get_tickets():
    conn = sqlite3.connect('Reservation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Tickets')
    tickets = cursor.fetchall()
    conn.close()

    return tickets

def update_quantity(id, reserved_quantity):
    conn = sqlite3.connect('Reservation.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE Tickets SET ticket_quantity = ticket_quantity - ? WHERE ticket_id = ?',(reserved_quantity, id))
    conn.commit()
    conn.close()

create_table()
insert_Tickets()