import requests
from flask import Flask, render_template, send_from_directory, request
import os

app = Flask(__name__)
message = ""
BASE_URL = 'https://api.voicerss.org/'
API_KEY = os.environ.get('api_key')
LANG = "en-us"


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        global message
        message = request.form.get('user_msg')

        api_call(message)

    return render_template("index.html")


def api_call(msg):
    params = {
        'key': API_KEY,
        'src': msg,
        'h1': LANG,
        'v': 'Eka',
        "c": "mp3",
        'f':'8khz_8bit_mono'
    }
    response = requests.get(url=BASE_URL, params=params)
    if response.status_code == 200:
        audio_data = response.content
        audio_filename = 'audio_output.mp3'
        audio_path = os.path.join(app.static_folder, audio_filename)
        with open(audio_path, 'wb') as audio_file:
            audio_file.write(audio_data)
        print(f'Audio saved as {audio_filename}')

    else:
        print('Failed to fetch audio from API', 500)


# @app.route('/static/<filename>')
# def audio(filename):
#     return send_from_directory('static', filename)


if __name__ == "__main__":
    app.run(debug=True)