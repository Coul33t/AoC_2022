from dataclasses import dataclass
from enum import Enum
from math import sqrt
from typing import List, Tuple

class Direction(Enum):
    """ Enumeration for the four possible directions """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

# Dictionnary to transform a letter into a Direction (Enum)
DIRECTIONS = {"U": Direction.UP, "R": Direction.RIGHT, "D": Direction.DOWN, "L": Direction.LEFT}
# Dictionnary to transform a Direction (Enum) into a tuple of variables corresponding to the direction
DELTA = {Direction.UP: (0, 1), Direction.RIGHT: (1, 0), Direction.DOWN: (0, -1), Direction.LEFT: (-1, 0)}

@dataclass
class Coordinates:
    """ Dataclass that contains a couple of coordinates (x and y) """
    x: int
    y: int

    def as_tuple(self) -> Tuple:
        return (self.x, self.y)

@dataclass
class Instr:
    """ Dataclass that contains a signel instruction (that is, a direction and the number of step in that direction) """
    dir: Direction
    steps: int

class Walker:
    """ Class that contains the logic for parsing, reading and running the instructions and keeping track of the knots coordinates """
    def __init__(self, instr_lst=None):
        self.visited = set()
        self.instr_lst = []
        self.current_instr = None
        self.instr_idx = -1

        if instr_lst:
            self.load_instructions(instr_lst)


    def load_instructions(self, instr_lst: List) -> None:
        """ Load the instructions in Instr objects into a list """
        for instr in instr_lst:
            self.instr_lst.append(Instr(DIRECTIONS[instr[0]], int(instr[1])))

    def dst(self, first: Coordinates, second: Coordinates) -> float:
        """ Computes the 2D distance between 2 points """
        return sqrt((first.x - second.x)**2 + 
                    (first.y - second.y)**2)

    def move_current(self, current: Coordinates, dx: int, dy: int) -> None:
        """ Moves a knot of the rope (should only be used for the head) """
        current.x += dx
        current.y += dy

    def move_next(self, current: Coordinates, next: Coordinates) -> None:
        """ Moves the knot right after the one that was moved (should be used for all knots except the head) """
        dx = current.x - next.x
        dy = current.y - next.y

        # move to the right
        if dx > 0:
            next.x += 1

        # move to the left
        if dx < 0:
            next.x -= 1

        # move up
        if dy > 0:
            next.y += 1

        # move down
        if dy < 0:
            next.y -= 1

    def next_instr(self) -> bool:
        """ Checks if there are still instructions to process, and if there are, adds the next one to the current_instr attribute """
        self.instr_idx += 1

        if self.instr_idx == len(self.instr_lst):
            return False

        self.current_instr = self.instr_lst[self.instr_idx]

        return True

    def run_simple_rope(self) -> int:
        """ Run the instructions with just a head and a tail (2 knots) and returns the number of tiles visited """
        self.instr_idx = -1
        self.visited.clear()
        
        all_pos = {"head": Coordinates(0, 0), "tail": Coordinates(0, 0)}

        self.visited.add(all_pos["tail"].as_tuple())

        while self.next_instr():
            for n in range(self.current_instr.steps):
                # Move the head
                self.move_current(all_pos["head"], *DELTA[self.current_instr.dir])

                # If the tail is more than one tile away from the head, move it too
                if self.dst(all_pos["head"], all_pos["tail"]) >= 2:
                    self.move_next(all_pos["head"], all_pos["tail"])
                    self.visited.add(all_pos["tail"].as_tuple())

        return len(self.visited)

    def run_multiple_knots_ropes(self) -> int:
        """ Run the instructions with 10 knots (1 head, 8 intermediate knots, 1 tail) and returns the number of tiles visited """
        self.instr_idx = -1
        self.visited.clear()
        
        all_pos = [Coordinates(0, 0) for i in range(10)]
        
        self.visited.add(all_pos[-1].as_tuple())

        while self.next_instr():
            for n in range(self.current_instr.steps):
                # Move the head
                self.move_current(all_pos[0], *DELTA[self.current_instr.dir])

                last_idx = 0
                # For each other knot
                for current_idx in range(1, len(all_pos)):
                    # If the distance to the knot in front of the current one is > 2 (= farther than 1 tile away)
                    if self.dst(all_pos[last_idx], all_pos[current_idx]) >= 2:
                        # Move it closer to the knot in front of it
                        self.move_next(all_pos[last_idx], all_pos[current_idx])

                        # If it's the last node (= the tail), add its current tile to the visited set
                        if (current_idx == len(all_pos) - 1):
                            self.visited.add(all_pos[-1].as_tuple())

                    last_idx += 1

        return len(self.visited)

def load_and_format_data():
    """ Loads the data in one big string """
    data = []

    with open("data.txt", "r") as input_file:
        content = input_file.read()

        for line in content.split("\n"):
            data.append([line.split(" ")[0], line.split(" ")[1]])
        
    return data

def main():
    data = load_and_format_data()
    walker = Walker(data)
    print(f"Number of visited tiles: {walker.run_simple_rope()}")
    print(f"Number of visited tiles by tail: {walker.run_multiple_knots_ropes()}")

if __name__ == "__main__":
    main()