import math
import random
import time
MAX_TABU_LENGTH = 50
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


def create_children(start,children_list):
    #children_list = []
    best_child = -1
    best_distance = -1
    for i in range(len(start.cities)-1):
        temp = start.cities[:]
        t = temp[i]
        temp[i] = temp[i+1]
        temp[i+1] = t
        p = Permutation(temp, calculate_distance(temp))
        if best_child == -1:
            best_child = i
            best_distance = p.distance
        elif best_distance > p.distance:
            best_child = i
            best_distance = p.distance
        children_list.append(p)
    # toto ked tak chcem vymazat
    k = len(start.cities)-1
    temp = start.cities[:]
    t = temp[k]
    temp[k] = temp[0]
    temp[0] = t
    p = Permutation(temp, calculate_distance(temp))
    if best_distance > p.distance:
        best_child = len(start.cities)-1
    children_list.append(p)
    return best_child


def tabu_search(permutation, tabu_list):
    count = 0
    best = permutation
    while count < MAX_STEPS:
        children = []
        best_child_pos = create_children(best,children)
        #print(len(children), "haha")
        #print(print_permutation(children[-1].cities))
        localBest = children[best_child_pos]
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


def load_example():
    cities = [Point(60, 200, 1), Point(180, 200, 2), Point(100, 180, 3), Point(140, 180, 4), Point(20, 160, 5),
              Point(80, 160, 6), Point(200, 160, 7), Point(140, 140, 8), Point(40, 120, 9), Point(120, 120, 10),
              Point(180, 100, 11), Point(60, 80, 12), Point(100, 80, 13), Point(180, 60, 14), Point(20, 40, 15),
              Point(100, 40, 16), Point(200, 40, 17), Point(20, 20, 18), Point(60, 20, 19), Point(160, 20, 20)]
    return cities

def main():
    cities = generate_cities(20)
    #cities = load_example()
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

