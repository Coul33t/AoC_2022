def has_diff_letters(buffer):
    """
        Checks if a string is only made of unique characters by comparing the size of the string vs the size of the string as a set
    """
    return len(buffer) == len(set(buffer))


def find_marker_index(data, buffer_size=4):
    """
        Finds the marker index in a string where a number (buffer_size) of letters are all uniques
    """
    buffer = []

    for i, l in enumerate(data):
        # Add the next character to the buffer
        buffer.append(l)

        # If the buffer is filled
        if i > buffer_size - 2:
            # Check if all characters are different from each other
            if has_diff_letters(buffer):
                return i + 1
            else:
                # removes the last character in the buffer (at idx = 0)
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