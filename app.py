from flask import Flask, render_template, request
from converter import convert_code

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    converted_code = ""
    source = "Python"
    target = "PHP"
    input_code = ""
    info = ""

    if request.method == "POST":
        source = request.form.get("source", "Python")
        target = request.form.get("target", "PHP")
        input_code = request.form.get("code", "")

        uploaded_file = request.files.get("codefile")

        if uploaded_file and uploaded_file.filename != "":
            input_code = uploaded_file.read().decode("utf-8", errors="ignore")

        if input_code.strip():
            converted_code, info = convert_code(source, target, input_code)

    return render_template(
        "index.html",
        converted_code=converted_code,
        source=source,
        target=target,
        input_code=input_code,
        info=info
    )

if __name__ == "__main__":
    app.run(debug=True)