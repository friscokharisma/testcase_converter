from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir_structure = {}
    for dirpath, dirnames, filenames in os.walk(rootdir):
        folder = dir_structure
        rel_path = os.path.relpath(dirpath, rootdir)
        if rel_path != '.':
            for part in rel_path.split(os.sep):
                folder = folder.setdefault(part, {})
        folder.update({f: None for f in filenames})
    return dir_structure

@app.route('/list_files')
def index():
    directory_structure = get_directory_structure(UPLOAD_FOLDER)
    return render_template('sample/x_index.html', structure=directory_structure)

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
