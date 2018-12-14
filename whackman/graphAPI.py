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

    
    
    def shortest(self, start, end, path=[]):
        return find_shortest_path(self.g, start, end, path)

# code from https://www.python.org/doc/essays/graphs/, modified bu me to work with python 3
def find_shortest_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not start in graph:
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

'''
# find shortest path
v = Graph()
v.add((1,1))
v.add((1,2), [(1,1)])
print(v.g)
print(v.shortest((1,1),(1,2)))
v.remove((1,1))
print(v.g)
'''
