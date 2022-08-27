from boggle import Boggle
from flask import Flask, request, render_template, flash, session, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Renders the homepage which contains the start button"""
    return render_template('home.html')

@app.route('/start')
def start_game():
    """Makes a new board and redirects user to game"""
    theBoard = boggle_game.make_board()
    session["board"] = theBoard
    return redirect('/game')

@app.route('/game')
def main_game():
    """Show the user the board"""
    board = session["board"]
    return render_template('board.html', board=board)

@app.route('/response')
def get_response():
    """Checks the guessed word and returns a result json"""
    board = session["board"]
    guessed = request.args.get('word')
    if guessed in boggle_game.words:
        result = boggle_game.check_valid_word(board, guessed)
        return jsonify({"result": result})
    return jsonify(result="not-a-word")

@app.route('/finish', methods=['POST'])
def finish_game():
    """Initialize cookie/change cookie based on game result or first time playing"""
    content = request.json
    if "played" in session:
        session["played"] += 1
    else:
        session["played"] = 1
    
    if "highestscore" in session:
        if content["score"] > session["highestscore"]:
            session["highestscore"] = content["score"]
    else:
        session["highestscore"] = content["score"]
    return jsonify({"result": "test"})