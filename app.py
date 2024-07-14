import os
import logging
from flask import Flask, request, jsonify
from google.cloud import storage
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Initialize Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/supercut', methods=['POST'])
def create_supercut():
    data = request.json
    video_url = data['video_url']
    timestamps = data['timestamps']
    output_url = data['output_url']

    logging.info("Received request for supercut")
    logging.info(f"Video URL: {video_url}")
    logging.info(f"Timestamps: {timestamps}")
    logging.info(f"Output URL: {output_url}")

    # Download video from cloud storage
    download_video(video_url, 'input_video.mp4')

    # Create supercut
    create_supercut_from_timestamps('input_video.mp4', timestamps, 'supercut.mp4')

    # Upload video to cloud storage
    upload_video('supercut.mp4', output_url)

    logging.info("Supercut creation completed successfully")
    return jsonify({'status': 'success', 'output_url': output_url})

def download_video(source_url, destination_file_name):
    logging.info(f"Downloading video from {source_url} to {destination_file_name}")
    storage_client = storage.Client()
    bucket_name, blob_name = source_url.replace("gs://", "").split("/", 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(destination_file_name)
    logging.info(f"Downloaded {source_url} to {destination_file_name}")

def upload_video(source_file_name, destination_url):
    logging.info(f"Uploading video from {source_file_name} to {destination_url}")
    storage_client = storage.Client()
    bucket_name, blob_name = destination_url.replace("gs://", "").split("/", 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(source_file_name)
    logging.info(f"Uploaded {source_file_name} to {destination_url}")

def create_supercut_from_timestamps(input_video_path, timestamps, output_video_path):
    logging.info("Creating supercut")
    logging.info(f"Input video path: {input_video_path}")
    logging.info(f"Timestamps: {timestamps}")
    logging.info(f"Output video path: {output_video_path}")

    clips = []
    with VideoFileClip(input_video_path) as video:
        for start_time, end_time in timestamps:
            logging.info(f"Creating clip from {start_time} to {end_time}")
            clip = video.subclip(start_time, end_time)
            clips.append(clip)
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_video_path)
    logging.info(f"Supercut saved to {output_video_path}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
