from enum import Enum


class MidiNote:
    note_range = range(0, 128)

    def __init__(self, midi_key: int, time: int):
        if midi_key not in MidiNote.note_range:
            raise ValueError(f"Midi note must be in {MidiNote.note_range}")

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


class Instrument(Enum):
    BASS = 0
    PLING = 1
    XYLOPHONE = 2

    def __str__(self) -> str:
        return self.name.lower().removeprefix("instrument.")


class Note:
    note_range = range(0, 25)
    raw_note_range = range(0, 75)

    def __init__(self, note_index: int, instrument: Instrument):
        if note_index not in Note.note_range:
            raise ValueError(f"Note must be in {Note.note_range}")
        self.note_index = note_index
        self.instrument = instrument

    def __str__(self) -> str:
        return f"[node_index: {self.note_index}, instrument: {self.instrument}]"

    def get_pitch(self) -> float:
        return 2 ** ((self.note_index - 12) / 12)

    def get_raw_note(self) -> int:
        return self.note_index + self.instrument.value * Note.note_range.stop


class NoteBuilder:
    ##################
    # static methods #
    ##################

    @staticmethod
    def midi_to_note(midi_note: int) -> Note:
        # map the range of the midi_note(0 to 127) to the range of the note_index(0 to 24), but the note_index has 3 layers, so in total 74 notes
        # the reason it is only 74 and not 75 is unclear to me at the moment, because I am writing this code late in the night,
        # but this works without errors, so I will leave it like this for now

        max_midi_note = MidiNote.note_range.stop - 1
        max_raw_note = Note.raw_note_range.stop - 2
        max_note = Note.note_range.stop - 1

        raw_note: int = round(midi_note * (max_raw_note + 1) / max_midi_note)
        instrument_index = min(2, raw_note // (max_note + 1))
        instrument: Instrument = Instrument(instrument_index)
        note_index: int = raw_note % (max_note + 1)

        return Note(note_index, instrument)
