from bfs import BFS
from dfs import DFS
from ucs import UCS
from a_star import A_star

input_file = "input-01.txt"
output_file = "output-01.txt"

# logic and gui
# ...

bfs_result = BFS(input_file).getResult()
dfs_result = DFS(input_file).getResult()
ucs_result = UCS(input_file).getResult()
a_star_result = A_star(input_file).getResult()

# output
bfs_result.save(output_file)
dfs_result.save(output_file)
ucs_result.save(output_file)
a_star_result.save(output_file)