from app import mysql

def init_db():
    cursor = mysql.connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task VARCHAR(255) NOT NULL
        )
    ''')
    mysql.connection.commit()
