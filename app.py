from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from lane.detect import detect_lanes
from database.db import init_db, log_upload
import os

UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video = request.files['video']
        filename = secure_filename(video.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"processed_{filename}")
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        video.save(filepath)
        detect_lanes(filepath, output_path)
        log_upload(filename)
        return render_template('index.html', video_url=output_path)
    return render_template('index.html', video_url=None)

if __name__ == '__main__':
    app.run(debug=True)
