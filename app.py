from flask import Flask, render_template

app = Flask(__name__)

#index is the main page
@app.route("/")
def index():
    return render_template("index.html")

if __name__ in "__main__":
    app.run(debug=True) 