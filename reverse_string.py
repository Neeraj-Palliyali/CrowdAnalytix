def reverse_string(input_string:str):
    split = input_string.split('-')
    return '-'.join(split[::-1])
    
if __name__ == "__main__":
    try:
        T = int(input("Enter the number of test cases:"))
        for test in range(T):
            try:
                input_string = input("Enter the input string:")
                print(reverse_string(input_string))
            except Exception :
                print("The input seems to be wrong for a string")
    except Exception:
        print("The input should be an integer")