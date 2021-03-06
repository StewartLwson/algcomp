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

    def load_song(self, filename, folder):
        path = "./songs/" + folder + "/" + filename + ".json"
        data = self.load_json(path)
        return data["melody"], data["comp"]

    def save_song(self, folder, melody, comp, info, filename=""):
        if filename == "":
            filename = str(hashlib.sha1(
                str(melody).encode("utf-8")).hexdigest())
        path = "./songs/" + folder + "/" + filename + ".json"
        data = {
            "melody": melody,
            "comp": comp,
            "info": info
        }
        self.save_json(path, data)

    def load_chords(self):
        path = "./music/chords.json"
        data = self.load_json(path)
        return data

    def load_scales(self):
        path = "./music/scales.json"
        data = self.load_json(path)
        return data
