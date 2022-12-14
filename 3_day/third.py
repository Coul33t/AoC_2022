def load_and_format_data():
    with open("data.txt", "r") as input_file:
        contents = input_file.read()
        data = [[x[:int(len(x) / 2)], x[int(len(x) / 2):]] for x in contents.split("\n")]
        
    return data

def reformat_data(data):
    new_data = ["".join(x) for x in data]
    new_data = [[new_data[i], new_data[i+1], new_data[i+2]] for i in range(0, len(new_data), 3)]
    return new_data

def get_misplaced(comp):
    """ Compute the interesction of multiple sets """
    global_set = set()
    for single_set in comp:
        if not global_set:
            global_set = set(single_set)
        else:
            global_set = global_set.intersection(set(single_set))

    return global_set.pop()

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
    new_data = reformat_data(data)
    print(f"Summed badges priorities: {sum_priorities(new_data)}")


if __name__ == "__main__":
    main()