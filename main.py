from MinecraftClasses import InstrumentPalate, CommandBuilder
from FileHandling import FileHandler, MidiNote, MidiData
from mido import bpm2tempo

tmp_debug_datapack_path_remove_later_do_not_forget = r"C:\Users\chaos\curseforge\minecraft\Instances\1.20.4\saves\New World\datapacks\NoteBlockDataBack"


def main() -> None:
    midi_data: MidiData = FileHandler.read_midi_data("Music/Lagtrain.mid")
    tcr = MidiNote.calculate_tcr(midi_data.ticks_per_beat, bpm2tempo(147))

    instrument_palate = InstrumentPalate.default_palate()

    playsound_commands = CommandBuilder.generate_playsound_notes(instrument_palate, midi_data.notes, tcr, True)
    place_commands = CommandBuilder.generate_place_commands(instrument_palate, midi_data.notes[:100], tcr)

    FileHandler.build_data_pack(tmp_debug_datapack_path_remove_later_do_not_forget, playsound_commands, place_commands)


if __name__ == "__main__":
    main()
