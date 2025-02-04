﻿import os.path

import mido
from NoteHandling import MidiNote
from tkinter import filedialog

from common import BuildMode


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
        import matplotlib.pyplot as plt
        import matplotlib.patches as m_patches

        # Make a diagram of the notes
        plt.title = "Midi Notes"
        fig, ax = plt.subplots()
        ax.set_xlim([0, self.notes[-1].time])
        ax.set_ylim([self.min_note, self.max_note])

        for note in self.notes:
            ax.add_patch(m_patches.Rectangle((note.time, note.midi_key), 1, 1, color='blue'))

        plt.show()
        plt.close()


class FileHandler:
    def __init__(self, build_mode: BuildMode):
        self.build_mode = build_mode
        self.file_path = ""
        self.pack_name = ""
        self.output_path = ""

        self.open_file()

    def open_file(self):
        self.file_path = filedialog.askopenfilename(title="Submit your midi file",
                                                    filetypes=(("Midi Files", "*.mid"), ("Midi Files", "*.midi"))
                                                    ) if (
                self.build_mode == BuildMode.RELEASE) else r"C:\Users\chaos\PycharmProjects\NoteblockMusic\Music\Young Girl A - siinamota.mid"

        self.pack_name = f"Pack_for_{os.path.basename(self.file_path).split('.')[0]}" if (
                    self.build_mode == BuildMode.RELEASE) else "DebugPack"

        self.output_path = f"Output\\{self.pack_name}" if (
                self.build_mode == BuildMode.RELEASE) else r"C:\Users\chaos\curseforge\minecraft\Instances\1.20.4\saves\New World\datapacks\NoteBlockDataBack"

    def read_midi_data(self) -> MidiData:
        if not self.file_path:
            raise FileNotFoundError("No file path provided")

        midi_file = mido.MidiFile(self.file_path)
        notes_with_time: list[MidiNote] = []
        current_time = 0

        for track in midi_file.tracks:
            for msg in track:
                # Increment current time by the delta time of this message
                current_time += msg.time

                if msg.type == 'note_on' and msg.velocity > 0:
                    notes_with_time.append(MidiNote(msg.note, current_time))

        return MidiData(notes_with_time, midi_file.ticks_per_beat)

    def build_data_pack(self, playsound_commands: str, place_commands: str) -> None:
        if not self.output_path:
            raise FileNotFoundError("No output path provided")

        # build the data pack, if release mode is used and the output path does not already exist
        if (self.build_mode == BuildMode.RELEASE) and not os.path.exists(self.output_path):
            os.makedirs(self.output_path + r"\data\main\functions", exist_ok=True)
            os.makedirs(self.output_path + r"\data\minecraft\tags\functions", exist_ok=True)

            with open(self.output_path + "\pack.mcmeta", "w") as f:
                f.write(
                    '{"pack": {"pack_format": 18, "description": "Noteblock Music Datapack, generated by NoteblockMusic(https://github.com/Julian-Mostbauer/NoteblockMusic)"}}')

            with open(self.output_path + r"\data\minecraft\tags\functions\load.json", "w") as f:
                f.write('{"values":["main:load"]}')

            with open(self.output_path + r"\data\minecraft\tags\functions\tick.json", "w") as f:
                f.write('{"values": ["main:tick"]}')

            with open(self.output_path + r"\data\main\functions\load.mcfunction", "w") as f:
                f.write(f"say Loaded {self.pack_name}" +
                        "\nscoreboard objectives add music dummy" +
                        "\nscoreboard objectives add is_playing dummy")

            with open(self.output_path + r"\data\main\functions\tick.mcfunction", "w") as f:
                f.write(
                    "scoreboard players add timer music 1\nexecute if score is_playing music matches 1 run function main:notes")

        with open(self.output_path + r"\data\main\functions\notes.mcfunction", "w") as f:
            f.write(playsound_commands)

        with open(self.output_path + r"\data\main\functions\place_music_player.mcfunction", "w") as f:
            f.write(place_commands)
