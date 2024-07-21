from flask import Flask, render_template, request, redirect, url_for 
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

# def read_file_content(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return f.read()
#     except UnicodeDecodeError:
#         try:
#             with open(file_path, 'r', encoding='latin1') as f:
#                 return f.read()
#         except UnicodeDecodeError:
#             return "Could not decode file content"

@app.route("/", methods=['GET', 'POST'])
def upload_files():
    if request.method =='POST':
        files = request.files.getlist('files')
        uploaded_files_content = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)

                uploaded_files_content.append(filename)

                # content = read_file_content(file_path)
                # uploaded_files_content.append((file.filename, content))

                # with open(file_path, 'r') as f:
                #     content = f.read()
                #     uploaded_files_content.append((file.filename, content))
        
        return render_template('test_template.html', files_content=uploaded_files_content)
    # upload.html
    return render_template('test_template.html')

# def home() : 
    # return "test home page"
    # return render_template('home.html')
    # return render_template('test_template.html')

# test for display content using pandas
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     # Read the Excel file using pandas
#     df = pd.read_excel(filepath)
#     # Display the content of the Excel file (for demonstration)
#     return df.to_html()

@app.route('/list_files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('list_files.html', files=files)

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
    # app.run(debug=True)
    # app.run(host="127.0.0.1", port=8080, debug=True)