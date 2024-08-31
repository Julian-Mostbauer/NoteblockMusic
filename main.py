from MinecraftClasses import *
from FileHandling import *

tmp_debug_datapack_path_remove_later_do_not_forget = r"C:\Users\chaos\curseforge\minecraft\Instances\1.20.4\saves\New World\datapacks\NoteBlockDataBack"


def main() -> None:
    midi_data: MidiData = FileHandler.read_midi_data("Music/Lagtrain.mid")
    tcr = MidiNote.calculate_tcr(midi_data.ticks_per_beat, bpm2tempo(147))

    midi_data.display_debug_info(tcr)
    
    output = CommandBuilder.playsound(midi_data.notes, tcr, True)

    FileHandler.build_data_pack(output, tmp_debug_datapack_path_remove_later_do_not_forget)


if __name__ == "__main__":
    main()
