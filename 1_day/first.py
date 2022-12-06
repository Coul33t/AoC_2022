def load_and_format_data():
    with open("data.txt", "r") as input_file:
        contents = input_file.read()
        data = [[int(y) for y in x.split("\n")] for x in contents.split("\n\n")]
        
    return data

def get_max(data):
    return max([sum(x) for x in data])

def get_three_top_max(data):
    max_three = []

    for vals in data:
        sum_val = sum(vals)
        
        if len(max_three) < 3:
            max_three.append(sum_val)

        else:
            if min(max_three) < sum_val:
                max_three[max_three.index(min(max_three))] = sum_val

    return sum(max_three)


def main():
    data = load_and_format_data()
    print(f"Max sum is {get_max(data)}")
    print(f"Sum of three biggest is {get_three_top_max(data)}")


if __name__ == "__main__":
    main()