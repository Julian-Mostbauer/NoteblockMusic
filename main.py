from HelperClasses import Note, Position, NoteBuilder
import mido

datapack_path = r"C:\Users\chaos\curseforge\minecraft\Instances\1.20.4\saves\New World\datapacks\NoteBlockDataBack"


# https://flat.io/score/636fcb42355217e28deaac0f-ragutorein-dao-xie-tan
# https://github.com/TheInfamousAlk/nbs
# https://www.reddit.com/r/MinecraftCommands/comments/16jlffl/how_can_i_get_a_disc_song_to_play_then_wait_for/

class CommandBuilder:
    @staticmethod
    def __place_command__(position: Position, note: Note) -> str:
        return f"setblock {position} minecraft:note_block[note={note}]"

    @staticmethod
    def __build_playsound__(i: int, delay_rate: float, pitch: float) -> str:
        return f"execute if score timer is_playing matches 1 if score timer music matches {round(i * delay_rate)} as @a at @s run playsound minecraft:block.note_block.harp master @a ~ ~ ~ 1 {pitch}"

    @staticmethod
    def playsound(midi_notes: [int], bpm: int, pure_noteblock_sounds: bool = False) -> str:
        delay_rate: float = 60.0 / bpm
        minecraft_pitches: [float] = [NoteBuilder.midi_to_note(note).get_pitch() for note in
                                      midi_notes] if pure_noteblock_sounds else [2 ** ((note - 57) / 12) for note in
                                                                                 midi_notes]
        return "\n".join(
            CommandBuilder.__build_playsound__(i, delay_rate, pitch)
            for i, pitch in enumerate(minecraft_pitches)
        )


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
