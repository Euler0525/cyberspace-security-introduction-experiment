# 反射型攻击

from flask import Flask, request
from jinja2 import Template

app = Flask(__name__)


@app.route("/")
def index():
    name = request.args.get('name', 'World!')
    t = Template("Hello " + name)
    return t.render()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
    app.config["DEBUG"] = True
