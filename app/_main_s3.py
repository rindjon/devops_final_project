import os
from flask import Flask, render_template, send_file
import boto3
import json

app = Flask(__name__)

# Function to load the configuration file
def load_config(config_path="config.json"):
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
        return config.get("S3_bucket_name", "devops-final-project-bucket")
    except FileNotFoundError:
        return None

# Function to get photos from a local folder
def get_image_urls(S3_bucket_name, folder_path=""):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=S3_bucket_name, Prefix=folder_path)
    if 'Contents' not in response:
        print(f"No objects found in bucket '{S3_bucket_name}' with prefix '{folder_path}'.")
        return []

    image_urls = []
    for obj in response['Contents']:
        file_key = obj['Key']
        if file_key.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_bucket_name, 'Key': file_key},
                ExpiresIn=3600
            )
            image_urls.append(url)

    return image_urls

@app.route("/")
def index():
    # default folder path
    folder_path = os.getenv("PHOTO_FOLDER", "")

    S3_bucket_name = load_config()
    photos = get_image_urls(S3_bucket_name, folder_path)

    return render_template("index.html", welcome_message="Welcome to Your Photo Viewer", photos=photos)

# @app.route("/photo/<path:photo_key>")
# def photo(photo_key):
#     folder_path = os.getenv("PHOTO_FOLDER", "photos")
#     file_path = os.path.join(folder_path, photo_key)
#     if os.path.exists(file_path):
#         return send_file(file_path, mimetype="image/jpeg")
#     return "Error: Photo not found.", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
