from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file, jsonify, abort
import os
import pandas as pd

import zipfile
import datetime
from io import BytesIO

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'processed/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
ALLOWED_EXTENSIONS = {'xlsx'}

timestamp_name =  datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
FOLDER_NAME = 'uploads/' + str(timestamp_name)
app.config['FOLDER NAME'] = FOLDER_NAME

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
                os.makedirs(FOLDER_NAME) #create folder using timestamp name
                filename = file.filename
                file.save(os.path.join(app.config['FOLDER NAME'], filename)) #create folder using timestamp name
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('upload_files'))
        # return render_template('test_template.html', files_content=uploaded_files_content)
    # upload.html
    return render_template('test_template.html')

# def home() : 
    # return "test home page"
    # return render_template('home.html')
    # return render_template('test_template.html')

# need to add button in fe for download all, show after file uploaded 
@app.route('/download_all')
def download_all():
    # Create a BytesIO object to hold the zip file in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            zip_file.write(file_path, os.path.basename(file_path))
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='all_files.zip')

@app.route('/list_files', defaults={'subfolder': ''})
@app.route('/list_files/<path:subfolder>')
def list_files(subfolder):
    folder = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
    if not os.path.exists(folder):
        abort(404)
    
    files = os.listdir(folder)
    return render_template('list_files.html', files=files, subfolder=subfolder)

# testing download
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/view_file/<path:filename>')
def view_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
    # app.run(debug=True)
    # app.run(host="127.0.0.1", port=8080, debug=True)