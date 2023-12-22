from flask import Flask, request, render_template, send_from_directory
import os
from PIL import Image
import pandas as pd
import numpy as np
import time


app = Flask(__name__)

# Function to convert hex to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Load emoji color data
emoji_data = pd.read_csv('../data/emojiColor.csv')
emoji_data['RGB'] = emoji_data['Hex Color'].apply(hex_to_rgb)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to find the closest emoji for a given color
def find_closest_emoji(rgb_pixel):
    distances = emoji_data['RGB'].apply(lambda x: np.linalg.norm(np.array(x) - np.array(rgb_pixel)))
    closest_index = distances.idxmin()
    return emoji_data.iloc[closest_index]['Emoji']

# Function to create an emoji image
def create_emoji_image(filepath, grid_width=32):
    start_time = time.time()  # Start time measurement

    with Image.open(filepath) as img:
        img = img.resize((grid_width, int(grid_width * img.size[1] / img.size[0])), Image.Resampling.NEAREST)
        emoji_html = "<div class='emoji-grid'>"
        for y in range(img.size[1]):
            emoji_html += "<div class='emoji-row'>"
            for x in range(img.size[0]):
                rgb = img.getpixel((x, y))
                emoji = find_closest_emoji(rgb)
                emoji_html += f"<span>{emoji}</span>"
            emoji_html += "</div>"
        emoji_html += '</div>'

    end_time = time.time()  # End time measurement
    processing_time = round(end_time - start_time, 2)  # Calculate and round processing time

    return emoji_html, processing_time


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    emoji_html = None
    processing_time = None
    if request.method == 'POST':
        file = request.files.get('file')
        grid_width = int(request.form.get('grid_width', 32))  # Default to 32 if not specified
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            emoji_html, processing_time = create_emoji_image(filepath, grid_width)
    return render_template('emojiArt.html', emoji_html=emoji_html, processing_time=processing_time)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
