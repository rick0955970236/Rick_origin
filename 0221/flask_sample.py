from flask import Flask

app = Flask(__name__)



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/home")
def hello_home():
    return "<p>Hello, home!</p>"



# 如果要使用使用 python xxx.py 執行
if __name__ == '__main__':
    app.run(debug=True)
