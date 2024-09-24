from flask import Flask, request, abort, g, render_template

import requests

app = Flask(__name__)

history_list = []
current_result = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global history_list, current_result
    if request.method == 'POST':
        if request.form.get('action') == 'history':
            result = requests.get("http://127.0.0.1:3001/history").content.decode('ascii')
            values = [x[1:-1] for x in result[1:-2].split(',')]
            history_list = values
        else:
            expr = request.form.get('expression')
            result = requests.post("http://127.0.0.1:3001/submit", json={'exp': expr}).content.decode('ascii')
            current_result = result
            history_list.insert(0, f'{expr} = {result}')
    return render_template('index.html', title='Home', history=history_list, result=current_result)


if __name__ == '__main__':
    app.run(port=4000)
