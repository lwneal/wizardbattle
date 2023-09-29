from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/<path:path>')
def serve_file(path):
    return app.send_static_file(path)

@app.route("/start", methods=['POST'])
def start():
    text_value = request.form['text']
    # You may work with the 'text_value' here
    return "Received the text: " + text_value

if __name__ == "__main__":
    app.run(debug=False)
