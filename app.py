from flask import *
from pytube import YouTube
import os
import re

app = Flask(__name__)

# Crear carpeta 'downloads' si no existe
downloads_folder = os.path.join(app.root_path, 'downloads')
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['link']
    yt = YouTube(url)
    title = yt.title
    filename = re.sub(r'[^\w\s-]', '', title) + '.mp4'
    filepath = os.path.join(downloads_folder, filename)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video.download(output_path=downloads_folder, filename=filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run()
