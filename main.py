from MinecraftClasses import *
from FileHandling import FileHandler

tmp_debug_datapack_path_remove_later_do_not_forget = r"C:\Users\chaos\curseforge\minecraft\Instances\1.20.4\saves\New World\datapacks\NoteBlockDataBack"


def main() -> None:
    # tcr = tick_convertion_ratio
    [midi_notes, tcr] = FileHandler.read_midi_data("Music/Lagtrain.mid", 147)

    output = CommandBuilder.playsound(midi_notes, tcr)

    FileHandler.build_data_pack(output, tmp_debug_datapack_path_remove_later_do_not_forget)


if __name__ == "__main__":
    main()
