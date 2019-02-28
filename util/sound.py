from pyo import Server, Sine, SfPlayer
import time
import math

class Sound:
    def __init__(self, key = "c", scale = "minor", octave = 4, sound = "synth", style="blues"):
        # Pyo server
        self.pyo = Server().boot()

        # Key center for composition
        self.key = key

        # Choice of sound to use for playing compositions
        # synth uses pyo's default Sine wave
        # piano uses a pitched sample of a piano
        self.sound = sound

        self.style = style

        # Lowest pitch value for every note
        self.notes_dict = { "c": 16.35, "c#": 17.32, "d": 18.35, "d#": 19.45,
        "e": 20.60, "f": 21.83, "f#": 23.12, "g": 24.50, "g#": 25.96,
        "a": 27.50, "a#": 29.14, "b": 30.87 }

        # Scale degrees
        self.scales_dict = { "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "minor_pent": [0, 3, 5, 7, 10],
        "minor_blues": [0, 3, 5, 6, 7, 10] }

        self.chord_dict = { "maj7": [1, 5/4, 3/2, 15/8], "min7": [1, 6/5, 3/2, 16/9],
        "dom7": [1, 5/4, 3/2, 16/9], "halfdim7": [1, 6/5, 25/18, 16/9], "five": [1, 3/2] }

        self.diatonic_dict = { "major": [self.chord_dict["maj7"], self.chord_dict["min7"],
        self.chord_dict["min7"], self.chord_dict["maj7"], self.chord_dict["dom7"],
        self.chord_dict["min7"], self.chord_dict["halfdim7"]], "minor": [self.chord_dict["min7"],
        self.chord_dict["halfdim7"], self.chord_dict["maj7"], self.chord_dict["min7"],
        self.chord_dict["min7"], self.chord_dict["maj7"], self.chord_dict["dom7"]] }

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
        self.chords = self.get_chords(self.octave, self.style)

        # Notes according to given scale starting at given octave
        self.notes = self.get_notes(self.scale, self.octave + 1)

    # Sets the key by repositioning notes_list to start with a given note
    # key is the note given to start the repositioned list
    def set_key(self, key):
        start = self.notes_list.index(key)
        for _ in range(start):
            self.notes_list.append(self.notes_list.pop(0))

    def get_chords(self, octave, style):
        chords = []
        scale = []
        chord_list = []
        self.octave = octave
        if style == "minor_jazz":
            scale = self.scales_dict["minor"]
            chord_list = self.diatonic_dict["minor"]
        elif style == "major_jazz":
            scale = self.scales_dict["major"]
            chord_list = self.diatonic_dict["major"]
        elif style == "blues":
            scale = self.scales_dict["minor"]
        for c, degree in enumerate(scale):
            if degree >= self.notes_list.index("c") and self.key is not "c":
                self.octave = octave + 1
            note = self.notes_dict[self.notes_list[degree]] * (2**self.octave)
            if self.sound == "synth":
                if style == "blues":
                    chords.append(Sine(freq=[note, note * self.chord_dict["five"]], phase=0, mul=0.1))
                else:
                    chords.append(Sine(freq=[note, note * chord_list[c][1], note * chord_list[c][2], note * chord_list[c][3]], phase=0, mul=0.1))
            elif self.sound == "piano":
                base = self.notes_dict["c"] * (2**4)
                note = note/base
                if style == "blues":
                    chords.append(SfPlayer("./sound/Piano.mf.C4.aiff", speed=[note, note * self.chord_dict["five"][1]]))
                else:
                    current = chord_list[c]
                    chords.append(SfPlayer("./sound/Piano.mf.C4.aiff", speed=[note, note * current[1], note * current[2], note * current[3]]))
        return chords

    def get_notes(self, scale, octave):
        notes = []
        self.octave = octave + 1
        for degree in self.scale_degrees:
            if degree >= self.notes_list.index("c") and self.key is not "c":
                self.octave = octave + 2
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
            if chord == "-":
                time.sleep(60 / bpm)
            else:
                self.chords[int(chord) - 1].out()
                time.sleep(60 / bpm)
                self.chords[int(chord) - 1].stop()
        self.pyo.stop()

    def play_melody(self, melody, bpm=60):
        self.pyo.start()
        for note in melody:
            if note == "-":
                time.sleep(60 / bpm)
            else:
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
            if chord == "-":
                Sine(freq=0).out()
            else:
                self.chords[int(chord) - 1].out()
            for note in melody[melody_start:melody_start + line]:
                if note == "-":
                    time.sleep(60 / (bpm * line))
                else:
                    j = self.scale_degrees.index(note)
                    self.notes[j].out()
                    time.sleep(60 / (bpm * line))
                    self.notes[j].stop()
            if chord == "-":
                Sine(freq=0).stop()
            else:
                self.chords[int(chord) - 1].stop()
            melody_start = melody_start + line
        self.pyo.stop()








