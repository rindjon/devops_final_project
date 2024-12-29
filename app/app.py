import os
from flask import Flask, render_template, send_file
import json
import boto3

def load_config(config_path):
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            configs['HEADER_MSG']  = config.get("welcome_message", "Welcome to Cars Photos Viewer!")
            configs['BUCKET_NAME'] = config.get("S3_bucket_name", "No bucket found")
            configs['AWS_ID']      = config.get("aws_access_key_id", "No access key found")
            configs['AWS_SECRET']  = config.get("aws_secret_access_key", "No secret key found")
            print(configs)
        return configs
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
        return None

configs = load_config("config.json")
if configs is None:
    print("Error: Config file not loaded. Exiting.")
#    exit

app = Flask(__name__)
try:
    session = boto3.Session(
        aws_access_key_id=configs['AWS_ID'],
        aws_secret_access_key=configs['AWS_SECRET'],
        region_name='us-east-1'
    )

    s3 = session.client('s3')
except Exception as e:
    print(f"Error creating S3 client: {e}")

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

    # welcome_message = load_config()
    photos_urls = get_s3_photos(configs['BUCKET_NAME'])

    return render_template("index.html", welcome_message=configs['HEADER_MSG'], photos_urls=photos_urls)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
