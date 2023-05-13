from flask import Flask, render_template, request

app = Flask(__name__)
dataset=["ABC","DEF","HIJ"]  # 模拟数据库


@app.route("/", methods=["GET", "POST"])

def index():
    query = ""
    # 提交
    if request.method == "POST":
        if request.form.get("submit") == "提交":
            comment = request.form.get("input").strip()
            if comment:
                dataset.append(comment)  # 模拟将提交写入数据库
    # 查询
    elif request.method == "GET":
        if request.args.get("submit") == "查询":
            query = request.args.get("content").strip()
            if query:
                sub_dataset = [x for x in dataset if query in x]
                return render_template("index.html", query=query, comments=sub_dataset)
    
    return render_template("index.html", query=query, comments=dataset)


if __name__ == "__main__":
    app.run()