from MinecraftClasses import InstrumentPalate, CommandBuilder
from FileHandling import FileHandler, MidiNote, MidiData
from mido import bpm2tempo

from common import BuildMode


def main() -> None:
    fh: FileHandler = FileHandler(BuildMode.RELEASE)

    midi_data: MidiData = fh.read_midi_data()
    tcr = MidiNote.calculate_tcr(midi_data.ticks_per_beat, bpm2tempo(147))

    instrument_palate = InstrumentPalate.default_palate()

    playsound_commands = CommandBuilder.generate_playsound_notes(instrument_palate, midi_data.notes, tcr, True)
    place_commands = CommandBuilder.generate_place_commands(instrument_palate, midi_data.notes[:10], tcr)

    fh.build_data_pack(playsound_commands, place_commands)


if __name__ == "__main__":
    main()
