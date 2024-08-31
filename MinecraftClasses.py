from NoteHandling import NoteBuilder, Note, MidiNote
from typing import List

class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"{self.x} {self.y} {self.z}"


class CommandBuilder:
    ##################
    # static methods #
    ##################

    @staticmethod
    def __place_command__(position: Position, note: Note) -> str:
        return f"setblock {position} minecraft:note_block[note={note}]"

    @staticmethod
    def __build_playsound__(time: int, note: Note, debug: bool = False) -> str:
        timing_prefix = f"execute if score timer is_playing matches 1 if score timer music matches {time} as @a at @s run"
        return f"{timing_prefix} playsound minecraft:block.note_block.{note.instrument} master @a ~ ~ ~ 1 {note.get_pitch()}" + (
            f"\n{timing_prefix} tellraw @a \"<music-player> {time}: playing {note.get_pitch()} with {note.instrument}\"" if debug else "")

    @staticmethod
    def playsound(midi_notes: List[MidiNote], tcr: float, debug: bool = False) -> str:
        return "\n".join(
            CommandBuilder.__build_playsound__(round(midi_note.time / tcr),
                                               NoteBuilder.midi_to_note(midi_note.midi_key), debug)
            for midi_note in midi_notes
        )
