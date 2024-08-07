from flask import Flask, render_template, request, send_from_directory, jsonify, abort
import os
import zipfile
from datetime import datetime
from convert import convert_file
import logging
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('main_index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part'})
    files = request.files.getlist('files[]')
    
    # Create a new folder with the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], timestamp)
    os.makedirs(folder_path)

    # process_folder_path = os.path.join(app.config['PROCESSED_FOLDER'], timestamp)
    # os.makedirs(process_folder_path)

    for file in files:
        filename = file.filename
        filelocation = os.path.join(folder_path, filename)
        
        # filename_test = f'testing_{filename}'
        # filelocation_test = os.path.join(folder_path, filename_test)
        file.save(filelocation)

        try:
            convert_file(filename, filelocation)
        except ValueError as e:
            return jsonify({'error': str(e)}), 422

        # file.save(os.path.join(folder_path, filename))
        

        # <----- processing file stage is here ----->
        # wb = openpyxl.load_workbook(folder_path + "/" + filename)
        # new_sheet_name = 'Testing'
        # if new_sheet_name not in wb.sheetnames:
        #     wb.create_sheet(title=new_sheet_name)
        #     print('created test')
        # wb.save(os.path.join(folder_path, filename))

        # new_filename = f"testing_{filename}" #process file is here <-----
        # file.save(os.path.join(folder_path, new_filename))

    return jsonify({'message': 'Files successfully uploaded', 'folder': timestamp})

@app.route('/download/<folder_name>')
def download_folder(folder_name):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
    
    if not os.path.exists(folder_path):
        return jsonify({'error': 'Folder not found'})

    zip_filename = f"{folder_name}.zip"
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], zip_filename, as_attachment=True)

@app.route('/list_folder', defaults={'req_path': ''})
@app.route('/list_folder/<path:req_path>')
def list_folder(req_path):
    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], req_path)

    if not os.path.exists(abs_path):
        return jsonify({'error': 'Path not found'})

    if os.path.isfile(abs_path):
        return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path))

    files = os.listdir(abs_path)
    file_list = []
    for file in files:
        path = os.path.join(req_path, file)
        if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], path)):
            file_list.append({'name': file, 'type': 'folder', 'path': path})
        else:
            file_list.append({'name': file, 'type': 'file', 'path': path})
    
    return jsonify({'files': file_list})

# @app.route('/view_folder/<path:folder_path>')
# def view_folder(folder_path):
#     abs_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_path)

#     if not os.path.exists(abs_path):
#         return render_template('error.html', message='Folder not found')

#     if os.path.isfile(abs_path):
#         return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path))

#     files = os.listdir(abs_path)
#     file_list = []
#     for file in files:
#         path = os.path.join(folder_path, file)
#         if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], path)):
#             file_list.append({'name': file, 'type': 'folder', 'path': path})
#         else:
#             file_list.append({'name': file, 'type': 'file', 'path': path})

#     return render_template('sample/gpt_folder_view.html', files=file_list, folder_path=folder_path)

# testing

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/debug')
def debug():
    # Get the current working directory
    cwd = os.getcwd()
    logging.debug(f'Current working directory: {cwd}')

    # List files in the current working directory
    files_in_cwd = os.listdir(cwd)
    logging.debug(f'Files in current working directory: {files_in_cwd}')

    # List files in the upload folder
    upload_files = os.listdir(app.config['UPLOAD_FOLDER'])
    logging.debug(f'Files in upload folder: {upload_files}')

    # List files in the template folder
    template_files = os.listdir(app.config['TEMPLATE_FOLDER'])
    logging.debug(f'Files in template folder: {template_files}')

    return jsonify({
        'current_working_directory': cwd,
        'files_in_cwd': files_in_cwd,
        'upload_files': upload_files,
        'template_files': template_files,
    })


# ------

app.config['TEMPLATE_FOLDER'] = os.path.join(os.getcwd(), 'testcase_template') 

# for see list of files in uploads
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
def list_files():
    directory_structure = get_directory_structure(UPLOAD_FOLDER)
    return render_template('main_list_files.html', structure=directory_structure)

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/delete_all_files', methods=['DELETE'])
def delete_all_files():
    folder_path = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'All files deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
