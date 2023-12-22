# Emoji Art

## Overview

Emoji Art is a Flask web application that allows users to upload images and convert them into pixelated art made entirely of emojis. The application down-scales the uploaded image, pixelates it, and then maps each pixel to the closest matching emoji based on color.

## Features

- Image Upload: Users can upload image files in common formats (JPG, PNG, etc.).
- Emoji Grid Generation: The application generates a grid of emojis that visually represent the uploaded image.
- Customizable Grid Size: Users can select different resolutions for the emoji grid.

## Installation and Setup

To run Emoji Art on your local machine, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/shaik/emojiArt.git
   cd emojiArt

2. **Set Up a Virtual Environment (Optional but Recommended):**
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   python emojiArtKD.py

## Usage

- Navigate to `http://localhost:5000`.
- Upload an image using the provided form.
- Choose a grid resolution.
- Submit the form to see the emoji representation of your image.

## Contributing

Contributions to Emoji Art are welcome! Please feel free to submit pull requests, report bugs, and suggest features.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Emoji data provided by [EmojiSource](link-to-emoji-source).
- Flask framework for simplifying web application development.

## Contact

For any queries, you can reach out to [YourName](your-email@example.com).
