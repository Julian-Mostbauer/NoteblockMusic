from __future__ import annotations
from typing import List, Dict, Tuple
from common import Block, Position


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


class Instrument:
    all_instruments: Dict[str, List[int, str]] = {
        "BASS": [0, "oak_log"],
        "DIDGERIDOO": [0, "pumpkin"],
        "GUITAR": [0.5, "black_wool"],
        "BANJO": [1, "hay_block"],
        "PLING": [1, "glowstone"],
        "HARP": [1, "air"],
        "IRON_XYLOPHONE": [1, "iron_block"],
        "BIT": [1, "emerald_block"],
        "FLUTE": [1.5, "clay"],
        "COW_BELL": [1.5, "soul_sand"],
        "XYLOPHONE": [2, "bone_block"],
        "CHIME": [2, "packed_ice"],
        "BELL": [2, "gold_block"],
        "SNARE": [3, "sand"],
        "HAT": [3, "glass"],
    }

    def __init__(self, name: str):
        if name not in Instrument.all_instruments:
            raise ValueError(f"Invalid instrument: {name}")
        self.name = name
        self.value = Instrument.all_instruments[name][0]
        self.block_name = Instrument.all_instruments[name][1]

    def __str__(self) -> str:
        return self.name.lower()


class InstrumentPalate:
    def __init__(self, instruments: Tuple[Instrument, Instrument, Instrument]):
        self.low_instrument = instruments[0]
        self.mid_instrument = instruments[1]
        self.high_instrument = instruments[2]

    def __str__(self) -> str:
        return f"[low: {self.low_instrument}, mid: {self.mid_instrument}, high: {self.high_instrument}]"

    @staticmethod
    def default_palate() -> InstrumentPalate:
        return InstrumentPalate((Instrument("BASS"), Instrument("PLING"), Instrument("XYLOPHONE")))


class MinecraftNote:
    static_note_range = range(0, 25)
    static_raw_note_range = range(0, 75)

    def __init__(self, note_index: int, instrument: Instrument):
        if note_index not in MinecraftNote.static_note_range:
            raise ValueError(f"Note must be in {MinecraftNote.static_note_range}")
        self.note_index = note_index
        self.instrument = instrument

    def __str__(self) -> str:
        return f"[node_index: {self.note_index}, instrument: {self.instrument}]"

    def get_pitch(self) -> float:
        return 2 ** ((self.note_index - 12) / 12)

    def get_raw_note(self) -> int:
        return self.note_index + self.instrument.value * MinecraftNote.static_note_range.stop


class MinecraftNoteBuilder:
    @staticmethod
    def midi_to_note(midi_note: int, instrument_palate: InstrumentPalate) -> MinecraftNote:
        # midi note range of 0-127 is too large to fit into the 0-74 range of the note block
        # shrinking the range, would make the notes sound too similar
        # instead, a subrange of the most common notes is taken
        # to preserve the most important notes
        # chosen range: 20-94

        # clamp the midi note to the conversion range
        midi_note = min(max(midi_note, MidiNote.conversion_note_range.start), MidiNote.conversion_note_range.stop - 1)

        max_note = MinecraftNote.static_note_range.stop - 1

        raw_note: int = midi_note - 20

        instrument: Instrument = instrument_palate.low_instrument if raw_note < 25 else (
            instrument_palate.mid_instrument if raw_note < 50 else instrument_palate.high_instrument)
        note_index: int = raw_note % (max_note + 1)

        return MinecraftNote(note_index, instrument)

    @staticmethod
    def midi_to_note_blocks(instrument_palate: InstrumentPalate, midi_note: MidiNote, origin_offset: Position) -> List[
        Block]:
        minecraft_note: MinecraftNote = MinecraftNoteBuilder.midi_to_note(midi_note.midi_key, instrument_palate)
        return [Block("note_block", {"note": minecraft_note.note_index}, origin_offset),
                Block(minecraft_note.instrument.block_name, {}, origin_offset + Position(0, -1, 0))]
