from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import pandas as pd
from process_data import process_selected_items

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

selected_items = []
imagePath = ""


def ensure_upload_folder_exists():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_index()


@app.route('/upload', methods=['POST'])
def upload_file():
    return handle_file_upload()


@app.route('/upload_image', methods=['POST'])
def upload_image():
    return handle_image_upload()


@app.route('/select', methods=['POST'])
def select_items():
    return handle_item_selection()


@app.route('/process', methods=['POST'])
def process_items():
    return handle_item_processing()


def render_index(data=None, column_values=None, selected_items=None):
    return render_template('index.html', data=data, column_values=column_values, selected_items=selected_items)


def handle_file_upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        if file.filename.endswith(".xlsx"):
            df = pd.read_excel(filepath)
        elif file.filename.endswith(".csv"):
            df = pd.read_csv(filepath)
        column_values = df[
            ['Name', 'Phone 1 - Value']].dropna().values.tolist()  # Extract rows with 'Name' and 'Phone 1 - Value'
        return render_index(column_values=column_values)


def handle_image_upload():
    global imagePath
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image file provided"}), 400
    image = request.files['image']
    if image.filename == '':
        return jsonify({"status": "error", "message": "No file selected"}), 400
    if image:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(filepath)
        imagePath = filepath
        return jsonify({"status": "success", "filepath": filepath})


def handle_item_selection():
    global selected_items
    selected_items = request.form.getlist('selected_items')
    selected_items = [eval(item) for item in selected_items]
    return render_index(selected_items=selected_items)


def handle_item_processing():
    process_selected_items(selected_items, imagePath)
    return jsonify({"status": "success"})


if __name__ == '__main__':
    ensure_upload_folder_exists()
    app.run(debug=True)
