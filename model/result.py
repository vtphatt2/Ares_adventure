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

    def save(self, filepath="", duplicate=False):
        """
        Save the result to a file in the following format:

        BFS
        Steps: 16, Cost: 695, Node: 4321, Time (ms): 58.12, Memory (MB): 12.56
        uLulDrrRRRRRRurD

        Parameters:
        - filepath (str): The path to the output file.
        - duplicate (bool): If False, ensures that each algorithm appears only once by replacing existing entries.
                            If True, allows multiple entries for the same algorithm.
        """
        # Ensure the directory exists
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Initialize a list to hold all entries except the current algorithm's (if duplicate=False)
        filtered_lines = []

        # If the file exists and duplicate is False, filter out existing entries for the current algorithm
        if os.path.exists(filepath) and not duplicate:
            with open(filepath, 'r') as f:
                lines = f.readlines()

            # Process the file in chunks of 3 lines (name, details, sequence)
            entries = [lines[i:i+3] for i in range(0, len(lines), 3)]
            
            # Debugging: Print number of entries before filtering
            print(f"Total entries before filtering: {len(entries)}")

            # Filter out entries where the first line matches the current algorithm name
            filtered_entries = [entry for entry in entries if entry[0].strip() != self.search_algo_name]
            
            # Debugging: Print number of entries after filtering
            print(f"Total entries after filtering: {len(filtered_entries)}")

            # Flatten the list of filtered entries back into a single list of lines
            filtered_lines = [line for entry in filtered_entries for line in entry]

            # Write the filtered content back to the file
            with open(filepath, 'w') as f:
                f.writelines(filtered_lines)

        # Append the new result
        with open(filepath, 'a') as f:
            f.write(self.search_algo_name + "\n")
            f.write(f"Steps: {self.steps}, Cost: {self.cost}, Node: {self.node}, Time (ms): {self.time}, Memory (MB): {self.memory}\n")
            f.write(self.sequence_of_actions + "\n")

        # Debugging: Confirm save operation
        action = "Appended" if duplicate else "Saved"
        print(f"{action} entry for algorithm: {self.search_algo_name}")
        

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
