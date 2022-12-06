def load_and_format_data():
    with open("data.txt", "r") as input_file:
        contents = input_file.read()
        data = [[[int(z) for z in y.split("-")] for y in x.split(",")] for x in contents.split("\n")]

    return data


def fully_overlap(pair):
    return (min(pair[0]) <= min(pair[1]) and max(pair[0]) >= max(pair[1])) \
        or (min(pair[1]) <= min(pair[0]) and max(pair[1]) >= max(pair[0]))

def partially_overlap(pair):
    if not fully_overlap(pair) \
       and min(pair[0]) < min(pair[1]) and max(pair[0]) < min(pair[1]) \
        or min(pair[1]) < min(pair[0]) and max(pair[1]) < min(pair[0]):
            return False

    return True


def get_overlapping(data, type="fully"):
    nb_overlap = 0

    for pair in data:
        if type == "fully":
            if fully_overlap(pair):
                nb_overlap += 1

        elif type == "partial":
            if partially_overlap(pair):
                nb_overlap += 1

    return nb_overlap

def main():
    data = load_and_format_data()
    print(f"Number of fully overlapping ranges: {get_overlapping(data)}")
    print(f"Number of partially overlapping ranges: {get_overlapping(data, 'partial')}")


if __name__ == "__main__":
    main()