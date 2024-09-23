from flask import Flask, request, abort, g, render_template

import requests

app = Flask(__name__)

history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('action') == 'history':
            result = requests.get("http://127.0.0.1:3001/history").content.decode('ascii')
            # TODO: convert result to list of strings
            # then set glogal variable history with this list
            # this list will be displayed

        else:
            expr = request.form.get('expression')
            result = requests.post("http://127.0.0.1:3001/submit", json={'exp': expr}).content.decode('ascii')
            # TODO: show result some way
    return render_template('index.html', title='Home', history=history)


if __name__ == '__main__':
    app.run(port=4000)
