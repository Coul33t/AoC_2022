def load_and_format_data():
    """
        Loads the data in two different lists: one for the deck data, one for the moving instructions 
    """
    with open("data.txt", "r") as input_file:
        contents = input_file.read()

    return contents

def main():
    data = load_and_format_data()

if __name__ == "__main__":
    main()