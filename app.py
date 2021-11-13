from flask import Flask

app = Flask(__name__)


@app.route('/<string:name>')
def hello_world(name):
    print("hello world~~", name)
    return 'hello test'


if __name__ == '__main__':
    app.run()