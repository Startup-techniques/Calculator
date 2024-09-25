from flask import Flask, request, abort, g, render_template

import requests

app = Flask(__name__)

ELEMENTS = {
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    'plus': '+',
    'minus': '-',
    'mul': '*',
    'div': '/',
    'mod': '%',
    'sqrt': 'sqrt',
    'pi': 'pi',
    'e': 'e',
    'sin': 'sin(',
    'cos': 'cos(',
    'tan': 'tan(',
    'sinh': 'sinh(',
    'cosh': 'cosh(',
    'tanh': 'tanh(',
    'asin': 'asin(',
    'acos': 'acos(',
    'atan': 'atan(',
    'asinh': 'asinh(',
    'acosh': 'acosh(',
    'atanh': 'atanh(',
    'left-bracket': '(',
    'right-bracket': ')',
    'dot': '.'
}

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
            response = requests.post("http://127.0.0.1:3001/submit", json={'exp': expr})
            result = response.content.decode('ascii')
            current_result = result
            history_list.insert(0, (expr, result, response.status_code == 200))
    return render_template('index.html', title='Home', history=history_list, result=current_result, elements=ELEMENTS)


if __name__ == '__main__':
    app.run(port=4000)
