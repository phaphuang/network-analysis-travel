def dfs_paths(graph, start, goal):
    wstep, forstep = 0,0
    stack = [(start, [start])]
    while stack:
        wstep+=1
        print("{}:{} before (vertex, path) = stack.pop():{}".format(wstep, forstep, stack))
        (vertex, path) = stack.pop()
        print("{}:{} after (vertex, path) = stack.pop(): {}".format(wstep, forstep, stack))
        forstep=0
        for next in graph[vertex] - set(path):
            forstep+=1
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))
                print("{}:{} after stack.append((next, path + [next])):{}".format(wstep, forstep, stack))

graph = {'A': set(['B','C','D','E']),
         'B': set(['A','C','D','E']),
         'C': set(['A','B','D','E']),
         'D': set(['A','B','C','E']),
         'E': set(['A','B','C','E'])}

list(dfs_paths(graph=graph, start='A', goal='A'))
