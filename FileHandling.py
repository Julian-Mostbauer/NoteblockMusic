import mido
from mido import bpm2tempo

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from NoteHandling import MidiNote


class MidiData:
    def __init__(self, notes: list[MidiNote], ticks_per_beat: int):
        self.notes: list[MidiNote] = notes
        self.ticks_per_beat: int = ticks_per_beat
        self.max_note = max(notes, key=lambda x: x.midi_key).midi_key
        self.min_note = min(notes, key=lambda x: x.midi_key).midi_key

    def display_debug_info(self, tcr: float) -> None:
        too_large_notes = [note for note in self.notes if note.midi_key > MidiNote.conversion_note_range.stop - 1]
        too_small_notes = [note for note in self.notes if note.midi_key < MidiNote.conversion_note_range.start]
        clipped_notes = too_large_notes + too_small_notes

        print("Debug Info: ")
        print("Total Midi Notes: ", len(self.notes))
        print(f"Tick Convertion Ratio: {tcr}")
        print(f"Total play time:  {self.notes[-1].time / (20 * tcr)}s")
        print("Midi Note Info:")
        print(f"\tMax Note: {self.max_note}")
        print(f"\tMin Note: {self.min_note}")

        print("Clamped Notes:")
        print("\tTotal Clamped Notes: ", len(clipped_notes))
        print("\tToo high: ", len(too_large_notes))
        print("\tToo low: ", len(too_small_notes))

    def plot_notes(self):
        # Make a diagram of the notes
        plt.title = "Midi Notes"
        fig, ax = plt.subplots()
        ax.set_xlim([0, self.notes[-1].time])
        ax.set_ylim([self.min_note, self.max_note])

        for note in self.notes:
            ax.add_patch(mpatches.Rectangle((note.time, note.midi_key), 1, 1, color='blue'))

        plt.show()
        plt.close()


class FileHandler:
    ##################
    # static methods #
    ##################

    @staticmethod
    def read_midi_data(file: str) -> MidiData:
        midi_file = mido.MidiFile(file)
        notes_with_time: list[MidiNote] = []
        current_time = 0

        for track in midi_file.tracks:
            for msg in track:
                # Increment current time by the delta time of this message
                current_time += msg.time

                if msg.type == 'note_on' and msg.velocity > 0:
                    notes_with_time.append(MidiNote(msg.note, current_time))

        return MidiData(notes_with_time, midi_file.ticks_per_beat)

    @staticmethod
    def build_data_pack(content: str, datapack_path: str) -> None:
        ## create the notes
        with open(datapack_path + r"\data\main\functions\notes.mcfunction", "w") as f:
            f.write(content)
