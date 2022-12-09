from enum import Enum
from dataclasses import dataclass, field
from typing import List, Type
from operator import itemgetter


TOTAL_AVAILABLE_SPACE = 70000000
REQUIRED_SPACE        = 30000000


class LineType(Enum):
    COMMAND = 0
    DIR = 1

class CommandType(Enum):
    NOT_A_COMMAND = 0
    CD = 1
    LS = 2

@dataclass
class FileNode:
    """ Dataclass for a filenode (either a file or a folder) """
    name: str
    size: int = 0
    parent = None

@dataclass
class File(FileNode):
    """ Dataclass for a file (name and size) """
    size = 0

@dataclass
class Folder(FileNode):
    """ Dataclass for a folder (name, size and content) """
    content: List = field(default_factory=list) 
    size = 0

    def print_content(self) -> None:
        """ Prints the content of the folder (files and directories)"""
        for filenode in self.content:
            print(filenode.name)


class Hierarchy:
    """ Class that represents the hierarchy of the filesystem with a tree representation """
    def __init__(self):
        self.tree = [Folder(name="/")]
        self.current_root = self.tree[0]

    def add_to_folder(self, to_add: Type[FileNode]) -> None:
        """ Adds a file or a folder to the current current root (different from the tree root) """
        to_add.parent = self.current_root
        self.current_root.content.append(to_add)

    def find_folder_from_current(self, folder_name: str) -> Folder:
        """ Finds and returns a folder from a given name in the current root """
        return self.find_folder(folder_name, self.current_root)

    def find_folder(self, folder_name: str, current_folder: Folder = None) -> Folder:
        """ Finds and returns a folder in a given folder """
        
        for filenode in current_folder.content:
            if isinstance(filenode, Folder):
                if filenode.name == folder_name:
                    return filenode

    def compute_all_sizes(self):
        """ Call the recursive method that computes the sizes of all folders with the right parameters """
        self.recursive_size(self.tree[0], 0)

    def recursive_size(self, current_folder: Folder, size: int) -> int:
        """ Computes the sizes for everything in the hierarchy (recursive) """
        
        new_size = 0

        for filenode in current_folder.content:
            if isinstance(filenode, Folder):
                self.recursive_size(filenode, new_size)

            new_size += filenode.size

        current_folder.size = new_size
        
        return new_size

    def get_sum_size_above_threshold(self, threshold: int = 100000) -> int:
        """ Computes the sum of all the folders in the tree that have a size equal or above a given threshold """
        queue = [self.tree[0]]

        sum_folders = 0

        while queue:

            current_filenode = queue.pop()

            
            if isinstance(current_filenode, Folder):
                if current_filenode.size < threshold:
                    sum_folders += current_filenode.size

                for sub in current_filenode.content:
                    queue.append(sub)

        return sum_folders

    def find_smallest_to_delete(self, total_available_space: int = TOTAL_AVAILABLE_SPACE, required_space: int = REQUIRED_SPACE):
        """ Finds the smallest directory to delete in order to free enough space """
        
        unused_space = total_available_space - self.tree[0].size
        min_space_to_free = required_space - unused_space 

        queue = [self.tree[0]]

        folders_and_size = {}

        while queue:
            current_filenode = queue.pop()
            
            if isinstance(current_filenode, Folder):
                if current_filenode.size >= min_space_to_free:
                    folders_and_size[current_filenode.name] = current_filenode.size

                for sub in current_filenode.content:
                    queue.append(sub)

        return min(folders_and_size.items(), key=itemgetter(1))

    def print(self) -> None:
        """ Ahahah nope """
        pass

    
class Instr:
    """ Class that represents an instruction (= a string)"""
    def __init__(self, str):
        self.line = str
        self.splitted = str.split(" ")

    def is_command(self) -> bool:
        """ Checks if the instruction is a command or not """
        return self.splitted[0] == "$"

    def get_command_type(self) -> CommandType:
        """ Returns the type of the command """
        if not self.is_command:
            return CommandType.NOT_A_COMMAND

        command = self.splitted[1]
        if command == "cd":
            return CommandType.CD

        elif command == "ls":
            return CommandType.LS

    def is_dir(self) -> bool:
        """ Returns a boolean indicating if the instruction contains a directory or not """
        if self.is_command():
            return False

        return self.splitted[0] == "dir"

    def get_size(self) -> int:
        """ Returns the size of the filenode (0 if it's not a filenode) """
        if not self.is_command():
            return self.splitted[0]

        return 0

    def get_name(self) -> str:
        """ Returns the name of a file or a directory """
        if self.is_command():
            return self.splitted[2]

        return self.splitted[1]

    def print(self) -> None:
        """ ¯\_(ツ)_/¯ """
        print(self.line)


class Parser:
    """ Class that contains a list of instructions, and parses them as they come """
    def __init__(self, instr_lst=None):
        self.instr_lst = instr_lst
        self.line_idx = -1
        self.current_instr = None

        if instr_lst:
            self.load_instr(self.instr_lst)


    def load_instr(self, all_instr: str) -> None:
        """ Loads the set of instruction (from big string to list of individual instructions) """
        self.instr_lst = all_instr.split("\n")

    def new_line(self) -> bool:
        """ Checks if there are still instructions to process, and if there are, adds the next one to the current_instr attribute """
        self.line_idx += 1

        if self.line_idx == len(self.instr_lst):
            return False

        self.current_instr = Instr(self.instr_lst[self.line_idx])

        return True

    def read_instrs(self, hierarchy: Hierarchy) -> None:
        """ Reads the instructions, parses them and extends the Hierarchy """
        while self.new_line():
            if self.current_instr.is_command():
                if self.current_instr.get_command_type() == CommandType.LS:
                    continue

                elif self.current_instr.get_command_type() == CommandType.CD:
                    if self.current_instr.get_name() == "/":
                        hierarchy.current_root = hierarchy.tree[0]

                    elif self.current_instr.get_name() == "..":
                        hierarchy.current_root = hierarchy.current_root.parent

                    else:
                        hierarchy.current_root = hierarchy.find_folder_from_current(self.current_instr.get_name())
                        

            else:
                if self.current_instr.is_dir():
                    hierarchy.add_to_folder(Folder(self.current_instr.get_name()))

                else:
                    hierarchy.add_to_folder(File(name=self.current_instr.get_name(), size=int(self.current_instr.get_size())))




def load_and_format_data():
    """ Loads the data in one big string """
    with open("data.txt", "r") as input_file:
        content = input_file.read()

    return content

def main():
    data = load_and_format_data()
    parser = Parser(data)
    hierarchy = Hierarchy()
    parser.read_instrs(hierarchy)

    hierarchy.compute_all_sizes()
    print(f"Sum of all directories with a size inferior to 10000: {hierarchy.get_sum_size_above_threshold()}")
    
    folder_to_delete = hierarchy.find_smallest_to_delete()
    print(f"Smallest directory size to delete to free enough space: {folder_to_delete[0]} = {folder_to_delete[1]}")

if __name__ == "__main__":
    main()