import json
import os
import time
from pathlib import Path


class AppInterface():
    def __init__(self, file_path):
        self.file_path = Path(file_path)


        self.time_since_last_update = time.time()
        self.UPDATE_FREQUENCY = 5

        self.info = {
            "player_1_score": 0,
            "player_2_score": 0,
            "game_mode": "Highest Score",
            "difficulty": "Medium",
            "ongoing": False,
            "ack": False
        }

    def game_ongoing(self) -> bool:
        #print(self.info)
        if time.time() - self.time_since_last_update > self.UPDATE_FREQUENCY:
            try:
                new_info = self.read_json()
                if new_info:
                    self.info = new_info
                    
                    self.info["ongoing"] = new_info["ongoing"]
            except:
                print("failed read")
        #print(self.info["ongoing"])
        return self.info["ongoing"]

    def update_score(self, score: tuple):
        print("updating score: " + str(score))
        self.info["player_1_score"] = score[0]
        self.info["player_2_score"] = score[1]
        self.info["ongoing"] = True
        try:
            self.write_json()
        except:
            print("line 47 failed write")

    def read_json(self):
        if self.file_path.exists():
            with open(self.file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)
                    
                except:
                    print("Read json parse failed")
                    return None
                #print(data)
                return data
        else:
            return None

    def get_difficulty(self):
        difficulty = self.info["difficulty"]
        return difficulty

    def get_game_mode(self):
        game_mode = self.info["game_mode"]
        return game_mode

    def write_json(self):
        with open(self.file_path, 'w') as json_file:
            print("Opens file")
        
            print(self.info)
            json.dump(self.info, json_file)
            print("Gets here")

    def wait_for_game_start(self):
        while True:
            file_data = self.read_json()
            print(file_data)
            if file_data:
                self.info = file_data
                if file_data["ongoing"]:
                    return
                else:
                    print("File exists, but game isn't ongoing")
            else:
                pass

    def end_game(self):
        self.ack = True
        self.info["ack"] = True

        try:
            self.write_json()
        except Exception as e:
            print(e)
        os.remove(self.file_path)
