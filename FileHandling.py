import mido
from mido import bpm2tempo

from NoteHandling import MidiNote


class FileHandler:
    ##################
    # static methods #
    ##################

    @staticmethod
    def read_midi_data(file: str, bpm) -> tuple[[MidiNote], float]:
        midi_file = mido.MidiFile(file)
        notes_with_time = []
        current_time = 0

        for track in midi_file.tracks:
            for msg in track:
                # Increment current time by the delta time of this message
                current_time += msg.time

                # Check if the message is a 'note_on' event with non-zero velocity
                if msg.type == 'note_on' and msg.velocity > 0:
                    notes_with_time.append(MidiNote(msg.note, current_time))

        return notes_with_time, MidiNote.calculate_minecraft_tick_ratio(midi_file.ticks_per_beat, bpm2tempo(bpm))

    @staticmethod
    def build_data_pack(content: str, datapack_path: str) -> None:
        ## create the notes
        with open(datapack_path + r"\data\main\functions\notes.mcfunction", "w") as f:
            f.write(content)
