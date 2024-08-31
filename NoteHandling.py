from enum import Enum


class MidiNote:
    note_range = range(0, 128)
    conversion_note_range = range(20, 95)
    
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
    def calculate_tcr(ticks_per_beat: int, tempo_in_microseconds_per_beat: int) -> float:
        """
            Calculate the Tick Conversion Ratio (TCR).
        
            The TCR is used to convert MIDI ticks to minecraft ticks.
        
            Parameters:
            ticks_per_beat (int): The number of MIDI ticks per beat.
            tempo_in_microseconds_per_beat (int): The tempo in microseconds per beat.
        
            Returns:
            float: The tick conversion ratio.
        """
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
        # midi note range of 0-127 is too large to fit into the 0-74 range of the note block
        # shrinking the range, would make the notes sound too similar
        # instead, a subrange of the most common notes is taken
        # to preserve the most important notes
        # choosen range: 20-94

        # clamp the midi note to the conversion range
        midi_note = min(max(midi_note, MidiNote.conversion_note_range.start), MidiNote.conversion_note_range.stop - 1)
    
        max_midi_note = MidiNote.note_range.stop - 1
        max_raw_note = Note.raw_note_range.stop - 2
        max_note = Note.note_range.stop - 1

        raw_note: int = midi_note - 20
        instrument_index = min(2, raw_note // (max_note + 1))
        instrument: Instrument = Instrument(instrument_index)
        note_index: int = raw_note % (max_note + 1)

        return Note(note_index, instrument)
