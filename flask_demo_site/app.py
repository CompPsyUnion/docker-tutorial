from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello, Docker!"


if __name__ == '__main__':
    with open("output.txt", "w", encoding="utf-8") as f:
        # 写入字符串内容
        f.write("Hello, 这是 Python 输出的文件内容！\n")
    app.run(host='0.0.0.0', port=5000)
