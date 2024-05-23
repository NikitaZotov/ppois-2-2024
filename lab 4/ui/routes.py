from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os

from core.brightness_controller import BrightnessController
from core.play_list import PlayList
from core.video_player import VideoPlayer
from core.volume_controller import VolumeController

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Initialize PlayList and VideoPlayer
playlist = PlayList()
video_player = VideoPlayer()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_to_queue', methods=['POST'])
def add_to_queue():
    if 'videoFile' not in request.files:
        return redirect(request.url)

    file = request.files['videoFile']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        playlist.add_to_queue(filepath)
        return redirect(url_for('index'))


@app.route('/play', methods=['POST'])
def play():
    queue_size = len(playlist.queue)
    while len(playlist.queue) != 0:
        video_to_play = playlist.get_video_to_play()
        if video_to_play is not None:
            video_player.play(video_to_play)
    if queue_size != 0:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/toggle_pause', methods=['POST'])
def toggle_pause():
    video_player.toggle_pause()
    if video_player.paused:
        return jsonify({'success': False})
    else:
        return jsonify({'success': True})


@app.route('/is_open', methods=['GET'])
def is_open():
    return jsonify({'open': video_player.video_player_is_open})

@app.route('/is_playing', methods=['GET'])
def is_playing():
    return jsonify({'playing': not video_player.paused})

@app.route('/is_queue_empty', methods=['GET'])
def is_queue_empty():
    return jsonify({'empty':  len(playlist.queue) == 0})

@app.route('/get_queue', methods=['GET'])
def get_queue_file_names():
    queue_file_names = [os.path.basename(file.file_path) for file in playlist.queue]
    return jsonify({'queue': queue_file_names})

@app.route('/get_current_video_file_name', methods=['GET'])
def get_current_video_file_name():
    if video_player.video_file is not None:
        current_video_file_name = os.path.basename(video_player.video_file.file_path)
        return jsonify({'name': current_video_file_name})
    else:
        return jsonify({'name': None})

@app.route('/save_queue', methods=['POST'])
def save_queue():
    try:
        playlist.save_playlist()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error saving queue: {e}")
        return jsonify({'success': False})

@app.route('/load_queue', methods=['POST'])
def load_queue():
    try:
        playlist.load_playlist()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error loading queue: {e}")
        return jsonify({'success': False})

@app.route('/set_brightness', methods=['POST'])
def set_brightness():
    data = request.get_json()
    brightness_level = int(data['brightness'])
    try:
        BrightnessController.set_brightness(brightness_level)
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error setting brightness: {e}")
        return (jsonify({'success': False}))


@app.route('/get_brightness', methods=['GET'])
def get_brightness():
    return jsonify({'brightness':  BrightnessController.get_brightness()})


@app.route('/set_volume', methods=['POST'])
def set_volume():
    data = request.get_json()
    volume_level = int(data['volume'])
    try:
        VolumeController.set_volume(volume_level)
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error setting brightness: {e}")
        return jsonify({'success': False})


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
