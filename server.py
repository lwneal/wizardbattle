from flask import Flask, render_template, request
import random
import wizards

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

    if random.choice(range(20)) + 1 > 10:
        name1, spell1, name2, spell2 = name2, spell2, name1, spell1

    print("Starting battle between {} and {}".format(name1, name2))
    winner = wizards.decide_winner(name1, name2, spell1, spell2)
    print("the winner is {}".format(winner))
    description = wizards.describe_battle(name1, name2, spell1, spell2, winner)
    print("description: {}".format(description))

    return description

if __name__ == "__main__":
    app.run(debug=False)
