from dataclasses import dataclass
from enum import Enum
from typing import List

class InstrName(Enum):
    NOOP = 0
    ADDX = 1

INSTR_TO_ENUM = {"noop": InstrName.NOOP, "addx": InstrName.ADDX}

@dataclass
class Instr:
    name: InstrName
    val: int = None

    def __init__(self, name, val=None):
        self.name = INSTR_TO_ENUM[name]
        if val:
            self.val = int(val)

@dataclass
class Register:
    name: str
    val: int = 1

    def do(self, instr: Instr) -> None:
        if instr.name == InstrName.ADDX:
            self.add(instr.val)

    def add(self, val: int) -> None:
        self.val += val


@dataclass
class Sprite:
    pos: int = 0
    size: int = 3


class SignalReader:
    def __init__(self, data: List[Instr]):
        self.instr_lst = data
        self.to_do_queue = []
        self.cycle = 0
        self.X = Register("X")

    def reset_cycles(self) -> None:
        self.cycle = 0

    def reset_queue(self) -> None:
        self.to_do_queue.clear()

    def reset_register(self) -> None:
        self.X.val = 0

    def reset(self) -> None:
        self.reset_cycles()
        self.reset_queue()
        self.reset_register()
        self.instr_to_queue()

    def instr_to_queue(self) -> None:
        for i, instr in enumerate(self.instr_lst):
            if instr.name == InstrName.NOOP:
                self.to_do_queue.append(None)

            elif instr.name == InstrName.ADDX:
                self.to_do_queue.append(None)
                self.to_do_queue.append(instr)

    def get_total_strength(self) -> int:
        self.reset()

        total_strength = 0

        for todo in self.to_do_queue:
            self.cycle += 1

            if (self.cycle - 20) % 40 == 0:
                total_strength += self.get_strength()

            if todo == None:
                continue

            elif isinstance(todo, Instr):
                self.X.do(todo)

        self.to_do_queue.clear()
        return total_strength

    def get_strength(self) -> int:
        return self.cycle * self.X.val


class Screen:
    def __init__(self, w=40, h=6):
        self.w = w
        self.h = h
        self.ascii = ["." for _ in range(w * h)]
        self.sprite = Sprite()

    def display(self) -> None:
        for y in range(6):
            for x in range(40):
                print(f"{self.ascii[(y*self.w)+x]}", end="")
            print("")


class Device:
    def __init__(self, data: List[Instr]):
        self.signal_reader = SignalReader(data)
        self.screen = Screen()

    def check_if_lit(self, line_cycle: int) -> bool:
        if  (line_cycle - 1) >= self.screen.sprite.pos \
        and (line_cycle - 1) <  self.screen.sprite.pos + self.screen.sprite.size:
            return True

        return False

    def generate_screen_display(self) -> None:
        self.signal_reader.reset()

        line_cycle = 0

        for todo in self.signal_reader.to_do_queue:
            self.signal_reader.cycle += 1
            line_cycle += 1

            if line_cycle > 39:
                line_cycle = 0

            print("-------------------------")
            print(f"Sprite pos   : {self.screen.sprite.pos}")
            print(f"Current cycle: {self.signal_reader.cycle} (-1 for idx on screen)")
            print(f"Is lit       : {self.check_if_lit(line_cycle)}")
            print(f"Current todo : {todo}")
            line = ["." for x in range (40)]
            line[self.screen.sprite.pos] = "#"
            line[self.screen.sprite.pos + 1] = "#"
            line[self.screen.sprite.pos + 2] = "#"
            line[line_cycle - 1] = "o"
            print(f"Sprite pos   : ")
            print(f"{''.join(line)}")
            print("Current screen:")
            self.screen.display()
            print("-------------------------")

            if self.check_if_lit(line_cycle):
                self.screen.ascii[self.signal_reader.cycle - 1] = "#"

            if isinstance(todo, Instr):
                self.signal_reader.X.do(todo)
                self.screen.sprite.pos = self.signal_reader.X.val - 1 # -1 because the register value is the center of the sprite
            

            if line_cycle == 10:
                breakpoint()
def load_and_format_data():
    """ Loads the data in a list of Instr """
    data = []

    with open("test_data.txt", "r") as input_file:
        content = input_file.read()

        for line in content.split("\n"):
            s_line = line.split(" ")
            data.append(Instr(*s_line))
        
    return data

def main():
    data = load_and_format_data()
    device = Device(data)
    print(f"Total signal strength: {device.signal_reader.get_total_strength()}")
    device.generate_screen_display()
    device.screen.display()

if __name__ == "__main__":
    main()