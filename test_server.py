from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Comprobando que funciona el deploy"

if __name__ == "__main__":
    app.run()
