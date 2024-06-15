import mysql.connector

class DB:
    def __init__(self):
        self.db_config = {
            'user': 'root',
            'password': 'ajay2105',
            'host': 'localhost',
            'database': 'matrimony_db'
        }
        self.connection = self.connect_to_db()
        self.cursor = self.connection.cursor()

    def connect_to_db(self):
        return mysql.connector.connect(**self.db_config)

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            username VARCHAR(50) PRIMARY KEY,
                            password VARCHAR(50),
                            name VARCHAR(50),
                            age INT,
                            gender VARCHAR(10),
                            interests TEXT,
                            profession VARCHAR(50),
                            company VARCHAR(50),
                            salary VARCHAR(50),
                            email VARCHAR(50),
                            city VARCHAR(50)
                          )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            sender VARCHAR(50),
                            recipient VARCHAR(50),
                            message_content TEXT,
                            timestamp DATETIME,
                            FOREIGN KEY (sender) REFERENCES users(username),
                            FOREIGN KEY (recipient) REFERENCES users(username)
                          )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS interests (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            recipient VARCHAR(50),
                            sender VARCHAR(50),
                            interest VARCHAR(50),
                            FOREIGN KEY (recipient) REFERENCES users(username),
                            FOREIGN KEY (sender) REFERENCES users(username)
                          )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS matches (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            user1_name VARCHAR(50),
                            user1_city VARCHAR(50),
                            user2_name VARCHAR(50),
                            user2_city VARCHAR(50)
                          )''')
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
