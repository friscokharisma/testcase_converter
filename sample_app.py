from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'uploads'
LIST_FOLDER = 'list_dir'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['LIST_FOLDER'] = LIST_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(LIST_FOLDER):
    os.makedirs(LIST_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('sample/index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file[]' not in request.files:
            return redirect(request.url)
        
        files = request.files.getlist('file[]')
        
        for file in files:
            # If the user does not select a file, the browser submits an empty file without a filename
            if file.filename == '':
                continue
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        return redirect(url_for('uploaded_files'))
    return render_template('sample/upload.html')

# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = file.filename
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_files'))
#     return render_template('sample/upload.html')

@app.route('/uploads')
def uploaded_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('sample/uploads.html', files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/list_files')
def list_files():
    files = os.listdir(app.config['LIST_FOLDER'])
    return render_template('sample/list_files.html', files=files)

@app.route('/list_files/<filename>')
def list_file(filename):
    return send_from_directory(app.config['LIST_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
