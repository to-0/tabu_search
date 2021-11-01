import math
import random
import time
MAX_TABU_LENGTH = 100
MAX_STEPS = 50000


class Point:
    def __init__(self, x: int, y: int, n: int):
        self.x = x
        self.y = y
        self.n = n

class Permutation:
    def __init__(self, cities, distance: int):
        self.cities = cities
        self.distance = distance


def generate_cities(n):
    cities = []
    for i in range(n):
        x = random.randint(0, 200)
        y = random.randint(0, 200)
        cities.append(Point(x, y, i+1))
    return cities


def print_permutation(cities):
    s = []
    for city in cities:
        s.append(city.n)
    print(s)

def calculate_distance(cities):
    length = len(cities)
    distance = 0
    for i in range(length-1):
        distance += math.sqrt(math.pow((cities[i].x - cities[i+1].x), 2) + math.pow((cities[i].y - cities[i+1].y), 2))
    return distance


def create_children(start):
    children_list = []
    for i in range(len(start.cities)-1):
        temp = start.cities[:]
        t = temp[i]
        temp[i] = temp[i+1]
        temp[i+1] = t
        children_list.append(Permutation(temp, calculate_distance(temp)))
    return children_list


def find_best_child(children, tabu_list):
    mind = children[0].distance
    n = 0
    count = 0
    for child in children:
        # tie cities su vzdy rovnake objekty len prehadzujem ich poradie ale nevytvaram nove Point objekty, tie point
        #pointre su rovnake
        if mind > child.distance and child.cities not in tabu_list:
            mind = child.distance
            n = count
        count += 1
    return n

def tabu_search(permutation, tabu_list):
    count = 0
    best = permutation
    while count < MAX_STEPS:
        children = create_children(best)
        #print(permutation.cities)
        #print(children[0].cities)
        position = find_best_child(children, tabu_list)
        localBest = children[position]
        # sme v lokalnom extreme
        if localBest.distance > best.distance:
            if len(tabu_list) > MAX_TABU_LENGTH:
                tabu_list = tabu_list[1:]
            tabu_list.append(best.cities)
        best = localBest
        count += 1
        print(localBest.distance)
    print_permutation(best.cities)
    print("Distance ", best.distance)

    #print(children)
    #print(children[0])
    #print_permutation(children[0].cities)
    #print(children[0].distance)


def main():
    cities = generate_cities(20)
    start_perm = Permutation(cities, calculate_distance(cities))
    print_permutation(cities)
    print(start_perm.distance)
    print("-"*50)
    start = time.time()
    tabu_search(start_perm, [])
    end = time.time()
    print(end-start, "s")




if __name__ == '__main__':
    main()

