from flask import *
from pytube import YouTube
import os
import re
import threading

app = Flask(__name__)

app.secret_key = 'tu_clave_secreta_aqui'

path = os.path.join(app.root_path, 'output')

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
            filepath = os.path.join(path, filename)
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            print('hasta aqui llega')
            video.download(path)
            threading.Timer(3, delete_files, args=[path]).start()
            return send_file(filepath, as_attachment=True)
        except Exception as e:
            flash('Error al descargar el video: ' + str(e))
    else:
        flash('URL no válida')
    return redirect(url_for('index')) 

def delete_files(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run()

