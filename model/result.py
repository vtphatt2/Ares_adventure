import os

class Result:
    def __init__(self, search_algo_name = "", steps = 0, cost = 0, node = 0, time = 0.00, memory = 0.00, sequence_of_actions = ""):
        self.search_algo_name = search_algo_name        # for example : BFS
        self.steps = steps                              # for example : 16
        self.cost = cost                            # for example : 695
        self.node = node                                # for example : 4321
        self.time = time                                # unit : ms, for example : 58.12
        self.memory = memory                            # unit : MB, for example : 12.56
        self.sequence_of_actions = sequence_of_actions  # for example : uLulDrrRRRRRRurD
        self.cost_steps = []                          # for example : [0, 3, 10, 15, 30, 32]

    def save(self, filepath="", mode="a"):
        """
        Save the result to a file in the following format:

        BFS
        Steps: 16, Cost: 695, Node: 4321, Time (ms): 58.12, Memory (MB): 12.56
        uLulDrrRRRRRRurD
        """
        # Ensure the directory exists
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # If the file exists, read its content and remove existing entries for the current algorithm
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                lines = f.readlines()

            # Process the file in chunks of 3 lines (name, details, sequence)
            entries = [lines[i:i+3] for i in range(0, len(lines), 3)]
            
            # Filter out entries where the first line matches the current algorithm name
            filtered_entries = [entry for entry in entries if entry[0].strip() != self.search_algo_name]

            # Write back the filtered entries to the file
            with open(filepath, 'w') as f:
                for entry in filtered_entries:
                    f.writelines(entry)

        # Append the new result
        with open(filepath, 'a') as f:
            f.write(self.search_algo_name + "\n")
            f.write(f"Steps: {self.steps}, Cost: {self.cost}, Node: {self.node}, Time (ms): {self.time}, Memory (MB): {self.memory}\n")
            f.write(self.sequence_of_actions + "\n")
        

    # all getters and setters
    def get_search_algo_name(self):
        return self.search_algo_name
    
    def set_search_algo_name(self, search_algo_name):
        self.search_algo_name = search_algo_name    
    
    def get_steps(self):
        return self.steps
    
    def set_steps(self, steps):
        self.steps = steps

    def get_total_cost(self):
        return self.cost
    
    def set_total_cost(self, cost):
        self.cost = cost
    
    def get_cost_steps(self):
        return self.cost_steps
    
    def set_cost_steps(self, cost_steps):
        self.cost_steps = cost_steps
    
    def get_node(self):
        return self.node
    
    def set_node(self, node):
        self.node = node

    def get_time(self):
        return self.time
    
    def set_time(self, time):
        self.time = time

    def get_memory(self):
        return self.memory
    
    def set_memory(self, memory):
        self.memory = memory

    def get_sequence_of_actions(self):
        return self.sequence_of_actions
    
    def set_sequence_of_actions(self, sequence_of_actions):
        self.sequence_of_actions = sequence_of_actions
