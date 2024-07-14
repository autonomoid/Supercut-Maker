import os
from flask import Flask, request, jsonify
from google.cloud import storage
from moviepy.editor import VideoFileClip, concatenate_videoclips

app = Flask(__name__)

@app.route('/supercut', methods=['POST'])
def create_supercut():
    data = request.json
    video_url = data['video_url']
    timestamps = data['timestamps']
    output_url = data['output_url']

    # Download video from cloud storage
    download_video(video_url, 'input_video.mp4')

    # Create supercut
    create_supercut_from_timestamps('input_video.mp4', timestamps, 'output_video.mp4')

    # Upload video to cloud storage
    upload_video('output_video.mp4', output_url)

    return jsonify({'status': 'success', 'output_url': output_url})

def download_video(source_url, destination_file_name):
    storage_client = storage.Client()
    bucket_name, blob_name = source_url.replace("gs://", "").split("/", 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Downloaded {source_url} to {destination_file_name}")

def upload_video(source_file_name, destination_url):
    storage_client = storage.Client()
    bucket_name, blob_name = destination_url.replace("gs://", "").split("/", 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"Uploaded {source_file_name} to {destination_url}")

def create_supercut_from_timestamps(input_video_path, timestamps, output_video_path):
    clips = []
    with VideoFileClip(input_video_path) as video:
        for start_time, end_time in timestamps:
            clip = video.subclip(start_time, end_time)
            clips.append(clip)
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_video_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)