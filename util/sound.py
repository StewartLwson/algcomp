from pyo import Server, Sine, SfPlayer
import time
import math
from util.io import IO
import os


class Sound:
    def __init__(self):
        """
        """
        self.io = IO()
        self.pyo = Server().boot()
        self.pyo.amp = 0.2
        self.chords = self.io.load_chords()
        self.sound_path = "./sound/piano-mf-"
        self.bpm = 60

    def play_note(self, note, dur):
        """
        """
        note_name = note[0]
        note_octave = note[1]
        note_beats = note[2]
        if not note_name == "-":
            path = self.sound_path + str(note_name) + str(note_octave) + ".aif"
            sound = SfPlayer(path)
            sound.out()
            time.sleep(dur)
            sound.stop()
        else:
            time.sleep(dur)

    def play_chord(self, chord, melody=[]):
        """
        """
        chord_name = chord[0]
        chord_type = chord[1]
        chord_notes = self.chords[chord_type][chord_name]
        chord_octave = chord[2]
        chord_beats = chord[3]
        dur = 60 / self.bpm

        sounds = []

        if not chord_name == "-":
            for note in chord_notes:
                path = self.sound_path + str(note) + str(chord_octave) + ".aif"
                sounds.append(SfPlayer(path))

        for sound in sounds:
            sound.out()

        if not len(melody) == 0:
            for note in melody:
                self.play_note(note, dur * (4/chord_beats))
        else:
            time.sleep(dur)

        for sound in sounds:
            sound.stop()

    def play_comp(self, comp, bpm=60):
        """
        """
        self.pyo.start()
        self.bpm = bpm
        for chord in comp:
            self.play_chord(chord)
        self.pyo.stop()

    def play_melody(self, melody, bpm=60):
        """
        """
        self.pyo.start()
        beat = 60/bpm
        for note in melody:
            print(note)
            if note == "-":
                time.sleep(beat)
            else:
                self.play_note(note)
        self.pyo.stop()

    def play_both(self, melody, comp, bpm=60):
        """
        """
        if(self.check_sync(melody, comp)):
            self.pyo.start()
            self.bpm = bpm
            melody_start = 0
            for chord in comp:
                drums = SfPlayer("sound/drums2.wav", speed=bpm/120)
                drums.out()
                chord_beats = chord[3]
                melody_fragment = melody[melody_start:melody_start + chord_beats]
                print(chord)
                print(melody_fragment)
                self.play_chord(chord, melody_fragment)
                melody_start = melody_start + chord_beats
            self.pyo.stop()
        else:
            print("Please check that the total number of beats for both parts are equal.")

    def check_sync(self, melody, comp):
        """
        """
        total_note_beats = 0
        for note in melody:
            note_beats = note[2]
            total_note_beats += note_beats
        total_chord_beats = 0
        for chord in comp:
            chord_beats = chord[3]
            total_chord_beats += chord_beats
        print(total_note_beats)
        print(total_chord_beats)
        return total_note_beats == total_chord_beats
