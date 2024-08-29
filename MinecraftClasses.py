from NoteHandling import NoteBuilder, Note, MidiNote


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
    def __build_playsound__(time: int, pitch: float) -> str:
        return f"execute if score timer is_playing matches 1 if score timer music matches {time} as @a at @s run playsound minecraft:block.note_block.harp master @a ~ ~ ~ 1 {pitch}"

    @staticmethod
    def playsound(midi_notes: [MidiNote], tick_convertion_ratio: float) -> str:
        return "\n".join(
            CommandBuilder.__build_playsound__(round(midi_note.time / tick_convertion_ratio),
                                               Note.midi_note_to_pitch(midi_note.midi_key))
            for midi_note in midi_notes
        )
