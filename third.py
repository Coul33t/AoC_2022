def load_and_format_data():
    with open("third_data.txt", "r") as input_file:
        contents = input_file.read()
        data = [[x[:int(len(x) / 2)], x[int(len(x) / 2):]] for x in contents.split("\n")]
        
    return data


def get_misplaced(comp):
    """ Compute the interesction of the two sets """
    return set(comp[0]).intersection(set(comp[1])).pop()

def sum_priorities(data):
    score = 0
    for comp in data:
        ret = get_misplaced(comp)
        breakpoint()

def main():
    data = load_and_format_data()
    sum_priorities(data)


if __name__ == "__main__":
    main()