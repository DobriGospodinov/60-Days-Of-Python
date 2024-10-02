from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/v1/<word>")
def description(word):
    cap_word = word.upper()
    return {"word": word,
            "description": cap_word}

if __name__ == "__main__":
    app.run(debug=True)