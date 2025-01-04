
from flask import Flask, render_template, request
import pymysql
import time

app = Flask(__name__)

# MySQL connection configuration
DB_HOST = "mysql"
DB_USER = "root"
DB_PASSWORD = "password"
DB_NAME = "logs_db"

# Function to insert data into the database
def insert_into_db(data):
    retries = 5
    while retries > 0:
        try:
            connection = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS logs (id INT AUTO_INCREMENT PRIMARY KEY, input_data TEXT)")
            cursor.execute("INSERT INTO logs (input_data) VALUES (%s)", (data,))
            connection.commit()
            break
        except pymysql.MySQLError as err:
            print(f"Error: {err}. Retrying...")
            time.sleep(5)
            retries -= 1
        finally:
            if 'connection' in locals():
                cursor.close()
                connection.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['user_input']
        insert_into_db(user_input)
        return "<h3>Data inserted successfully!</h3><a href='/'>Go back</a>"
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
