from pyo import Server, Sine, SfPlayer
import time
import math

class Sound:
    def __init__(self, key = "c", scale = "minor", octave = 4, sound = "synth"):
        # Pyo server
        self.pyo = Server().boot()

        # Key center for composition
        self.key = key

        # Choice of sound to use for playing compositions
        # synth uses pyo's default Sine wave
        # piano uses a pitched sample of a piano
        self.sound = sound

        # Lowest pitch value for every note
        self.notes_dict = { "c": 16.35, "c#": 17.32, "d": 18.35, "d#": 19.45,
        "e": 20.60, "f": 21.83, "f#": 23.12, "g": 24.50, "g#": 25.96,
        "a": 27.50, "a#": 29.14, "b": 30.87 }

        # Scale degrees
        self.scales_dict = { "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10], "minor_pent": [0, 3, 7, 10],
        "minor_blues": [0, 3, 6, 7, 10] }

        # Name of scale being used to be looked up in dictionary
        self.scale = scale

        # List of degrees for the given scale
        self.scale_degrees = self.scales_dict[self.scale]

        # List of note names
        self.notes_list = list(self.notes_dict.keys())

        # Position to shift when re-ordering notes
        self.set_key(self.key)

        # Octave to start with
        self.octave = octave

        # Chords according to given scale starting at given octave
        self.chords = self.get_chords(self.scale, self.octave)

        # Notes according to given scale starting at given octave
        self.notes = self.get_notes(self.scale, self.octave + 1)

    # Sets the key by repositioning notes_list to start with a given note
    # key is the note given to start the repositioned list
    def set_key(self, key):
        start = self.notes_list.index(key)
        for _ in range(start):
            self.notes_list.append(self.notes_list.pop(0))

    def get_chords(self, scale, octave):
        chords = []
        self.octave = octave
        for degree in self.scale_degrees:
            if degree >= self.notes_list.index("c") and self.key is not "c":
                self.octave = octave + 1
            note = self.notes_dict[self.notes_list[degree]] * (2**self.octave)
            if self.sound == "synth":
                chords.append(Sine(freq=[note, note * (3/2)], phase=0, mul=0.1))
            elif self.sound == "piano":
                base = self.notes_dict["c"] * (2**4)
                chords.append(SfPlayer("./sound/Piano.mf.C4.aiff", speed=[note/base, note/base * (3/2)]))
        return chords

    def get_notes(self, scale, octave):
        notes = []
        self.octave = octave
        for degree in self.scale_degrees:
            if degree >= self.notes_list.index("c") and self.key is not "c":
                self.octave = octave + 1
            note = self.notes_dict[self.notes_list[degree]] * (2**self.octave)
            if self.sound == "synth":
                notes.append(Sine(freq=note, phase=0, mul=0.1))
            elif self.sound == "piano":
                base = self.notes_dict["c"] * (2**octave)
                notes.append(SfPlayer("./sound/Piano.mf.C4.aiff", speed=(note/base)))
        return notes

    def play_comp(self, comp, bpm=60):
        self.pyo.start()
        for chord in comp:
            self.chords[int(chord) - 1].out()
            time.sleep(60 / bpm)
            self.chords[int(chord) - 1].stop()
        self.pyo.stop()

    def play_melody(self, melody, bpm=60):
        self.pyo.start()
        for note in melody:
            i = self.scale_degrees.index(note)
            self.notes[i].out()
            time.sleep(60 / bpm)
            self.notes[i].stop()
        self.pyo.stop()

    def play_both(self, melody, comp, bpm=60):
        self.pyo.start()
        melody_start = 0
        line = int(len(melody) / len(comp))
        for chord in comp:
            self.chords[int(chord) - 1].out()
            for note in melody[melody_start:melody_start + line]:
                j = self.scale_degrees.index(note)
                self.notes[j].out()
                time.sleep(60 / (bpm * line))
                self.notes[j].stop()
            self.chords[int(chord) - 1].stop()
            melody_start = melody_start + line
        self.pyo.stop()








