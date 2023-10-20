import os
from flask import Flask, request, render_template
from flask_cors import CORS
from paddleocr import PaddleOCR
import codecs


app = Flask(__name__)
CORS(app)



def getPrediction(img, save_name):
    ocr = PaddleOCR()
    results = ocr.ocr(img)
    for result in results[0]:
        _, (text, confidence) = result
        with open(f'./{save_name}.txt', 'a', encoding='gbk') as f:
            f.write(text + '\n')


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        uploaded_image = request.files['image']
        img_bytes = uploaded_image.read()
        save_name = uploaded_image.filename[:uploaded_image.filename.rfind('.')]

        if os.path.exists(f'./{save_name}.txt'):
            return {
                'msg': 'Please change the image file name and do not need to change the suffix, otherwise the recognized text content will be duplicated'
            }

        if uploaded_image.filename != '':
            getPrediction(img_bytes, save_name)
            try:
                with codecs.open(f"./{save_name}.txt", "r", encoding="gbk") as file:

                    content = file.read()
                return render_template("index.html", content=content)
            except FileNotFoundError:
                return "文件未找到"

    return 'No image uploaded.'

if __name__ == '__main__':
    app.run('0.0.0.0', port=15009, debug=True)