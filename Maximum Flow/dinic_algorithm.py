def find_levels(graph):
    levels = [1] + [0 for _ in graph[1:]]
    queue = [0]

    while queue:
        vertex = queue.pop(0)
        for next_vertex, capacity in enumerate(graph[vertex]):
            if levels[next_vertex] == 0 and capacity > 0:
                queue.append(next_vertex)
                levels[next_vertex] = levels[vertex] + 1

    return levels


def bfs_with_levels(graph, levels):
    queue = [0]
    traceback = [None for _ in graph]

    while queue:
        vertex = queue.pop(0)
        for next_vertex, capacity in enumerate(graph[vertex]):
            if levels[next_vertex] > levels[vertex] and capacity > 0:
                queue.append(next_vertex)
                traceback[next_vertex] = vertex

    current_vertex = len(graph) - 1
    path = []

    while current_vertex is not None:
        path.insert(0, current_vertex)
        current_vertex = traceback[current_vertex]

    return path or None


def find_maxflow_graph(graph):
    residual_graph = graph.copy()
    flow_graph = [[0 for _ in graph] for _ in graph]

    while True:
        levels = find_levels(residual_graph)
        if levels[-1] == 0:
            break

        path = bfs_with_levels(residual_graph, levels)
        if path is None:
            continue

        min_capacity = min([
            residual_graph[current_vertex][path[i + 1]] for i, current_vertex in enumerate(path[:-1])
        ])
        for i, current_vertex in enumerate(path[:-1]):
            residual_graph[current_vertex][path[i + 1]] -= min_capacity
            flow_graph[current_vertex][path[i + 1]] += min_capacity

    return flow_graph


if __name__ == '__main__':
    queue = []
    test_graph = [[000, 150, 100,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                  [150,   0,   0, 200,   0,   0,   0,   0,   0,   0,   0,   0],
                  [100,   0,   0,   0, 180, 170,   0,   0,   0,   0,   0,   0],
                  [000, 200,   0,   0, 180,   0, 200,   0,   0,   0,   0,   0],
                  [000,   0, 180, 180,   0, 160,   0,   0,   0,   0,   0,   0],
                  [000,   0, 170,   0, 160,   0, 250, 170, 200,   0,   0,   0],
                  [000,   0,   0, 200,   0,   0,   0,   0,   0, 200,   0,   0],
                  [000,   0,   0,   0,   0, 170,   0,   0, 240, 240,   0,   0],
                  [000,   0,   0,   0,   0, 200,   0, 240,   0,   0,   0,   0],
                  [000,   0,   0,   0,   0,   0, 200, 240,   0,   0, 200,   0],
                  [000,   0,   0,   0,   0,   0,   0,   0,   0, 200,   0, 250],
                  [000,   0,   0,   0,   0,   0,   0,   0,   0,   0, 250,   0]]

    maxflow = find_maxflow_graph(test_graph)
    print('done')
    print('[', end='')
    for i in maxflow[:-1]:
        print(i, end=',\n')
    print(maxflow[-1], end=']\n')
