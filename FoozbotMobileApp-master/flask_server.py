from flask import Flask, request, jsonify
import json
import random
import time
import os

app = Flask(__name__)

gameInProgress = False
sessionID = random.randint(100, 10000)
connectingUser = False
startConnectionSession = time.time()


def fileHandler(mode, data=None):
    if mode == "write":
        with open("score.json", 'w') as file:
            json.dump(data, file)
    elif mode == "read":
        with open("score.json", 'r') as file:
            jsonData = json.load(file)
        return jsonData
    elif mode == "check":
        try:
            if os.path.isfile("score.json"):
                with open("score.json", 'r') as file:
                    jsonData = json.load(file)
                if jsonData["ack"]:
                    os.remove("score.json")
                    print("removed")
                    return True
                return False
            else:
                print("File does not exist")
                return True
        except Exception as e:
            print("Error:", e)
            return False
    else:
        print("Mode not defined")


@app.route('/', methods=['GET', 'POST'])
def handle_request():
    global gameInProgress, sessionID, connectingUser, startConnectionSession

    if request.method == 'GET':
        if gameInProgress:
            print("\nsending score\n")
            jsonData = fileHandler("read")

            message = {
                "ongoing": True,
                "otherUserConnecting": False,
                "gameEnded": jsonData["ongoing"],
                "p1Score": jsonData["player_1_score"],
                "p2Score": jsonData["player_2_score"],
                "arcScore": ((jsonData["player_1_score"] * 100) + (jsonData["player_2_score"] * -25) + (
                        (jsonData["player_1_score"] - jsonData["player_2_score"]) * 10)),
            }
        elif fileHandler("check") and (not connectingUser or ((time.time() - startConnectionSession) > 10)):
            print("no users Playing. Reserving game for a 10 seconds (indev), then a new user can connect")
            connectingUser = True
            startConnectionSession = time.time()
            sessionID = random.randint(100, 10000)

            message = {
                "ongoing": False,
                "otherUserConnecting": False,
                "sessionID": sessionID
            }
        else:
            message = {
                "ongoing": False,
                "otherUserConnecting": True
            }

        return jsonify(message)

    elif request.method == 'POST':
        print("a")
        data = request.json
        print(data)

        if gameInProgress and sessionID == data["sessionID"] and data.get("stop"):
            message = {"start": False}
            gameInProgress = False

            saveData = {
                "player_1_score": -1,
                "player_2_score": -1,
                "game_mode": "Dont Care",
                "difficulty": "Didn't Ask",
                "ongoing": False,
                "ack": False,
            }
            fileHandler("write", saveData)

            print("stopping")
        elif sessionID == data["sessionID"] and (not gameInProgress):
            message = {"start": True}
            saveData = {
                "player_1_score": 0,
                "player_2_score": 0,
                "game_mode": data["gamemode"],
                "difficulty": data["difficulty"],
                "ongoing": True,
                "ack": False,
            }
            fileHandler("write", saveData)
            gameInProgress = True
            connectingUser = False
            message = {"start": True}
            print("\nstarting game\n")
        else:
            print("another user posting" + str(data.get("stop")))
            message = {"start": False}

        return jsonify(message)


if os.path.isfile("score.json"):
    os.remove("score.json")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)