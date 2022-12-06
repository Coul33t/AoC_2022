# each stack is a LIFO (Last In First Out)
import queue
from dataclasses import dataclass

ASCII_COL_WIDTH = 3

@dataclass
class MovingInstr:
    """ Dataclass for the moving instructions """
    quantity: int
    origin: int
    destination: int

class Dock:
    """ 
        Represents a Dock, which is made of few stacks of crates (LIFOs) and a crane to move them around (run() method)
        from a list of MovingInstr
    """
    def __init__(self, deck_data, move_data):
        self.stacks = []
        self.moving_instr = []
        self.init(deck_data, move_data)

    def init(self, deck_data, move_data):
        """ 
            Initialises the Dock attributes (number of stacks, initial stacks states, moving instructions)
            from the strings of data
        """
        # ----------------------------
        #     Stacks initialisation
        # ----------------------------
        nb_stacks = max([int(x) for x in deck_data[-1].split(" ") if x != ""])
        self.stacks = [queue.LifoQueue() for i in range(nb_stacks)]

        # Insert from bottom to the top
        for i in range(len(deck_data) - 2, -1, -1):
            splitted_line = deck_data[i].split(" ")

            # easy case : crates for all stacks
            if len(splitted_line) != 9:
                splitted_line = reformat_splitted_string(deck_data[i])
            
            for s in range(9):
                if splitted_line[s] and not splitted_line[s].isspace():
                    self.stacks[s].put(splitted_line[s][1])

        # ----------------------------
        #  Stacks initialisation done 
        # ----------------------------

        for line in move_data:
            splitted_line = line.split(" ")
            self.moving_instr.append(MovingInstr(int(splitted_line[1]), int(splitted_line[3]), int(splitted_line[5])))

    def run(self, put_order="regular"):
        """
            Apply the moving instructions in the MovingInstr list
        """
        for i, instr in enumerate(self.moving_instr):
            if put_order == "regular":
                # Take the crates from the origin stack and put them on the destination stack, LIFO style
                for _ in range(instr.quantity):
                    self.stacks[instr.destination - 1].put(self.stacks[instr.origin - 1].get())

            elif put_order == "same":
                temp_stack = queue.LifoQueue()
                # Take the crates from the origin stack and put them on the temp LIFO stack
                for _ in range(instr.quantity):
                    temp_stack.put(self.stacks[instr.origin - 1].get())

                # Put them back on the destination stack, in the same order as they were in the origin stack
                for _ in range(instr.quantity):
                    self.stacks[instr.destination - 1].put(temp_stack.get())


    def get_top_crates(self):
        """
            Returns a string composed of the concatenated top crates names
        """
        crates_str = ""

        for stack in self.stacks:
            crates_str += stack.queue[-1]

        return crates_str

    def print_stacks(self):
        """
            Prints the stacks (horizontally ¯\_(ツ)_/¯)
        """
        for stack in self.stacks:
            print(f"{stack.queue}")


def reformat_splitted_string(splitted_str):
    """
        Correctly formats a string when there are some empty spots on one or more stacks
    """
    new_splitted_line = []
    offset = 0

    for i in range(9):
        new_splitted_line.append(splitted_str[offset + i * ASCII_COL_WIDTH:offset + (i + 1) * ASCII_COL_WIDTH])
        offset += 1

    return new_splitted_line


def load_and_format_data():
    """
        Loads the data in two different lists: one for the deck data, one for the moving instructions 
    """
    with open("data.txt", "r") as input_file:
        contents = input_file.read()

        is_moving_data = False

        splitted_input = contents.split("\n")
        
        dock_data = []
        line_idx = 0

        while True:
            # if we are at the moving instruction, go to the next loop
            if (splitted_input[line_idx].startswith("move")):
                is_moving_data = True
                break

            # Skip empty lines
            if splitted_input[line_idx]:
                dock_data.append(splitted_input[line_idx])
            line_idx += 1

        move_data = splitted_input[line_idx:]

    return dock_data, move_data

def main():
    dock_data, move_data = load_and_format_data()
    dock = Dock(dock_data, move_data)
    dock.run(put_order="regular")
    print(f"Final top crates (regular order): {dock.get_top_crates()}")

    dock_same = Dock(dock_data, move_data)
    dock_same.run(put_order="same")
    print(f"Final top crates (same order): {dock_same.get_top_crates()}")


if __name__ == "__main__":
    main()