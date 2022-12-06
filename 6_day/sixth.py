def has_diff_letters(buffer):
    return len(buffer) == len(set(buffer))


def find_marker_index(data, buffer_size=4):
    buffer = []
    for i, l in enumerate(data):
        buffer.append(l)

        if i > buffer_size - 2:
            if has_diff_letters(buffer):
                return i + 1
            else:
                buffer.pop(0)

    return -1

        

def load_and_format_data():
    """
        Loads the data in two different lists: one for the deck data, one for the moving instructions 
    """
    with open("data.txt", "r") as input_file:
        contents = input_file.read()

    return contents

def main():
    data = load_and_format_data()
    print(f"Marker found at {find_marker_index(data)}")
    print(f"State-of-the-art marker found at {find_marker_index(data, buffer_size=14)}")

if __name__ == "__main__":
    main()