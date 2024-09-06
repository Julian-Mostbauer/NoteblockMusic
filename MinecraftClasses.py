import copy

from common import Block, Position
from NoteHandling import MinecraftNoteBuilder, MinecraftNote, MidiNote, InstrumentPalate
from enum import Enum
from typing import Dict, List, Final


class CommandBuilder:
    @staticmethod
    def __place_command__(block: Block, position_relative: bool = True) -> str:
        return f"setblock {block.relative_str() if position_relative else block.absolute_str()}"

    @staticmethod
    def generate_place_commands(instrument_palate, midi_notes: List[MidiNote], tcr: float,
                                position_relative: bool = True) -> str:

        blocks = CommandBuilder.__midi_notes_to_blocks__(instrument_palate, midi_notes, tcr)
        return "\n".join(CommandBuilder.__place_command__(block, position_relative) for block in blocks)

    @staticmethod
    def __midi_notes_to_blocks__(instrument_palate: InstrumentPalate, midi_notes: List[MidiNote], tcr: float) -> List[
        Block]:
        blocks: List[Block] = []
        position = Position(0, 0, 0)
        was_previous_delay = False

        for i, midi_note in enumerate(midi_notes):
            was_previous_delay = True
            delay = midi_notes[i].time if i == 0 else midi_notes[i].time - midi_notes[i - 1].time
            delay = round(delay / tcr)  # convert to minecraft ticks

            if delay > 0:
                delay_blocks = RedstoneHandler.delay_to_minecraft_blocks(delay, position)
                print(delay, [db.absolute_str() for db in delay_blocks])
                delay_block_offset = (delay_blocks[-1].position - delay_blocks[0].position)
                position += delay_block_offset + Position(1, 0, 0)
                blocks += delay_blocks
            else:
                print("no delay")
                was_previous_delay = False

            if was_previous_delay:
                position += Position(1, 0, 0)  # offset of a note in direction of the next note will always be 1
                note_blocks = MinecraftNoteBuilder.midi_to_note_blocks(instrument_palate, midi_note, position)
            else:
                position += Position(0, 0, 1)
                note_blocks = MinecraftNoteBuilder.midi_to_note_blocks(instrument_palate, midi_note, position)
                position -= Position(0, 0, 1)

            blocks += note_blocks
        return blocks

    @staticmethod
    def __build_playsound__(time: int, note: MinecraftNote, debug: bool = False) -> str:
        timing_prefix = f"execute if score timer is_playing matches 1 if score timer music matches {time} as @a at @s run"
        return f"{timing_prefix} playsound minecraft:block.note_block.{note.instrument} master @a ~ ~ ~ 1 {note.get_pitch()}" + (
            f"\n{timing_prefix} tellraw @a \"<music-player> {time}: playing {note.get_pitch()} with {note.instrument}\"" if debug else "")

    @staticmethod
    def generate_playsound_notes(instrument_palate: InstrumentPalate, midi_notes: List[MidiNote], tcr: float,
                                 debug: bool = False) -> str:
        return "\n".join(
            CommandBuilder.__build_playsound__(round(midi_note.time / tcr),
                                               MinecraftNoteBuilder.midi_to_note(midi_note.midi_key, instrument_palate),
                                               debug)
            for midi_note in midi_notes
        )


class RedstoneHandler:
    class RedstoneDelays(Enum):
        Repeater_1 = 2
        PistonRepeater = 3
        Repeater_2 = 4
        Repeater_3 = 6
        Repeater_4 = 8

        def to_blocks(self, offset_origin: Position) -> [Block]:
            if self.value != 3:
                return [
                    Block("repeater", {"delay": self.value // 2, "facing": "west"}, offset_origin + Position(3, 0, 0))]
            else:
                return [Block("sticky_piston", {"facing": "east"}, offset_origin),
                        Block("redstone_block", {}, offset_origin + Position(1, 0, 0)),
                        Block("redstone_wire", {}, offset_origin + Position(3, 0, 0))]

    default_delay_values: Final[List[int]] = [b.value for b in RedstoneDelays]

    @staticmethod
    def cheapest_combination(n: int, nums: List[int] = None) -> List[int]:
        # one tick is not possible, and will be rounded up to 2
        if n == 1:
            return [2]

        result: List[int] = []
        nums = copy.deepcopy(RedstoneHandler.default_delay_values) if nums is None else nums

        if n % 2 == 1:
            result.append(3)
            n -= 3

        while n > 0:
            while nums[-1] > n:
                nums.pop()

            result.append(nums[-1])
            n -= nums[-1]

        return result

    @staticmethod
    def delay_to_minecraft_blocks(delay: int, origin_offset: Position = Position(0, 0, 0)) -> List[Block]:
        delays = RedstoneHandler.cheapest_combination(delay)
        redstone_delays = [RedstoneHandler.RedstoneDelays(d) for d in delays]
        blocks: List[Block] = []
        for i, redstone_delay in enumerate(redstone_delays):
            blocks += redstone_delay.to_blocks(Position(i, 0, 0) + origin_offset)
            i += 1 if redstone_delay.value != 3 else 4  # piston repeater width
        return blocks
