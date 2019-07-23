# -*- coding: utf-8 -*-
import plotly.io as pio
from helpers import Map, load_map_40, show_map
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
        k = self.i
        if k > self.n:
            raise StopIteration
        self.i += 1
        return k

    def empty(self):
        return self.n == 0

    def min(self):
        return self.elements[1]

    def get_f_score(self, x):
        if x in self.scores.keys():
            return self.scores[x]
        return math.inf

    def score(self, k):
        if self.elements[k] in self.scores:
            self.scores[self.elements[k]]
        return math.inf

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

def distance (m, a, b):
    dx = m.intersections[b][0] - m.intersections[a][0]
    dy = m.intersections[b][1] - m.intersections[a][1]
    return math.hypot(dx, dy)

def neighbours(m, x):
    return m.roads[x]

def construct_path(came_from, x):
    path = [x]
    while x in came_from.keys():
        x = came_from[x]
        path.append(x)

    return [x for x in reversed(path)]

def get_g_score(g_scores, x):
    if x in g_scores.keys():
        return g_scores[x]
    return math.inf

def planner(m, start, goal):
    open_set = MinPQ()
    open_set.add(start)
    f_scores = {start: distance(m, start, goal)}
    open_set.scores = f_scores
    g_scores = {start: 0}
    close_set = set()
    came_from = {}

    while not open_set.empty():
        x = open_set.min()
        if x == goal:
            return construct_path(came_from, x)

        open_set.remove()
        close_set.add(x)
        for y in neighbours(m, x):
            if y in close_set:
                continue

            if get_g_score(g_scores, x) + distance(m, x, y) < get_g_score(g_scores, y):
                g_scores[y] = get_g_score(g_scores, x) + distance(m, x, y)
                f_scores[y] = g_scores[y] + distance(m, y, goal)
                came_from[y] = x

            if  y not in open_set:
                open_set.add(y)

    print('No path found.')
    return None

def test(a_star_search_function):
    MAP_40_ANSWERS = [
        (5, 34, [5, 16, 37, 12, 34]),
        (5, 5,  [5]),
        (8, 24, [8, 14, 16, 37, 12, 17, 10, 24])
    ]

    map_40 = load_map_40()
    correct = 0
    for start, goal, answer_path in MAP_40_ANSWERS:
        path = a_star_search_function(map_40, start, goal)
        if path == answer_path:
            correct += 1
        else:
            print("For start:", start, 
                  "Goal:     ", goal,
                  "Your path:", path,
                  "Correct:  ", answer_path)
    if correct == len(MAP_40_ANSWERS):
        print("All tests pass!!")
    else:
        print("Passed", correct, "/", len(MAP_40_ANSWERS), "test cases")

# test(planner)
m= load_map_40()
start, goal = 8, 24
correct_path = [5, 16, 37, 12, 34]

path = planner(m, start, goal)
show_map(m, start=start, goal=goal, path=path)
