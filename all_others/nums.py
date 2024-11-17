def read_graph(file_name):
    with open(file_name, 'r') as f:
        n = int(f.readline().strip())
        graph = [[] for _ in range(n)]
        for i in range(n):
            line = list(map(int, f.readline().strip().split()))
            for target in line:
                if target == -2:
                    break
                graph[i].append(target)
    return n, graph


def dfs(graph, node, visited):
    visited[node] = True
    for neighbor in graph[node]:
        if not visited[neighbor]:
            dfs(graph, neighbor, visited)


def find_inevitable_points(n, graph):
    visited_from_start = [False] * n
    dfs(graph, 0, visited_from_start)

    visited_from_finish = [False] * n
    reverse_graph = [[] for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            reverse_graph[v].append(u)

    dfs(reverse_graph, n - 1, visited_from_finish)

    inevitable_points = []
    for i in range(1, n - 1):  # Исключаем старт (0) и финиш (N-1)
        if visited_from_start[i] and visited_from_finish[i]:
            inevitable_points.append(i)

    return inevitable_points


def find_split_points(n, graph):
    split_points = []

    for s in range(1, n - 1):  # Проверяем все точки кроме стартовой (0) и финишной (N-1)
        # Создаем граф без вершины s
        subgraph = [[] for _ in range(n)]

        for u in range(n):
            if u == s:
                continue
            for v in graph[u]:
                if v == s:
                    continue
                subgraph[u].append(v)

        # Проверяем достижимость от старта до финиша
        visited_from_start = [False] * n
        dfs(subgraph, 0, visited_from_start)

        if not visited_from_start[n - 1]:  # Если финиш недостижим
            split_points.append(s)

    return split_points


def main():
    n, graph = read_graph('input.txt')

    inevitable_points = find_inevitable_points(n, graph)
    split_points = find_split_points(n, graph)

    # Записываем результаты в выходной файл
    with open('output.txt', 'w') as f:
        f.write(f"{len(inevitable_points)}")
        if inevitable_points:
            f.write(" " + " ".join(map(str, sorted(inevitable_points))))
        f.write("n")

        f.write(f"{len(split_points)}")
        if split_points:
            f.write(" " + " ".join(map(str, sorted(split_points))))
        f.write("n")


if __name__ == "__main__":
    main()
