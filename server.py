from flask import Flask, render_template, request, Response
import time
import sys

# Create flask app
app = Flask(__name__)

state = ["down", "down"]
health = [400, 400]
last_acc = [{"left": [-9, 0, 0], "right": [-9, 0, 0]},
            {"left": [-9, 0, 0], "right": [-9, 0, 0]}]

@app.route("/")
def root():
    """ Landing page
    A page where we select what kind of device we are serving """
    return render_template("main.html")


@app.route("/game")
def game():
    """ Page where the main screen is located
    Players health is reset on every reload """
    global health, state
    health = [400, 400]
    state = ["down", "down"]
    return render_template("game.html")


@app.route("/input")
def input():
    """ Website that reads and sends accelerometer data back to the server """
    return render_template("input.html")


@app.route("/api", methods=['POST'])
def api():
    """ Backend point to which all accelerometer data is send to """
    global state, last_acc, last_led

    # Get POST request data
    acc = request.form.get("data").split()
    player = int(request.form.get("player"))-1
    hand = request.form.get("hand")

    # Disable dead players from doing anything
    if health[player] <= 0:
        return ""

    # Save new accelerometer data
    last_acc[player][hand] = list(map(float, acc))

    for direction in ["left", "right"]:
        # Check player hit left or right punches
        if last_acc[player][direction][2] < -8:
            if state[player] != direction:
                if state[not player] == "up":
                    health[not player] -= 2;
                else:
                    health[not player] -= 20
                if health[not player] <= 0:
                    state[not player] = "dead"
            state[player] = direction
            break

    else:
        if abs(last_acc[player]["left"][0]) > 8 and abs(last_acc[player]["right"][0]) > 8:
            # Check if the player put up a block
            state[player] = "up"
        elif health[not player] <= 0:
            # If nothing is up but the player won
            state[player] = "win"
        else:
            # The basic pose
            state[player] = "down"

    return ""


@app.route('/status')
def status():
    """ Return a space seperated string of important data """
    return " ".join(state) + " " + " ".join(map(str, health))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
