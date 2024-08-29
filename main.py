from HelperClasses import *
import mido

datapack_path = r"C:\Users\chaos\curseforge\minecraft\Instances\1.20.4\saves\New World\datapacks\NoteBlockDataBack"


def get_midi_notes(file: str) -> list[int]:
    midi_file = mido.MidiFile(file)
    return [msg.note for track in midi_file.tracks for msg in track if msg.type == 'note_on' and msg.velocity > 0]


def main() -> None:
    bpm = 145
    midi_notes: [int] = get_midi_notes("Music/Lagtrain.mid")
    output = CommandBuilder.playsound(midi_notes, bpm)

    with open(datapack_path + r"\data\main\functions\notes.mcfunction", "w") as f:
        f.write(output)

    if __name__ == "__main__":
        main()
