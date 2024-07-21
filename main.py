from flask import Flask, render_template, request, redirect, url_for, send_from_directory 
import os
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'processed/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
ALLOWED_EXTENSIONS = {'xlsx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def upload_files():
    if request.method =='POST':
        if 'file[]' not in request.files:
            return redirect(request.url)
        
        files = request.files.getlist('file[]')

        for file in files:
            if file.filename == '':
                continue
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('upload_files'))
        # return render_template('test_template.html', files_content=uploaded_files_content)
    # upload.html
    return render_template('test_template.html')

# def home() : 
    # return "test home page"
    # return render_template('home.html')
    # return render_template('test_template.html')

@app.route('/list_files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('list_files.html', files=files)

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
    # app.run(debug=True)
    # app.run(host="127.0.0.1", port=8080, debug=True)