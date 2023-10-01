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
    wizard_names = wizards.get_random_wizards(3)
    return render_template('choose.html', wizards=wizard_names)

@app.route("/battlebegin")
def begin_battle():
    name = flask.request.args.get('wizard') or wizards.get_random_wizard()
    placeholderspell = wizards.get_random_magic_spell()
    return render_template('battlebegin.html', name=name, placeholderspell=placeholderspell)

@app.route("/round1", methods=['GET', 'POST'])
def start_wizard_battle():
    if request.method == 'GET':
        return flask.redirect('/')
    spell1 = request.form['text']
    name1 = request.form['name']

    name2 = wizards.get_random_opponent(name1)['name']
    spell2 = wizards.get_random_magic_spell()

    playername, opponentname = name1, name2

    if random.choice(range(20)) + 1 > 10:
        playername, opponentname = name2, name1
        name1, spell1, name2, spell2 = name2, spell2, name1, spell1

    print("Starting battle between {} and {}".format(name1, name2))
    winner = wizards.decide_winner(name1, spell1, name2, spell2)
    print("the winner is {}".format(winner))
    description = wizards.describe_battle(name1, spell1, name2, spell2, winner)
    print("description: {}".format(description))

    narration = description.replace('\n', '. ').split('. ')
    narration = [line + "." if not line.endswith('.') else line for line in narration]

    portrait_filename_1 = wizards.get_portrait_filename(name1)
    portrait_filename_2 = wizards.get_portrait_filename(name2)

    print("Winner: {}".format(winner))
    print("Player name: {}".format(playername))
    player_wins = winner.lower().startswith(playername.lower())
    print("Player wins: {}".format(player_wins))
    winner_name = playername if player_wins else opponentname
    winner_portrait = wizards.get_portrait_filename(winner_name)

    return render_template('round1_results.html', description=description, winner=winner, name1=name1, name2=name2, spell1=spell1, spell2=spell2, narration=narration, portrait_filename_1=portrait_filename_1, portrait_filename_2=portrait_filename_2, playername=playername, winner_portrait=winner_portrait, player_wins=player_wins)


if __name__ == "__main__":
    app.run(debug=False)
