import os
from flask import Flask, render_template, send_file
import json
import boto3

def load_config(config_path="config.json"):
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
        return config.get("welcome_message", "Welcome to Cars Photos Viewer!")
    except FileNotFoundError:
        return "Welcome to Cars Photos Viewer!"


# load_config("config.json")
# if len(configs) is 0:
#     print("Error: Config file not loaded. Exiting.")


app = Flask(__name__)

# session = boto3.Session(
#     aws_access_key_id=configs['AWS_ID'],
#     aws_secret_access_key=configs['AWS_SECRET'],
#     region_name='us-east-1'
# )

try:
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET'),
        region_name='us-east-1'
    )
except Exception as e:
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
    # Local folder path
    # folder_path = os.getenv("PHOTO_FOLDER", "photos")

    welcome_message = load_config()
    photos_urls = get_s3_photos('devops-final-project-photos')
    # photos_urls = []

    return render_template("index.html", welcome_message=welcome_message, photos_urls=photos_urls)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
