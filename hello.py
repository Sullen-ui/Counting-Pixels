import os
from flask import Flask, request
from flask.templating import render_template
from PIL import Image
import numpy as np

UPLOAD_FOLDER = './static/pic'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        return ("Файл успешно загружен!")

       
    return render_template ("index.html")

if __name__ == '__main__':
    app.run()  

@app.route('/pixels')
def countBW():
      
        original = np.array(Image.open("static/pic/pixel.jpg").convert('RGB')) 
        
        black = [0, 0, 0]
        white = [255, 255, 255]
        numblacks = numwhites = 0
        numblacks = np.count_nonzero(np.all(original==black, axis=2))
        numwhites = np.count_nonzero(np.all(original==white, axis=2))
        
        #return numblacks,numwhites
        return render_template ("count.html", black=numblacks, white=numwhites)

if __name__ == '__main__':
    app.run() 