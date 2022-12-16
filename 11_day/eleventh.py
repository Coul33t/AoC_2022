from dataclasses import dataclass, field
from enum import Enum
from typing import List
from webbrowser import Opera


class Operator(Enum):
    ADD = 0,
    SUB = 1,
    MUL = 2,
    DIV = 3,
    NONE = 4

def operator_to_string(string):
    if string == "+":
        return Operator.ADD

    elif string == "-":
        return Operator.SUB

    elif string == "*":
        return Operator.MUL

    elif string == "/" or string == "divisible":
        return Operator.DIV

    return Operator.NONE


@dataclass
class Monkey:
    name: str
    starting_items: list = field(default_factory=list)
    values_operator: Operator = Operator.NONE
    old: int = -1
    new: int = -1
    values: list = field(default_factory=list)
    test_operator: Operator = Operator.NONE
    value_test: int = -1
    throw_to: list = field(default_factory=list)

def do_operation(monkey):
    val1 = -2
    val2 = -2

    if monkey.values[0] == "old":
        val1 = monkey.old

    if monkey.values[1] == "old":
        val2 = monkey.old

    if monkey.values_operator == Operator.ADD:
        return val1 + val2

    elif monkey.values_operator == Operator.MUL:
        return val1 * val2

def do_test(monkey):
    if monkey.test_operator == Operator.DIV:
        return monkey.new % monkey.value_test == 0


def going_ape(monkeys):
    for i, monkey in enumerate(monkeys):
        for single_item in monkey.starting_items:
            monkey.old = single_item
            monkey.new = do_operation(monkey)

def load_and_format_data():
    """ Loads the data in a list of Monkeys """
    data = []

    with open("test_data.txt", "r") as input_file:
        content = input_file.read()

        monkey = None

        for line in content.split("\n"):
            if not line:
                continue

            splitted = line.strip().split(" ")

            if splitted[0] == "Monkey":
                if monkey:
                    data.append(monkey)

                monkey = Monkey(name=splitted[1].strip(":"))

            elif splitted[0] == "Starting":
                monkey.starting_items = [int(x) for x in line.split(":")[1].split(",")]
            
            elif splitted[0] == "Operation:":
                operator_splitted = line.split("=")[1].split(" ")
                
                try:
                    monkey.values.append(int(operator_splitted[1]))
                except ValueError:
                    monkey.values.append(operator_splitted[1])


                monkey.values_operator = operator_to_string(operator_splitted[2])

                try:
                    monkey.values.append(int(operator_splitted[3]))
                except ValueError:
                    monkey.values.append(operator_splitted[3])

            elif splitted[0] == "Test:":
                test_splitted = line.strip().split(":")[1].strip().split(" ")

                monkey.test_operator = operator_to_string(test_splitted[0])
                monkey.value_test = int(test_splitted[-1])

            elif splitted[1] == "true:":
                monkey.throw_to.append(int(splitted[-1]))

            elif splitted[1] == "false:":
                monkey.throw_to.append(int(splitted[-1]))
                
        data.append(monkey)

    return data

def main():
    data = load_and_format_data()
    breakpoint()

if __name__ == "__main__":
    main()