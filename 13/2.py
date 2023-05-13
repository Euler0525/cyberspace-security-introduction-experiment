from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/name/<name>')
def get_name(name):
    return render_template('name.html', name=name)

if __name__ == '__main__':
    app.run()