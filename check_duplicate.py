import argparse

class user_defined(Exception):
    # Custom exception class
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return "Duplicate found at index "+str(self.value)

class check_duplicate:
    # Class to check if duplicate exists
    N = 0
    input_array = []
    def __init__(self, args) -> None:
        # user input
        self.N = args.N
        self.input_array = args.input_array

    # function to check if duplicate exists
    def check_duplicate_value(self)-> bool:
        visisted = set()
        for i in range(self.N):
            if self.input_array[i] in visisted:
                raise user_defined(i)
            visisted.add(self.input_array[i])    
        return True
    
def main(args):
    while True:
        if args.N == len(args.input_array):
            # parsing args
            ob = check_duplicate(args)
            while True:
                # check if duplicate values exists
                try:
                    ob.check_duplicate_value()
                    print(sorted(ob.input_array, reverse=True))
                    break
                except user_defined as e:
                    ob.input_array.pop(e.value)
                    ob.N-=1
                    print(e)
            break
        else:
            # if arg parse fails
            print(f"Number of element not equal to the provided value for N = {args.N}")
            print("Input the values again:")
            try:
                args.input_array = list(map(int, input().split()))
            except Exception:
                continue
        
if __name__ == "__main__":
    # input format " python .\check_duplicate.py -N 6 -input_array 33 4 2 3 44 4"
    parser = argparse.ArgumentParser()
    parser.add_argument("-N", help = "Enter the number of elements in list:", type = int)
    parser.add_argument("-input_array",nargs="+", help = "Space seperated int values based on N", type = int)
    args = parser.parse_args()
    main(args)