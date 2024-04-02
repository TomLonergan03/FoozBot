import json
import time
from pathlib import Path


class AppInterface():
    def __init__(self, file_path):
        self.file_path = Path(file_path)

        self.player_1_score = 0
        self.player_2_score = 0
        self.game_mode = None
        self.difficulty = None
        self.ongoing = False
        self.ack = False

        self.time_since_last_update = time.time()
        self.UPDATE_FREQUENCY = 5

        self.info = {
            "player_1_score": self.player_1_score,
            "player_2_score": self.player_2_score,
            "game_mode": self.game_mode,
            "difficulty": self.difficulty,
            "ongoing": self.ongoing,
            "ack": self.ack
        }

    def game_ongoing(self) -> bool:
        if time.time() - self.time_since_last_update > self.UPDATE_FREQUENCY:
            new_info = self.read_json()
            if new_info:
                self.info = new_info
        print(self.info["ongoing"])
        return self.info["ongoing"]

    def update_score(self, score: tuple):
        if self.player_1_score == score[0] and self.player_2_score == score[1]:
            return
        else:
            self.player_1_score = score[0]
            self.player_2_score = score[1]
            self.write_json()

    def read_json(self):
        if self.file_path.exists():
            with open(self.file_path, 'r') as json_file:
                data = json.load(json_file)
                print(data)
                return data
        else:
            print("no file yet")
            return None

    def get_difficulty(self):
        difficulty = self.info["difficulty"]
        return difficulty

    def get_game_mode(self):
        game_mode = self.info["game_mode"]
        return game_mode

    def write_json(self):
        with open(self.file_path, 'w') as json_file:
            json.dump(self.info, json_file)

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
                print("File doesn't exist")
            time.sleep(1)

    def end_game(self):
        self.ack = True
        self.write_json()