import os
import time
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from wtforms import FileField, SelectField, SubmitField
import pandas as pd
from PIL import Image
import numpy as np
from scipy.spatial import KDTree


# Configuration Class
class Config:
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB limit
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    ALLOWED_GRID_WIDTHS = {10, 24, 32, 40, 64, 80, 100, 120}
    SECRET_KEY = 'your_secret_key'  # Replace with your actual secret key


app = Flask(__name__)
app.config.from_object(Config)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Flask-Limiter without explicitly passing key_func here
limiter = Limiter(
    app,
    default_limits=["100 per day", "100 per hour"]
)

# Set key_func after Limiter initialization
limiter.key_func = get_remote_address


@app.errorhandler(429)
def ratelimit_handler(e):
    return "Rate limit exceeded. Please try again later.", 429

# Function to convert hex to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


# Load emoji color data and create k-d tree
emoji_data = pd.read_csv('data/emojiColor.csv')
emoji_data['RGB'] = emoji_data['Hex Color'].apply(hex_to_rgb)
color_tuples = list(emoji_data['RGB'])
color_tree = KDTree(color_tuples)


def find_closest_emoji(rgb_pixel):
    distance, index = color_tree.query(rgb_pixel)
    return emoji_data.iloc[index]['Emoji']


def create_emoji_image(filepath, grid_width=32):
    start_time = time.time()

    with Image.open(filepath) as img:
        img = img.resize((grid_width, int(grid_width * img.size[1] / img.size[0])), Image.Resampling.NEAREST)
        img = img.convert("RGB")  # Convert to RGB format if not already
        emoji_html = "<div class='emoji-grid'>"
        for y in range(img.size[1]):
            emoji_html += "<div class='emoji-row'>"
            for x in range(img.size[0]):
                rgb = img.getpixel((x, y))  # This will now be a tuple of length 3
                emoji = find_closest_emoji(rgb)
                emoji_html += f"<span>{emoji}</span>"
            emoji_html += "</div>"
        emoji_html += '</div>'

    end_time = time.time()
    processing_time = round(end_time - start_time, 2)

    return emoji_html, processing_time


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


class UploadForm(FlaskForm):
    file = FileField('Image File', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    grid_width = SelectField('Grid Width',
                             choices=[(str(width), str(width)) for width in sorted(Config.ALLOWED_GRID_WIDTHS)])
    submit = SubmitField('Upload')


@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def upload_file():
    form = UploadForm()
    emoji_html = None
    processing_time = None
    error_message = None
    if request.method == 'POST' and form.validate_on_submit():
        file = form.file.data
        grid_width = int(form.grid_width.data)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            emoji_html, processing_time = create_emoji_image(filepath, grid_width)
        else:
            error_message = 'Please upload a file.'
    return render_template('emojiArt.html', form=form, emoji_html=emoji_html, processing_time=processing_time,
                           error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
