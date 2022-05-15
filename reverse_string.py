# Question 2
def reverse_string(input_string:str)->str:
    # splitting based on '-'
    split = input_string.split('-')
    if len(split)==1:
        print("There is no '-' seperated words!!!")
    # reverse iterated and joined
    return '-'.join(split[::-1])
    
if __name__ == "__main__":
    try:
        T = int(input("Enter the number of test cases:"))
        for test in range(T):
            try:
                input_string = input("Enter the input string:")
                print(reverse_string(input_string))
            except Exception as e:
                print("The input seems to be wrong for a string")
    except Exception:
        print("The input should be an integer")