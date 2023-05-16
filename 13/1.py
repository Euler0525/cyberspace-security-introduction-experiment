from flask import Flask, render_template, request

app = Flask(__name__)
dataset=["ABC","DEF","HIJ"]  # 模拟数据库


@app.route("/", methods=["GET", "POST"])

def index():
    query = ""
    # 查询
    if request.method == "GET":
        if request.args.get("submit") == "查询":
            query = request.args.get("content").strip()
            # # 防御反射型攻击
            # query = ''.join(q for q in query if q.isalnum())
            
            if query:
                sub_dataset = [x for x in dataset if query in x]
                return render_template("index.html", query=query, comments=sub_dataset)
    # 提交
    elif request.method == "POST":
        if request.form.get("submit") == "提交":
            comment = request.form.get("input").strip()
            # # 防御持久型攻击
            # comment = ''.join(c for c in comment if c.isalnum())
            if comment:
                dataset.append(comment)  # 模拟将提交写入数据库

    return render_template("index.html", query=query, comments=dataset)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)