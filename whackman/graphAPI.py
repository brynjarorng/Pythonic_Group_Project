class GraphAPI:
    def __init__(self):
        self.g = {}
        
    def add(self, point, connected=[]):
        # add point as a node if not in graph
        if point not in self.g:
            self.g[point] = set(connected)
        
        # add this connection to all other nodes in the graph, create them if they do not exist
        for node in connected:
            if node not in self.g:
                self.g[node] = set([point])
            else:
                tmp = self.g[node]
                tmp.add(point)
                self.g[node] = tmp
        
    def remove(self, point):
        # if node is not connected to anything remove it, else remove it from all other nodes
        if len(self.g[point]) == 0:
            del self.g[point]
        else:
            for node in self.g[point]:
                tmp = self.g[node]
                tmp.remove(point)
                self.g[node] = tmp
        del self.g[point]

    def BFS(self, start, end, graph):
        queue = []
        visited = set()
        queue.insert(0, graph.g[start])
        visited.add(start)
        retList = []
        
        # loop through all items in the graph using BFS(first check all components in the current node)
        # then go to the next component. when a path is found return the queue.
        while len(queue) > 0:
            curr = queue.pop()
            for node in list(curr):
                if node not in visited and node in graph.g:
                    queue.insert(0, graph.g[node])
                    visited.add(node)
                    retList.append(node)
                    if node == end:
                        return retList[::-1]


    def anyPath(self, start, end, graph):
        path = graph.BFS(start, end, graph)[::-1]
        #for n, i in path:


# BROKEN 
def recursive(end, queue, visited, graph):
    #print(queue)
    # get list of items to check
    curr = list(queue.pop())
        # if item is found end recursion and pop back
    if i in curr:
        return i
    for i in curr:
        queue.insert(0, graph.g[i])
    return  recursive(end, queue, visited, graph)


# find shortest path

v = GraphAPI()
v.add((1,1))
v.add((1,2), [(1,1), (2,1), (3,1), (4,1)])
v.add((1,3), [(1,2), (2,1)])
v.add((1,4), [(1,3), (3,1)])
print(v.anyPath((1,1), (1,4), v))

