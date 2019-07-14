# -*- coding: utf-8 -*-
import plotly.io as pio
from helpers import Map, load_map_10, load_map_40, show_map
import math

class MinPQ():
    def __init__(self, f_scores):
        self.n = 0;
        
        # dict(node_id, fscore)
        self.f_scores = f_scores;        
        self.elements = [None]
        
    def score(self, idx):
        return self.f_scores[self.elements[idx]]
        
    def min(self):
        return self.elements[1]
    
    def add(self, node):
        self.elements.append(node)
        self.n += 1        
        self.swim(self.n)
                
    def swim(self, k):
        while k/2 >= 1:
            if self.score(k/2) <= self.score(k):
                return
            self.elements[k/2], self.elements[k] = self.elements[k], self.elements[k/2]
            k = k / 2

    def remove(self):
        self.elements[1], self.elements[self.n] = self.elements[self.n], self.elements[1]
        self.elements[self.n] = None
        self.n -= 1       
        self.sink(1)

    def sink(self, k):
        while 2*k <= self.n:
            i = 2*k
            if i+1 <= self.n and self.score(i+1) < self.score(i):
                i += 1
            if self.score(i) < self.score(k):
                self.elements[k], self.elements[i] = self.elements[i], self.elements[k]
            k = i
            
    def size(self):
        return self.n;
    
class PathPlanner():
    """Construct a PathPlanner Object"""
    def __init__(self, M, start=None, goal=None):
        """ """
        self.map = M
        self.start= start
        self.goal = goal
        self.closedSet = self.create_closedSet() if goal != None and start != None else None
        self.cameFrom = self.create_cameFrom() if goal != None and start != None else None
        self.gScore = self.create_gScore() if goal != None and start != None else None
        self.fScore = self.create_fScore() if goal != None and start != None else None
        self.openSet = self.create_openSet() if goal != None and start != None else None        
        self.path = self.run_search() if self.map and self.start != None and self.goal != None else None
    
    def reconstruct_path(self, current):
        """ Reconstructs path after search """
        total_path = [current]
        while current in self.cameFrom.keys():
            current = self.cameFrom[current]
            total_path.append(current)
        return total_path
    
    def _reset(self):
        """Private method used to reset the closedSet, openSet, cameFrom, gScore, fScore, and path attributes"""
        self.closedSet = None
        self.openSet = None
        self.cameFrom = None
        self.gScore = None
        self.fScore = None
        self.path = self.run_search() if self.map and self.start and self.goal else None

    def run_search(self):
        """ """
        if self.map == None:
            raise(ValueError, "Must create map before running search. Try running PathPlanner.set_map(start_node)")
        if self.goal == None:
            raise(ValueError, "Must create goal node before running search. Try running PathPlanner.set_goal(start_node)")
        if self.start == None:
            raise(ValueError, "Must create start node before running search. Try running PathPlanner.set_start(start_node)")

        self.closedSet = self.closedSet if self.closedSet != None else self.create_closedSet()
        self.openSet = self.openSet if self.openSet != None else  self.create_openSet()
        self.cameFrom = self.cameFrom if self.cameFrom != None else  self.create_cameFrom()
        self.gScore = self.gScore if self.gScore != None else  self.create_gScore()
        self.fScore = self.fScore if self.fScore != None else  self.create_fScore()

        while not self.is_open_empty():
            current = self.get_current_node()

            if current == self.goal:
                self.path = [x for x in reversed(self.reconstruct_path(current))]
                return self.path
            else:
                self.openSet.remove(current)
                self.closedSet.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in self.closedSet:
                    continue    # Ignore the neighbor which is already evaluated.

                if not neighbor in self.openSet:    # Discover a new node
                    self.openSet.add(neighbor)
                
                if self.get_tentative_gScore(current, neighbor) >= self.get_gScore(neighbor):
                    continue        # This is not a better path.

                # This path is the best until now. Record it!
                self.record_best_path_to(current, neighbor)
        print("No Path Found")
        self.path = None
        return False
        
    def create_openSet(self):
        """ Creates and returns a data structure suitable to hold the set of currently discovered nodes 
        that are not evaluated yet. Initially, only the start node is known."""
        if self.start != None:            
            pq = MinPQ(self.fScore)
            pq.add(self.start)
            return pq
        
        raise(ValueError, "Must create start node before creating an open set. Try running PathPlanner.set_start(start_node)")

    def create_closedSet(self):
        """ Creates and returns a data structure suitable to hold the set of nodes already evaluated"""
        return set()    
                      
    def create_cameFrom(self):
        """Creates and returns a data structure that shows which node can most efficiently be reached from another,
        for each node."""
        return {}
        
    def create_gScore(self):
        """Creates and returns a data structure that holds the cost of getting from the start node to that node, 
        for each node. The cost of going from start to start is zero."""
        return {self.start : 0.0}
        
    def create_fScore(self):
        """Creates and returns a data structure that holds the total cost of getting from the start node to the goal
        by passing by that node, for each node. That value is partly known, partly heuristic.
        For the first node, that value is completely heuristic."""
        # TODO: return a data structure that holds the total cost of getting from the start node to the goal
        # by passing by that node, for each node. That value is partly known, partly heuristic.
        # For the first node, that value is completely heuristic. The rest of the node's value should be 
        # set to infinity.        
        return {self.start : math.inf}
        
    def is_open_empty(self):
        """ Check whether there are still nodes on the frontier to explore.
        Returns True if the open set is empty. False otherwise. """
        # TODO: Return True if the open set is empty. False otherwise.
        return self.openSet.size() > 0
        
    def get_current_node(self):
        """ Find the lowest fScore of the nodes on the frontier.
        Returns the node in the openSet with the lowest value of f(node)."""
        # TODO: Return the node in the open set with the lowest value of f(node).
        return self.openSet.min()
                     
    def get_neighbors(self, node):
        """Returns the neighbors of a node"""
        # TODO: Return the neighbors of a node
        return self.map[node]['connections']
        
    def set_map(self, M):
        """Method used to set map attribute """
        self._reset(self)
        self.start = None
        self.goal = None
        self.map = M

    def set_start(self, start):
        """Method used to set start attribute """
        self._reset(self)
        self.goal = None
        self.start = start

    def set_goal(self, goal):
        """Method used to set goal attribute """
        self._reset(self)
        self.goal = goal        

    def get_gScore(self, node):
        """Returns the g Score of a node"""
        return self.gScore[node]
                

    def distance(self, node_1, node_2):
        """ Computes the Euclidean L2 Distance"""
        x1 = self.map[node_1]['pos'](0)
        y1 = self.map[node_1]['pos'](1)
        x2 = self.map[node_2]['pos'](0)
        y2 = self.map[node_2]['pos'](1)
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def get_tentative_gScore(self, current, neighbor):
        """Returns the tentative g Score of a node"""
        # TODO: Return the g Score of the current node 
        # plus distance from the current node to it's neighbors
        return self.gScore[current] + self.distance(current, neighbor)
        
    def heuristic_cost_estimate(self, node):
        """ Returns the heuristic cost estimate of a node """
        # TODO: Return the heuristic cost estimate of a node
        return self.distance(node, self.goal)
        
        
    def calculate_fscore(self, node):
        """Calculate the f score of a node. """
        # TODO: Calculate and returns the f score of a node. 
        # REMEMBER F = G + H        
        return self.gScore[node] + self.heuristic_cost_estimate(node)
        
    def record_best_path_to(self, current, neighbor):
        """Record the best path to a node """
        # TODO: Record the best path to a node, by updating cameFrom, gScore, and fScore
        self.cameFrom[neighbor] = current
        self.gScore[neighbor] = self.get_tentative_gScore(current, neighbor)
        self.fScore[neighbor] = self.calculate_fscore(neighbor)        
        
map_40 = load_map_40()
#show_map(map_40)
#show_map(map_40, start=5, goal=34, path=[5,16,37,12,34])

planner = PathPlanner(map_40, 5, 34)
path = planner.path
if path == [5, 16, 37, 12, 34]:
    print("great! Your code works for these inputs!")
else:
    print("something is off, your code produced the following:")
    print(path)
#
#   
## Visualize your the result of the above test! You can also change start and goal here to check other paths
#start = 5
#goal = 34
# 
#show_map(map_40, start=start, goal=goal, path=PathPlanner(map_40, start, goal).path)        
 
