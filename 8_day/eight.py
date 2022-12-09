from typing import List
from functools import reduce

class TreeMap:
    """ Class that stores the initial tree map, and a visited trees one """
    def __init__(self, initial_map) -> None:
        self.initial_map = initial_map
        self.already_visible = [[0 for x in range(len(initial_map[y]))] for y in range(len(initial_map))]

    def rotate_list(self, lst: List) -> List:
        """ Rotates a 2D list clockwise """
        return [list(reversed(col)) for col in zip(*lst)]

    def rotate_maps(self):
        """ Rotates both the maps """
        self.initial_map = self.rotate_list(self.initial_map)
        self.already_visible = self.rotate_list(self.already_visible)

    def check_line(self, line: List) -> List:
        """ Checks the number of visible trees on a line """
        visible = [1 for i in range(len(line))]

        # For each tree in a line
        for i, tree in enumerate(line):
            for j in range(i):
                # If there's a higher tree before the current one, not visible
                if line[j] >= tree:
                    visible[i] = 0
                    break

        return visible



    def visible_trees(self) -> int:
        """ Checks the true number of visible trees (that is, any tree that is visible AND that has not been counted yet) """
        sum_of_visible_trees = 0
        # For each line
        for i, line in enumerate(self.initial_map):
            visible_trees = self.check_line(line)
            
            for j, vis in enumerate(visible_trees):
                if not self.already_visible[i][j] and vis:
                    self.already_visible[i][j] = 1
                    sum_of_visible_trees += 1

        return sum_of_visible_trees

    def compute_all_visible_trees(self) -> int:
        """ Computes the total number of visible trees """
        total_sum = 0

        for i in range(4):
            total_sum += self.visible_trees()
            self.rotate_maps()

        return total_sum

    def compute_scenic_score(self, x: int, y: int) -> int:
        """ Computes the scenic score of a tree """
        # Compute right
        score = 0
        
        line = self.initial_map[y]

        tree_height = line[x]

        scenic = []

        # Compute to the right
        if x < len(line) -1:
            for k in range(x + 1, len(line)):
                if line[k] >= tree_height:
                    scenic.append(abs(k - x))
                    break

            else:
                scenic.append(abs(len(line) - x - 1))
        
        # Compute to the left
        if x > 0:
            for k in range(x - 1, -1, -1):
                if line[k] >= tree_height:
                    scenic.append(abs(k - x))
                    break

            else:
                scenic.append(abs(x))

        column = [self.initial_map[z][x] for z in range(len(self.initial_map))]

        # Compute down
        if y < len(column) - 1:
            for k in range(y + 1, len(column)):
                if column[k] >= tree_height:
                    scenic.append(abs(k - y))
                    break

            else:
                scenic.append(abs(len(column) - y - 1))

        # Compute up
        if y > 0:
            for k in range(y - 1, -1, -1):
                if column[k] >= tree_height:
                    scenic.append(abs(k - y))
                    break
            
            else:
                scenic.append(abs(y))
        
        return reduce(lambda x, y: x*y, scenic)

    def compute_highest_scenic_score(self) -> int:
        """ Computes the highest scenic score for all the trees in the map (excluding trees on the edge) """
        highest_score = 0

        # avoid the trees on the edges
        for y in range(1, len(self.initial_map) - 1):
            for x in range(1, len(self.initial_map[y]) - 1):
                new_score = self.compute_scenic_score(x, y)

                if new_score > highest_score:
                    highest_score = new_score

        return highest_score
    
    def pretty_print(self):
        """ Prints the matrix """
        for i in range(len(self.initial_map)):
            for j in range(len(self.initial_map[i])):
                print(self.initial_map[i][j], end=" ")
            print("")


def test_rotation(tree_map: TreeMap) -> None:
    """ Testing the matrix rotation """
    tree_map.pretty_print()
    print("\n\n\n")

    for i in range(3):
        tree_map.rotate_maps()
        tree_map.pretty_print()
        print("\n\n\n")

def load_and_format_data():
    """ Loads the data in one big string """
    data = []

    with open("data.txt", "r") as input_file:
        content = input_file.read()

        for line in content.split("\n"):
            data.append([int(x) for x in list(line)])
        
    return data

def main():
    data = load_and_format_data()
    tree_map = TreeMap(data)
    print(f"Number of all visible trees: {tree_map.compute_all_visible_trees()}")
    print(f"Highest scenic score is: {tree_map.compute_highest_scenic_score()}")

if __name__ == "__main__":
    main()