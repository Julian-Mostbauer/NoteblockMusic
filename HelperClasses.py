import math


class Note:
    note_range = range(0, 25)

    def __init__(self, note_index: int):
        if note_index not in Note.note_range:
            raise ValueError(f"Note must be in {Note.note_range}")
        self.note_index = note_index

    def __str__(self):
        return f"{self.note_index}"

    def get_pitch(self) -> float:
        return 2 ** ((self.note_index - 12) / 12)


class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"


class NoteBuilder:
    @staticmethod
    def note_from_index(note: int):
        return Note(note)

    @staticmethod
    def midi_to_note_index(midi_note: int) -> int:
        return round((midi_note - 57) / (81 - 57) * 24)

    @staticmethod
    def midi_to_note(midi_note: int) -> Note:
        # restrict the range of midi notes to the range of the note blocks
        if midi_note < 57:
            midi_note = 57
        if midi_note > 81:
            midi_note = 81
        
        return Note(NoteBuilder.midi_to_note_index(midi_note))
