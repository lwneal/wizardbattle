from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/<path:path>')
def serve_file(path):
    return app.send_static_file(path)

@app.route("/start", methods=['POST'])
def start_wizard_battle():
    user_spell = request.form['text']

    name1 = "Ignatius the Red"
    spell1 = "a destructive fireball of pure energy"
    name2 = "Bartholomew the Blue"
    spell2 = user_spell
    print("Starting battle between {} and {}".format(name1, name2))
    winner = decide_winner(name1, name2, spell1, spell2)
    print("the winner is {}".format(winner))
    description = describe_battle(name1, name2, spell1, spell2, winner)
    print("description: {}".format(description))

    return description

if __name__ == "__main__":
    app.run(debug=False)
