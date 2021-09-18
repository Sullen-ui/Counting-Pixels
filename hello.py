import os
from flask import Flask, request, redirect , url_for, flash
from flask.templating import render_template
from PIL import Image, ImageColor
import numpy as np

UPLOAD_FOLDER = './static/pic'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # проверим, передается ли в запросе файл 
        if 'file' not in request.files:
            # После перенаправления на страницу загрузки
            # покажем сообщение пользователю 
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # безопасно извлекаем оригинальное имя файла
            filename = file.filename
            # сохраняем файл
            path=(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(path)

            # Берем картинку и считаем белые и чёрные пиксели
            original = np.array(Image.open(path).convert('RGB')) 
            black = [0, 0, 0]
            white = [255, 255, 255]
            numblacks = numwhites = 0
            numblacks = np.count_nonzero(np.all(original==black, axis=2))
            numwhites = np.count_nonzero(np.all(original==white, axis=2))   
            return render_template ("index.html", black=numblacks, white=numwhites, path=path)

            #return redirect(url_for('countBW', name=path))
    return render_template ("index.html")



@app.route('/pixels', methods=['GET', 'POST'])
def countBW():
            if request.method == 'POST':
                path=request.args.get('name')
                original = np.array(Image.open(path).convert('RGB')) 
                black = [0, 0, 0]
                white = [255, 255, 255]
                numblacks = numwhites = 0
                numblacks = np.count_nonzero(np.all(original==black, axis=2))
                numwhites = np.count_nonzero(np.all(original==white, axis=2))   
            return render_template ("count.html", black=numblacks, white=numwhites)

if __name__ == '__main__':
    app.run() 

@app.route('/hex')
def countHex():
        
        original = np.array(Image.open("static/pic/dino.png").convert('RGB')) 
        
        hex=ImageColor.getrgb("#000000")
        
        numpixels = 0
        numpixels = np.count_nonzero(np.all(original==hex, axis=2))
        
        return render_template ("hex.html", hex=numpixels)

if __name__ == '__main__':
    app.run() 