from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("upload.html")

# POST → upload image
@app.route("/upload", methods=["POST"])
def upload():
    image = request.files["image"]
    image.save("static/uploads/photo.jpg")
    return render_template("display.html", img="photo.jpg")

# PUT logic → update image
@app.route("/update", methods=["POST"])
def update():
    image = request.files["image"]
    image.save("static/uploads/photo.jpg")
    return render_template("display.html", img="photo.jpg")

if __name__ == "__main__":
    app.run(debug=True)