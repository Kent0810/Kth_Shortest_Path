import numpy as np


class Map:
    def __init__(self, graph):
        self.length = len(graph)
        self.graph = graph
        # create residual graph fill with of, with the size of initial graph
        self.rgraph = []
        # list is a list of 0 with length of the graph
        self.nlist = []
        for _ in range(self.length):
            self.nlist.append(0)
        for _ in graph:
            self.rgraph.append(self.nlist + [])

    def bfs(self, source, sink):
        path = []  # path include the current path we choose
        max_flow = float("inf")  # the return variable
        visited = self.nlist + []  # don't visit one node twice
        visited[source] = 1
        path.append(source)
        current_node = source + 0  # current node we are in
        next_node = 0
        while len(path) != 0 and current_node != sink:  # while not reach sink and there's still path
            # loop all to find next_node until reach the sink, auto-break if in one cycle, there were no next_node
            while next_node < self.length:
                # for next_node in range(self.length):
                # Check if next_node != source, not visited, can go
                if self.graph[current_node][next_node] > 0 and next_node != source and visited[next_node] == 0:
                    # current_node -> next_node, mark next_node as visited, add next_node to the path.
                    current_node = next_node
                    path.append(current_node)
                    visited[current_node] = 1
                    next_node = 0
                else:
                    next_node += 1
                if current_node == sink:  # If reach the sink, out of loop
                    break
            # If there's no next_node, pop the last_node from path and marked it as not visited
            next_node = path.pop() + 1
            visited[next_node - 1] = 0

            if current_node != sink and len(path) != 0:
                current_node = path[-1]
        # Now we have the path and the residual graph, and the left-over graph.
        if current_node == sink:
            path.append(current_node)
            for _ in range(len(path) - 1):
                max_flow = min(max_flow, self.graph[path[_]][path[_ + 1]])
            for _ in range(len(path) - 1):
                self.rgraph[path[_ + 1]][path[_]] += max_flow
                self.graph[path[_]][path[_ + 1]] -= max_flow
                self.graph[path[_ + 1]][path[_]] += max_flow
            print(f"Graph for this step:{self.graph}")
            print(f"Residual graph for this step:{self.rgraph}")
            print(f"Path of this step:{path}")
            print(f"Max flow of this step:{max_flow}")
            return True
        return False

    def maxflow(self, source, sink):
        while self.bfs(source, sink):
            print("OK")
        return self.rgraph


if __name__ == '__main__':
    queue = []
    test_graph = [[0, 16, 13,  0,  0,  0],
                  [0,  0, 10, 12,  0,  0],
                  [0,  4,  0,  0, 14,  0],
                  [0,  0,  9,  0,  0, 20],
                  [0,  0,  0,  7,  0,  4],
                  [0,  0,  0,  0,  0,  0]]
    new_map = Map(test_graph)
    final_rgraph = new_map.maxflow(0, 5)
    print(f"Maximum flow:{sum(final_rgraph[-1])}")
    print("Optimized path:")
    print(np.array(final_rgraph).transpose())

