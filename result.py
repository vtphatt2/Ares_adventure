class Result:
    def __init__(self, search_algo_name = "", steps = 0, weight = 0, node = 0, time = 0.00, memory = 0.00, sequence_of_actions = ""):
        self.search_algo_name = search_algo_name        # for example : BFS
        self.steps = steps                              # for example : 16
        self.weight = weight                            # for example : 695
        self.node = node                                # for example : 4321
        self.time = time                                # unit : ms, for example : 58.12
        self.memory = memory                            # unit : MB, for example : 12.56
        self.sequence_of_actions = sequence_of_actions  # for example : uLulDrrRRRRRRurD

    def save(self, filepath = "", mode = "a"):
        """
        Save the result to a file as format:

        BFS
        Steps: 16, Weight: 695, Node: 4321, Time (ms): 58.12, Memory (MB): 12.56
        uLulDrrRRRRRRurD
        """

        with open(filepath, mode) as f:
            f.write(self.search_algo_name + "\n")
            f.write(f"Steps: {self.steps}, Weight: {self.weight}, Node: {self.node}, Time (ms): {self.time}, Memory (MB): {self.memory}\n")
            f.write(self.sequence_of_actions + "\n")

