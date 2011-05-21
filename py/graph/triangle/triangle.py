import sys
import heapq

class TriangleGraph(object):
    """
    Problem: Determine the maximum sum of numbers in a path from the
    top of the triangle to the bottom. You have to start at the top
    and move to adjacent numbers on the line below.

    Example triangle (samples/triangle2.txt):

                5*
               / \
              /   \
             9*    6
            / \   / \
           /   \ /   \
          4     6*    8
         / \   / \   / \
        /   \ /   \ /   \
       0     7*    1     5

    Answer to the triangle above is 5+9+6+7 = 27
    """

    def __init__(self, triangle_lines=[]):
        """
        triangle_lines should be a list of space-delimited strings of numbers:
            Example: ["5", "9 6", "4 6 8", "0 7 1 5"] represents the following:
               5
               9 6
               4 6 8
               0 7 1 5
        """
        self.lines = triangle_lines

        self.graph = []
        self.numNodes = 1

        # initialize self.values with root value
        self.values = [int(self.lines[0])]

        self.distances = []
        self.predecessors = []

        self.build_adjacency_lists()

    def build_adjacency_lists(self):
        """
        Generates the adjacency lists from the data.
        """
        for i in xrange(len(self.lines)-1):
            nextline = self.lines[i+1].split()

            # add next line of values to self.values (this is why self.values
            # is initialized with root value above)
            self.values.extend([int(n) for n in nextline])

            for j in xrange(len(nextline[:-1])):
                self.graph.append({self.numNodes: int(nextline[j]),
                                   self.numNodes+1: int(nextline[j+1])})
                self.numNodes += 1

            self.numNodes += 1

        # add last line's adjacency list (which are just empty dicts)
        last = self.lines[-1].split()
        self.graph.extend([{} for i in xrange(len(last))])

    def path(self, s, v):
        """
        Returns the total cost of traveling from s to v.
        """
        if s == v:
            return self.values[s]
        elif self.predecessors[v] == -1:
            return 0
        else:
            return self.path(s, self.predecessors[v]) + self.values[v]

    def relax(self, u, v, w):
        """
        Note: shortest-path relax function checks if d[v] > d[u] + w
        Since I'm trying to find the longest path, I do the opposite.
        """
        if self.distances[v] < self.distances[u] + w:
            self.distances[v] = self.distances[u] + w
            self.predecessors[v] = u

    def weight(self, u, v):
        return self.values[u] + self.values[v]

    def dijkstra(self, s):
        """
        Dijkstra's algorithm finds the single-source shortest-path in a
        weighted directed graph. I want to find the single-source
        longest-path, so rather than initialize distances to infinity,
        they're initialized to -1.
        """
        for i in xrange(self.numNodes):
            self.distances.append(-1)
            self.predecessors.append(-1)
        self.distances[s] = 0

        S = set()
        Q = [i for i in xrange(self.numNodes)]
        heapq.heapify(Q)

        while Q:
            u = heapq.heappop(Q)
            S.add(u)
            for v in self.graph[u].keys():
                w = self.weight(u, v)
                self.relax(u, v, w)

    def longest_path(self):
        total = 0
        for i in xrange(self.numNodes-len(self.lines), self.numNodes):
            # iterate over the last line's numbers from start to end to
            # get valid end points.
            t = self.path(0, i)
            if t > total:
                total = t
        return total

def main():
    if len(sys.argv) < 2:
        print "Usage: %s <triangle_file>" % sys.argv[0]
        return

    try:
        lines = open(sys.argv[1]).read()
    except IOError:
        print "Can't open file '%s'" % sys.argv[1]
        return

    # last element of split is "" if file is properly formatted
    lines = lines.split("\n")[:-1]
    G = TriangleGraph(lines)
    G.dijkstra(0)
    print G.longest_path()

if __name__ == "__main__":
    main()