from flask import Flask
from flask import template_rendered


app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!!</h1>'


@app.route('/user/<name>')
def user(name):
    # return '<h1> Hello {name}</h1>'.format(name=name)
    return '<h1> Hello {name}</h1>'.format(**{'name': name})


if __name__ == '__main__':
    app.run(debug=True)
