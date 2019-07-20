# -*- coding: utf-8 -*-
import plotly.io as pio
from helpers import Map, load_map_10, load_map_40, show_map
import math

class MinPQ():
    def __init__(self):
        self.n = 0
        self.scores = {}
        self.elements = [None]
        self.i = 1
        
    def __iter__(self):
        self.i = 1
        return self
        
    def __next__(self):
        if self.i > self.n:
            raise StopIteration
        self.i += 1
        
    def min(self):
        return self.elements[1]
        
    def score(self, k):
        if self.elements[k] not in self.scores:
            return math.inf
        return self.scores[self.elements[k]]
    
    def add(self, x):
        self.n += 1
        self.elements.append(x)
        self.swim(self.n)
    
    def remove(self):
        self.elements[1], self.elements[self.n] = self.elements[self.n], self.elements[1]
        del self.elements[-1]
        self.n -= 1
        self.sink(1)
        
    def sink(self, k):
        while k*2 <= self.n:
            i = k*2
            if i < self.n and self.score(i) > self.score(i+1):
                i += 1
            if self.score(k) <= self.score(i):
                break 
            self.elements[k], self.elements[i] = self.elements[i], self.elements[k]
            k = i
        
    def swim(self, k):
        while k//2 >= 1:
            if self.score(k//2) <= self.score(k):
                break
            self.elements[k], self.elements[k//2] = self.elements[k//2], self.elements[k]
            k = k//2

m = load_map_40()
start = 30
goal = 24

def distance(a, b):
    delta_x = m.intersections[b][0] - m.intersections[a][0]
    delta_y = m.intersections[b][1] - m.intersections[a][1]
    return math.hypot(delta_x, delta_y)

g_scores = {start: 0}
f_scores = {start: distance(start,goal)}
came_from = {}

def get_g_score(a):
    if a not in g_scores:
        return math.inf
    return g_scores[a]

def trace_path(a):
    path = [a]
    while a in came_from.keys():
        a = came_from[a]
        path.append(a)
    return [x for x in reversed(path)]
    
def search(m, start, goal):    
    closed_set = set()
    open_set = MinPQ()
    open_set.add(start)
    open_set.scores = f_scores
    
    while open_set.n != 0:
        current = open_set.min()
        
        if current == goal:
            return trace_path(goal)
        
        open_set.remove()
        closed_set.add(current)
        
        for neighbor in m.roads[current]:
            if neighbor in closed_set:
                continue
            
            if neighbor not in open_set:
                open_set.add(neighbor)
                
            if get_g_score(current) + distance(current, neighbor) < get_g_score(neighbor):
                g_scores[neighbor] = get_g_score(current) + distance(current, neighbor)
                f_scores[neighbor] = get_g_score(neighbor) + distance(neighbor, goal)
                came_from[neighbor] = current
    
    print('No path found')
    return None
    
path=search(m, start, goal)
print(path)
show_map(m, start=start, goal=goal, path=path)