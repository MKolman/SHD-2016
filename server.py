from flask import Flask, render_template, request

# Create flask app
app = Flask(__name__)

state = ["down", "down"]
health = [400, 400]
last_acc = [{"left": [-9, 0, 0], "right": [-9, 0, 0]},
            {"left": [-9, 0, 0], "right": [-9, 0, 0]}]


def get_counter():
    num = 0
    with open("game_counter.txt", "r") as counter:
        num = int(counter.read())
    return num


def increase_counter():
    num = get_counter()
    with open("game_counter.txt", "w") as counter:
        counter.write("{}\n".format(num + 1))


@app.route("/")
def root():
    """ Landing page
    A page where we select what kind of device we are serving """
    return render_template("main.html", counter=get_counter())


@app.route("/game")
def game():
    """ Page where the main screen is located
    Players health is reset on every reload """
    return render_template("game.html")


@app.route("/reset")
def reset():
    """ Reset the game """
    global health, state, last_acc
    health = [400, 400]
    state = ["down", "down"]
    last_acc = [{"left": [-9, 0, 0], "right": [-9, 0, 0]},
                {"left": [-9, 0, 0], "right": [-9, 0, 0]}]
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
    player = int(request.form.get("player")) - 1
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
                    health[not player] -= 5
                else:
                    health[not player] -= 20
                if health[not player] <= 0:
                    if state[not player] != "dead":
                        increase_counter()
                    state[not player] = "dead"
            state[player] = direction
            break

    else:
        if abs(last_acc[player]["left"][0]) > 8 and \
                abs(last_acc[player]["right"][0]) > 8:
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


@app.route('/help')
def help():
    return render_template("help.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
