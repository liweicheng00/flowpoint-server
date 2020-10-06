from flask import Flask, render_template

app = Flask(__name__, static_url_path='/templates', static_folder='templates', instance_relative_config=True)


@app.route('/')
def hello():

    return render_template("dist/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

