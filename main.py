import math
import random
import time
from tkinter import *
MAX_TABU_LENGTH = 50
MAX_STEPS = 50000
best_solution = None
children_type = 1


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
        x = random.randint(6, 206)
        y = random.randint(6, 206)
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

    l = len(cities)-1
    distance += math.sqrt(math.pow((cities[l].x - cities[0].x), 2) + math.pow((cities[l].y - cities[0].y), 2))
    return distance


def create_children_test(start, children_list, tabu_list, matrix):
    best_child = -1
    global best_solution
    r = random.randint(0, len(start.cities)-1)
    for i in range(len(start.cities)):
        if r == i:
            continue
        temp = start.cities[:]
        t = temp[i]
        temp[i] = temp[r]
        temp[r] = t

        p = Permutation(temp, calculate_distance_test(temp, matrix))
        # p = Permutation(temp, new_dist)
        if (best_child == -1 or best_child.distance > p.distance) and p.cities not in tabu_list:
            best_child = p
        # elif best_child != -1 and best_child.distance > p.distance and p.cities not in tabu_list:
        #     best_child = p
        children_list.append(p)
    return best_child


def create_tabu_value(cities):
    s = ""
    for city in cities:
        s += str(city.n)+ " "
    return s

def check_occurence_limit(d,val):
    occurences = d.get(val)
    if occurences is None:
        return False
    elif occurences > 5:
        #print("Vela tam bol")
        return True
    return False

def create_children_neighbours(start, children_list, tabu_list, matrix, occurance_dictionary):
    best_child = -1
    global best_solution
    for i in range(len(start.cities)-1):
        temp = start.cities[:]
        t = temp[i]
        temp[i] = temp[i+1]
        temp[i+1] = t
        p = Permutation(temp, calculate_distance_test(temp, matrix))
        #val = create_tabu_value(p.cities)
        if (best_child == -1 or best_child.distance > p.distance) and p.cities not in tabu_list: #and not check_occurence_limit(occurance_dictionary, val)
            best_child = p
        children_list.append(p)
    k = len(start.cities)-1
    temp = start.cities[:]
    t = temp[k]
    temp[k] = temp[0]
    temp[0] = t
    p = Permutation(temp, calculate_distance_test(temp, matrix))
    if best_child.distance > p.distance and p.cities not in tabu_list:
        best_child = p
    children_list.append(p)
    return best_child


def tabu_search(permutation, tabu_list, matrix):
    count = 0
    current = permutation
    occurence_dictionary = {}
    global best_solution
    while count < MAX_STEPS:
        children = []
        if children_type == 2:
            best_child = create_children_test(current, children, tabu_list, matrix)
        else:
            best_child = create_children_neighbours(current, children, tabu_list, matrix, occurence_dictionary)
        # print("current")
        # print_permutation(current.cities)
        # print(current.distance)

        if current.distance < best_solution.distance:
            print("new best ", current.distance)
            print_permutation(best_solution.cities)
            print("Generation ", count)
            best_solution = current
        # lokalny extrem nemam mensiu vzdialenost
        if current.distance <= best_child.distance:
            tabu_list.append(current.cities)
            # if children_type == 1:
            #     val = create_tabu_value(best_child.cities)
            #     oc = occurence_dictionary.get(val)
            #     if oc is None:
            #         occurence_dictionary[val] = 1
            #     else:
            #         occurence_dictionary[val] +=1
        current = best_child

        if len(tabu_list) > MAX_TABU_LENGTH:
            tabu_list = tabu_list[1:]
        count += 1
        #print("="*50)
    print_permutation(best_solution.cities)
    print("Distance ", best_solution.distance)
    return best_solution


def draw_salesman(first_permutation, final_permutation):
    window = Tk()
    c = Canvas(window, width=500, height=400)
    c.pack()
    c2 = Canvas(window, width=500, height=400)
    c2.pack()
    #zadanie
    for city in first_permutation.cities:
        c.create_oval(city.x-5, city.y-5, city.x+5, city.y+5,fill="red")
        c.create_text(city.x, city.y-10, text=str(city.n))

    for i in range(len(first_permutation.cities) - 1):
        city1 = first_permutation.cities[i]
        city2 = first_permutation.cities[i + 1]
        c.create_line(city1.x, city1.y, city2.x, city2.y)
    last = len(first_permutation.cities) - 1
    city1 = first_permutation.cities[last]
    city2 = first_permutation.cities[0]
    c.create_line(city1.x, city1.y, city2.x, city2.y)


    # vysledok
    for city in final_permutation.cities:
        c2.create_oval(city.x-5, city.y-5, city.x+5, city.y+5,fill="red")
        c2.create_text(city.x, city.y-10, text=str(city.n))

    for i in range(len(final_permutation.cities) - 1):
        city1 = final_permutation.cities[i]
        city2 = final_permutation.cities[i + 1]
        c2.create_line(city1.x, city1.y, city2.x, city2.y)
    last = len(final_permutation.cities) - 1
    city1 = final_permutation.cities[last]
    city2 = final_permutation.cities[0]
    c2.create_line(city1.x , city1.y , city2.x , city2.y )

    window.mainloop()


def load_example():
    cities = [Point(60, 200, 1), Point(180, 200, 2), Point(100, 180, 3), Point(140, 180, 4), Point(20, 160, 5),
              Point(80, 160, 6), Point(200, 160, 7), Point(140, 140, 8), Point(40, 120, 9), Point(120, 120, 10),
              Point(180, 100, 11), Point(60, 80, 12), Point(100, 80, 13), Point(180, 60, 14), Point(20, 40, 15),
              Point(100, 40, 16), Point(200, 40, 17), Point(20, 20, 18), Point(60, 20, 19), Point(160, 20, 20)]
    return cities


def write_to_file(cities):
    f = open("input.txt", "w")
    for city in cities:
        print(city.x, city.y, file=f)
    f.close()

def load_from_file():
    f = open("input.txt", "r")
    lines = f.readlines()
    cities = []
    counter = 0
    for line in lines:
        line = line.split(" ")
        x = int(line[0])
        y = int(line[1])
        counter += 1
        cities.append(Point(x, y, counter))
    f.close()
    return cities


def create_matrix(cities, n):
    matrix = [[0 for i in range(n)] for y in range(n)]
    for i in range(n):
        for k in range(n):
            if i == k:
                continue
            matrix[i][k] = math.sqrt(math.pow((cities[i].x - cities[k].x), 2) + math.pow((cities[i].y - cities[k].y), 2))
    return matrix

def calculate_distance_test(cities, matrix):
    length = len(cities)
    distance = 0
    for i in range(length - 1):
        distance += matrix[cities[i].n-1][cities[i+1].n-1]

    l = len(cities) - 1
    distance += math.sqrt(math.pow((cities[l].x - cities[0].x), 2) + math.pow((cities[l].y - cities[0].y), 2))
    return distance

def main():
    global MAX_TABU_LENGTH
    global MAX_STEPS
    global best_solution
    global children_type
    load_option = input("Read from input file or generate random permutation or load sample permutation? 1/2/3 \n")
    cities = []
    if load_option == "1":
        cities = load_from_file()
    elif load_option == "2":
        number_cities = int(input("Number of cities "))
        cities = generate_cities(number_cities)
    else:
        cities = load_example()
    #write_to_file(cities)
    matrix = create_matrix(cities, len(cities))
    length_tabu = int(input("Length of tabu list "))
    MAX_TABU_LENGTH = length_tabu
    MAX_STEPS = int(input("Number of generations "))
    children_type = int(input("Children type 1 (zo zadania) /2 lepsi sposob\n"))
    start_perm = Permutation(cities, calculate_distance(cities))
    dist = calculate_distance_test(cities, matrix)
    print(dist)
    print(start_perm.distance)

    best_solution = start_perm
    first = start_perm

    print_permutation(cities)
    print(start_perm.distance)
    print("-"*50)
    start = time.time()
    final = tabu_search(start_perm, [], matrix)
    end = time.time()
    print(end - start, "s")
    draw_salesman(first, final)
    save = input("Save this cities config? yes/no \n")
    if save=="yes":
        write_to_file(first.cities)


if __name__ == '__main__':
    main()

