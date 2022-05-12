import argparse

class user_defined(Exception):

    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return "Duplicate found at index "+str(self.value)

class check_duplicate:
    N = 0
    input_array = []
    def __init__(self, args) -> None:
        # user input
        self.N = args.N
        self.input_array = args.input_array


    def check_duplicate_value(self)-> bool:
        visisted = set()
        for i in range(len(self.input_array)):
            if self.input_array[i] in visisted:
                raise user_defined(i)
            visisted.add(self.input_array[i])    
        
        return True

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-input_array",nargs="+", help = "Space seperated int values based on N", type = int)
    parser.add_argument("-N", help = "Enter the number of elements in list:", type = int)
    args = parser.parse_args()
    if args.N == len(args.input_array):
        while True:
            ob = check_duplicate(args)
            try:
                ob.check_duplicate_value()
                val = ob.input_array
                print(sorted(ob.input_array, reverse=True))
                break
            except user_defined as e:
                ob.input_array.pop(e.value)
                print (e)
    else:
        print(f"Number of element not equal to the provided value for N = {args.N}")
        
