import json
import hashlib

class IO:
    def __init__(self):
        pass

    def load_json(self, path):
        data = {}
        with open(path, "r") as infile:
            data = json.load(infile)
        return data

    def save_json(self, path, data):
        with open(path, "w") as outfile:
            json.dump(data, outfile)

    def load_training_data(self, filename):
        path = "./training data/" + filename + ".json"
        data = self.load_json(path)
        return data

    def save_training_data(self, filename, data):
        path = "./training data/" + filename + ".json"
        data = {
            "data": data
        }
        self.save_json(path, data)

    def load_song(self, filename, style):
        path = "./songs/" + style + "/" + filename + ".json"
        data = self.load_json(path)
        return data["melody"], data["comp"]

    def save_song(self, filename, style, melody, comp):
        filename = str(hashlib.sha1(str(filename).encode("utf-8")).hexdigest())
        path = "./songs/" + style + "/" + filename + ".json"
        data = {
            "melody": melody,
            "comp": comp,
        }
        self.save_json(path, data)

    def load_chords(self):
        path = "./music/chords.json"
        data = self.load_json(path)
        return data