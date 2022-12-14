CORRESPONDING = {"X": "A", "Y": "B", "Z": "C"}

WIN = {"A": "Y", "B": "Z", "C": "X"} 
LOSE = {"A": "Z", "B": "X", "C": "Y"}
DRAW = {"A": "X", "B": "Y", "C": "Z"} 
MUST = {"X": LOSE, "Y": DRAW, "Z": WIN}

def load_and_format_data():
    """ Loads the data into a list of strings """
    with open("data.txt", "r") as input_file:
        contents = input_file.read()
        data = [ x.split(" ") for x in contents.split("\n")]
    
    return data

def compute_single_round_score(couple):
    """ Computes the score for a single round """
    # A is 1 point, B 2 points, C 3 points
    score = ord(couple[1]) - (ord("A")) + 1

    # draw
    if couple[0] == couple[1]:
        score += 3

    # win
    elif ord(couple[1]) - ord(couple[0]) == -2 or ord(couple[1]) - ord(couple[0]) == 1:
        score += 6

    return score

def get_score(data):
    """ Part 1: just follows the guide (data) """
    score = 0

    for couple in data:
        score += compute_single_round_score([couple[0], CORRESPONDING[couple[1]]])

    return score

def get_sneaky_score(data):
    """ Part 2: your letter (second row in the data) tells if you have to win, draw or lose """
    score = 0

    for couple in data:
        use_dict = MUST[couple[1]]
        new_couple = [couple[0], CORRESPONDING[use_dict[couple[0]]]]
        score += compute_single_round_score(new_couple)

    return score


            
def main():
    data = load_and_format_data()
    print(f"Score is {get_score(data)}")
    print(f"Sneaky score is {get_sneaky_score(data)}")


if __name__ == "__main__":
    main()