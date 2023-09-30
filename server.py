import flask
from flask import Flask, render_template, request
import random
import wizards

app = Flask(__name__)

@app.route('/static/<path:path>')
def serve_file(path):
    # Serve static files from the 'static/' directory
    return send_from_directory('static', path)

@app.route("/")
def home():
    name1 = wizards.get_random_wizard()
    name2 = wizards.get_random_wizard()
    name3 = wizards.get_random_wizard()
    return render_template('choose.html', name1=name1, name2=name2, name3=name3)

@app.route("/battlebegin")
def begin_battle():
    name = flask.request.args.get('wizard') or wizards.get_random_wizard()
    return render_template('battlebegin.html', name=name)

@app.route("/start", methods=['POST'])
def start_wizard_battle():
    spell1 = request.form['text']
    name1 = request.form['name']

    name2 = "Ignatius the Red"
    spell2 = "a destructive fireball of pure energy"

    if random.choice(range(20)) + 1 > 10:
        name1, spell1, name2, spell2 = name2, spell2, name1, spell1

    print("Starting battle between {} and {}".format(name1, name2))
    winner = wizards.decide_winner(name1, name2, spell1, spell2)
    print("the winner is {}".format(winner))
    description = wizards.describe_battle(name1, name2, spell1, spell2, winner)
    print("description: {}".format(description))

    return render_template('battle.html', description=description, winner=winner, name1=name1, name2=name2, spell1=spell1, spell2=spell2)

if __name__ == "__main__":
    app.run(debug=False)
