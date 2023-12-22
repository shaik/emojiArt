from flask import Flask, render_template
import csv

app = Flask(__name__)

def read_emojis_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        emojis = [row[0] for row in reader]
    return ''.join(emojis)

@app.route('/')
def index():
    emojis = read_emojis_from_csv('../data/emojis.csv')
    return render_template('index.html', emojis=emojis)

if __name__ == '__main__':
    app.run(debug=True)
