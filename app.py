from flask import Flask

app = Flask(__name__)

#index is the main page
@app.route("/")
def index():
    return "Hello Everyone"

if __name__ in "__main__":
    app.run(debug=True) 