from flask import Flask, jsonify, render_template
from camera import Camera

app = Flask(__name__)
camera = Camera()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/capture')
def capture():
    if camera.is_awake():
        file_path = camera.trigger_capture()
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)