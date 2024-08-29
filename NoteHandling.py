class Note:
    note_range = range(0, 25)

    def __init__(self, note_index: int):
        if note_index not in Note.note_range:
            raise ValueError(f"Note must be in {Note.note_range}")
        self.note_index = note_index

    def __str__(self) -> str:
        return f"{self.note_index}"

    def get_pitch(self) -> float:
        return 2 ** ((self.note_index - 12) / 12)

    ##################
    # static methods #
    ##################

    @staticmethod
    def midi_note_to_pitch(midi_note: int) -> float:
        return NoteBuilder.midi_to_note(midi_note).get_pitch()


class NoteBuilder:
    ##################
    # static methods #
    ##################

    @staticmethod
    def note_from_index(note: int) -> Note:
        return Note(note)

    @staticmethod
    def midi_to_note(midi_note: int) -> Note:
        # restrict the range of midi notes to the range of the note blocks
        midi_note -= 57
        if midi_note < Note.note_range.start:
            return NoteBuilder.note_from_index(Note.note_range.start)
        elif midi_note > Note.note_range.stop - 1:
            return NoteBuilder.note_from_index(Note.note_range.stop - 1)
        else:
            return NoteBuilder.note_from_index(midi_note)


class MidiNote:
    def __init__(self, midi_key: int, time: int):
        self.midi_key: int = midi_key
        self.time: int = time

    def __str__(self) -> str:
        return f"[key: {self.midi_key}, time: {self.time}]"

    ##################
    # static methods #
    ##################

    @staticmethod
    def calculate_minecraft_tick_ratio(ticks_per_beat: int, tempo_in_microseconds_per_beat: int) -> float:
        divisor = (ticks_per_beat * 50000) / tempo_in_microseconds_per_beat
        return divisor
