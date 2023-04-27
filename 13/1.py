# /?name={% for i in range(19) %}{{ i }}{% endfor %}


from flask import Flask, request
from jinja2 import Template

app = Flask(__name__)


@app.route("/")
def index():
    name = request.args.get('name', 'guest')
    t = Template("Hello " + name)
    return t.render()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
