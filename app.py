from flask import *
from pytube import YouTube
import os
import re

app = Flask(__name__)


path = os.getcwd() + '/output/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['link']
    if url.startswith('http://') or url.startswith('https://'):
        try:
            yt = YouTube(url)
            title = yt.title
            filename = re.sub(r'[^\w\s-]', '', title) + '.mp4'
            p = path + title + '.mp4'
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            video.download(path)
            return send_file(p, as_attachment=True)
            redirect(url_for('index.html')) 
        except Exception as e:
            flash('Error al descargar el video: ' + str(e))
    else:
        flash('URL no válida')


if __name__ == '__main__':
    app.run()

