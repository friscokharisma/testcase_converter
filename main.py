from flask import Flask, render_template, request, redirect, url_for 
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin1') as f:
                return f.read()
        except UnicodeDecodeError:
            return "Could not decode file content"

@app.route("/", methods=['GET', 'POST'])
# def upload_files():
#     if request.method =='POST':
#         files = request.files.getlist('files')
#         uploaded_files_content = []

#         for file in files:
#             if file:
#                 file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#                 file.save(file_path)

#                 content = read_file_content(file_path)
#                 uploaded_files_content.append((file.filename, content))

#                 # with open(file_path, 'r') as f:
#                 #     content = f.read()
#                 #     uploaded_files_content.append((file.filename, content))
        
#         return render_template('upload.html', files_content=uploaded_files_content)
    
#     return render_template('upload.html')

def home() : 
    # return "test home page"
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
    # app.run(debug=True)
    # app.run(host="127.0.0.1", port=8080, debug=True)