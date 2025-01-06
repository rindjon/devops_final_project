import os
from flask import Flask, render_template, send_file
import json
import boto3
import pymysql

# MySQL connection configuration
DB_HOST = "mysql"  # Use the service name defined in service.yaml
DB_USER = "root"
DB_PASSWORD = "password"  # Match MYSQL_ROOT_PASSWORD in StatefulSet
DB_NAME = "logs_db"  # Match MYSQL_DATABASE in StatefulSet

# Function to insert data into the database
def insert_into_db(data):
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
    except pymysql.MySQLError as err:
        print(f"Error: {err}")
    finally:
        if connection:
            cursor.close()
            connection.close()

app = Flask(__name__)

print(os.getenv('AWS_ID', 'aws_id not found'))
print(os.getenv('AWS_SECRET', 'aws_id not found'))

try:
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET'),
        region_name='us-east-1'
    )
except Exception as e:
    print(f"Error creating S3 client: {e}")
    s3 = boto3.client(
        's3',
        region_name='us-east-1'
    )

def get_s3_photos(bucket_name):
    try:
        photos = s3.list_objects_v2(Bucket=bucket_name).get('Contents', [])
        print(f'photos: {photos}')
        photo_urls = [f"https://{bucket_name}.s3.us-east-1.amazonaws.com/{photo['Key']}" for photo in photos]
        return photo_urls
    except Exception as e:
        print(f"Error retrieving files from S3: {e}")
        return []

@app.route("/")
def index():
    insert_into_db("test test")
    photos_urls = get_s3_photos('devops-final-project-photos')

    return render_template("index.html", welcome_message="This is our cars photos viewer app", photos_urls=photos_urls)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
