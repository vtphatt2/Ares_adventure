from result import Result

class UCS:
    def __init__(self, input_file = ""):
        self.input_file = input_file
        self.result = Result(search_algo_name = "UCS")

    def getResult(self):
        return self.result
    
    # continue with the implementation of the UCS algorithm
    # ...