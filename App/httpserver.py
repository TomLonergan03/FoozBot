from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
import time
import os



gameInProgress = False
sessionID = random.randint(100, 10000)
connectingUser = False
startConnectionSession = time.time()

def fileHandler(mode, data):
     
    if mode == "write":

        print("aa")
        if (os.path.isfile("score.json")):
            os.remove("score.json")
        

        file = open("score.json", 'w')
        json.dump(data, file)
        file.close()

    elif mode == "read":
        
        file = open("score.json", 'r')
        jsonData =(json.load(file))
        file.close()

        return jsonData

    elif mode == "check":

        try:

            if (os.path.isfile("score.json")):
            
                file = open("score.json", 'r')
                jsonData =(json.load(file))
                file.close()

                if jsonData["ack"] == True:
                    os.remove("score.json")
                    print("removed")
                    return True
                
                print("da")
                return False
            
            else:
                print("urgh")
                return True
        
        except:
            print("exx")
            return False
            

    else:
        print("mode not defined")


class handler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')  # Allow GET, POST, OPTIONS requests
        self.send_header('Access-Control-Allow-Headers', 'Content-type')  # Allow Content-type header
        self.end_headers()

    ##Get will get the score and relay it to the app
    def do_GET(self):

        global gameInProgress, sessionID, connectingUser, startConnectionSession, fileHandler
        
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()


        #At any time, if a game is in progress. 
        if (gameInProgress):
            print("\nsending score\n")

            jsonData = fileHandler("read", "")



            #Arcade score:
                # 100 pts for a goal
                # -25 pts for conceding a goal
                # +- 10 points per goal difference
            message = {
                "ongoing": True,
                "otherUserConnecting": False,
                "gameEnded": jsonData["ongoing"],
                "p1Score": jsonData["player_1_score"],
                "p2Score": jsonData["player_2_score"],
                "arcScore": ((jsonData["player_1_score"] * 100) + (jsonData["player_2_score"] * -25) + ((jsonData["player_1_score"] - jsonData["player_2_score"]) * 10)),
                }


        #If there is:
            #No Ongoing Game
            #No connecting user or the user connecting has been idle for >60 seconds
            #The ACK Flag has not yet been set
        elif fileHandler("check", "") and (not connectingUser or ((time.time() - startConnectionSession) > 10) ):

            #Check the ACK Flag (if the file exists)
            
            print("no users Playing. Reserving game for a 10 seconds (indev), then a new user can connect")
            connectingUser = True
            startConnectionSession = time.time()

            sessionID = random.randint(100, 10000)
            
            message = {
                "ongoing": False,
                "otherUserConnecting": False,
                "sessionID": sessionID
                }

        #If a user is currently connecting, or the last game is ongoing
        else:
            message = {
                "ongoing":False,
                "otherUserConnecting":True
                }
            

        print("sending json")
        self._set_headers()
        self.wfile.write(bytes(json.dumps(message), "utf8"))

    ##Post will start the game, with parameters that the user has set.
    ##Can also end the game if the post req contains that flag
    ##Make sure to check the session ID!
    def do_POST(self):
        self._set_headers()
        global gameInProgress, sessionID, connectingUser, fileHandler
            
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)


        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        print(data)


        #If this is the current user session, with a game in progress, and the STOP flag is included, stop the game
        if (gameInProgress and sessionID == data["sessionID"] and data["stop"] == True):
            
            message = {
                "start":False,
                }
            
            gameInProgress = False
            print("stopping")

            
            
                

    

        #If this is the current user session and the game hasnt been started
        elif(sessionID == data["sessionID"] and (not gameInProgress)):
            
            message = {
                "start":True,
                }

            saveData = {
                "player_1_score" : 0,
                "player_2_score" : 0,
                "game_mode" : data["gamemode"],
                "difficulty" : data["difficulty"],
                "ongoing" : True,
                "ack": False,
                }
            
            fileHandler("write", saveData)

            gameInProgress = True
            connectingUser = False
            
            print("\nstarting game\n")
            

        #Otherwise, this user has been idle too long, and someone else has started the game.
        else:
            print("another user posting" + str(data["stop"]))
            message = {
                "start":False,
                }

        self.wfile.write(bytes(json.dumps(message), "utf8"))

if (os.path.isfile("score.json")):
    os.remove("score.json")

with HTTPServer(('0.0.0.0', 8000), handler) as server:
    server.serve_forever()

