from flask import Flask, render_template, request, jsonify
from services.text_analyzer import analyze_text

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze-text", methods=["POST"])
def api_analyze_text():

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({
            "error": "No text provided."
        }), 400

    result = analyze_text(data["text"])

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)