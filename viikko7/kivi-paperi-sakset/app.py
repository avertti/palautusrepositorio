from flask import Flask, render_template, request, session, redirect, url_for
from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu

app = Flask(__name__)
app.secret_key = "your-secret-key-change-in-production"

WINNING_SCORE = 3


def get_tuomari():
    if "tuomari" not in session:
        session["tuomari"] = {"ekan_pisteet": 0, "tokan_pisteet": 0, "tasapelit": 0}
    return session["tuomari"]


def update_tuomari(tuomari_dict):
    session["tuomari"] = tuomari_dict
    session.modified = True


def get_game_mode():
    return session.get("game_mode", None)


def set_game_mode(mode):
    session["game_mode"] = mode


def get_ai():
    if "ai_memory" not in session:
        session["ai_memory"] = []
    return session["ai_memory"]


def update_ai(memory):
    session["ai_memory"] = memory
    session.modified = True


def check_winner(tuomari_dict):
    if tuomari_dict["ekan_pisteet"] >= WINNING_SCORE:
        return "player1"
    elif tuomari_dict["tokan_pisteet"] >= WINNING_SCORE:
        return "player2"
    return None


@app.route("/")
def index():
    session.clear()
    return render_template("index.html", winning_score=WINNING_SCORE)


@app.route("/select_mode", methods=["POST"])
def select_mode():
    mode = request.form.get("mode")
    set_game_mode(mode)
    return redirect(url_for("play"))


@app.route("/play")
def play():
    mode = get_game_mode()
    if not mode:
        return redirect(url_for("index"))

    tuomari = get_tuomari()
    winner = check_winner(tuomari)

    if winner:
        return redirect(url_for("game_over"))

    return render_template(
        "play.html", mode=mode, tuomari=tuomari, winning_score=WINNING_SCORE
    )


@app.route("/make_move", methods=["POST"])
def make_move():
    player_move = request.form.get("move")
    mode = get_game_mode()

    if not player_move or player_move not in ["k", "p", "s"]:
        return redirect(url_for("play"))

    # Get computer move based on mode
    if mode == "pvp":
        computer_move = request.form.get("move2")
        if not computer_move or computer_move not in ["k", "p", "s"]:
            return redirect(url_for("play"))
    elif mode == "easy":
        ai = Tekoaly()
        computer_move = ai.anna_siirto()
    elif mode == "hard":
        memory = get_ai()
        ai = TekoalyParannettu(10)
        # Rebuild AI memory
        for m in memory:
            ai.aseta_siirto(m)
        computer_move = ai.anna_siirto()
        ai.aseta_siirto(player_move)
        # Save memory
        memory.append(player_move)
        update_ai(memory)
    else:
        return redirect(url_for("index"))

    # Update score
    tuomari_dict = get_tuomari()
    tuomari = Tuomari()
    tuomari.ekan_pisteet = tuomari_dict["ekan_pisteet"]
    tuomari.tokan_pisteet = tuomari_dict["tokan_pisteet"]
    tuomari.tasapelit = tuomari_dict["tasapelit"]

    tuomari.kirjaa_siirto(player_move, computer_move)

    tuomari_dict["ekan_pisteet"] = tuomari.ekan_pisteet
    tuomari_dict["tokan_pisteet"] = tuomari.tokan_pisteet
    tuomari_dict["tasapelit"] = tuomari.tasapelit
    update_tuomari(tuomari_dict)

    # Determine result
    if player_move == computer_move:
        result = "Tasapeli!"
    elif tuomari._eka_voittaa(player_move, computer_move):
        result = "Voitit!"
    else:
        result = "Hävisit!"

    move_names = {"k": "Kivi", "p": "Paperi", "s": "Sakset"}

    # Check if game is over
    winner = check_winner(tuomari_dict)

    return render_template(
        "result.html",
        mode=mode,
        player_move=move_names[player_move],
        computer_move=move_names[computer_move],
        result=result,
        tuomari=tuomari_dict,
        winning_score=WINNING_SCORE,
        winner=winner,
    )


@app.route("/game_over")
def game_over():
    mode = get_game_mode()
    tuomari = get_tuomari()
    winner = check_winner(tuomari)

    if not winner:
        return redirect(url_for("play"))

    return render_template("game_over.html", mode=mode, tuomari=tuomari, winner=winner)


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
