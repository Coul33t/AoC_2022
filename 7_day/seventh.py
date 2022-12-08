from enum import Enum
from dataclasses import dataclass, field
from fileinput import fileno
from typing import List, Type

class LineType(Enum):
    COMMAND = 0
    DIR = 1

class CommandType(Enum):
    NOT_A_COMMAND = 0
    CD = 1
    LS = 2

@dataclass
class FileNode: 
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
        for filenode in self.content:
            print(filenode.name)

class Hierarchy:
    def __init__(self):
        self.tree = [Folder(name="/")]
        self.current_root = self.tree[0]

    def add_to_folder(self, to_add: Type[FileNode]) -> None:
        to_add.parent = self.current_root
        self.current_root.content.append(to_add)

    def find_folder_from_current(self, folder_name: str) -> Folder:
        return self.find_folder(folder_name, self.current_root)

    def find_folder(self, folder_name: str, current_folder: Folder = None) -> Folder:
        """ Finds and returns a folder in the current root """
        
        for filenode in current_folder.content:
            if isinstance(filenode, Folder):
                if filenode.name == folder_name:
                    return filenode

    def recursive_size(self, current_folder: Folder, size: int) -> int:
        """ Computes the sizes for everything in the hierarchy (recursive) """
        
        for filenode in current_folder.content:
            if isinstance(filenode, Folder):
                self.recursive_size(filenode, size)

            size += filenode.size

        current_folder.size = size
        return size

    def print(self) -> None:
        pass

    
class Instr:
    def __init__(self, str):
        self.line = str
        self.splitted = str.split(" ")

    def is_command(self) -> bool:
        return self.splitted[0] == "$"

    def get_command_type(self) -> CommandType:
        if not self.is_command:
            return CommandType.NOT_A_COMMAND

        command = self.splitted[1]
        if command == "cd":
            return CommandType.CD

        elif command == "ls":
            return CommandType.LS

    def is_dir(self) -> bool:
        if self.is_command():
            return False

        return self.splitted[0] == "dir"

    def get_size(self) -> int:
        if not self.is_command():
            return self.splitted[0]

        return 0

    def get_name(self) -> str:
        """ Returns the name of a file or a directory """
        if self.is_command():
            return self.splitted[2]

        return self.splitted[1]

    def print(self) -> None:
        print(self.line)


class Parser:
    def __init__(self, instr_lst=None):
        self.instr_lst = instr_lst
        self.line_idx = 0
        self.current_instr = None
        self.hierarchy = Hierarchy()

        if instr_lst:
            self.load_instr(self.instr_lst)


    def load_instr(self, all_instr: str) -> None:
        self.instr_lst = all_instr.split("\n")

    def new_line(self) -> bool:
        self.current_instr = Instr(self.instr_lst[self.line_idx])
        self.line_idx += 1

        if self.line_idx == len(self.instr_lst):
            return False

        return True

    def read_instrs(self) -> None:
        while self.new_line():
            if self.current_instr.is_command():
                if self.current_instr.get_command_type() == CommandType.LS:
                    continue

                elif self.current_instr.get_command_type() == CommandType.CD:
                    if self.current_instr.get_name() == "/":
                        self.hierarchy.current_root = self.hierarchy.tree[0]

                    elif self.current_instr.get_name() == "..":
                        self.hierarchy.current_root = self.hierarchy.current_root.parent

                    else:
                        self.hierarchy.current_root = self.hierarchy.find_folder_from_current(self.current_instr.get_name())
                        

            else:
                if self.current_instr.is_dir():
                    self.hierarchy.add_to_folder(Folder(self.current_instr.get_name()))

                else:
                    self.hierarchy.add_to_folder(File(name=self.current_instr.get_name(), size=int(self.current_instr.get_size())))

                
    def compute_sizes(self) -> int:
        self.hierarchy.recursive_size(self.hierarchy.tree[0], 0)




def load_and_format_data():
    """
        Loads the data in two different lists: one for the deck data, one for the moving instructions 
    """
    with open("data.txt", "r") as input_file:
        content = input_file.read()

    return content

def main():
    data = load_and_format_data()
    parser = Parser(data)
    parser.read_instrs()
    parser.compute_sizes()

if __name__ == "__main__":
    main()