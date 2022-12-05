def load_and_format_data():
    with open("third_data.txt", "r") as input_file:
        contents = input_file.read()
        data = [[x[:int(len(x) / 2)], x[int(len(x) / 2):]] for x in contents.split("\n")]
        
    return data


def get_misplaced(comp):
    """ Compute the interesction of the two sets """
    return set(comp[0]).intersection(set(comp[1])).pop()

def get_priority(letter):
    # a to z (1 - 26)
    ret = ord(letter) - ord('a') + 1
    
    if ord(letter) > ord('Z'):
        return ret
    
    # A to Z (27 - 52)
    else:
        return ret + ord('z') - ord('A') + 1
 
def sum_priorities(data):
    score = 0
    for comp in data:
        score += get_priority(get_misplaced(comp))

    return score
        

def main():
    data = load_and_format_data()
    print(f"Summed priorities: {sum_priorities(data)}")


if __name__ == "__main__":
    main()