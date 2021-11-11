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


def create_children_second_type(start, children_list, tabu_list, matrix):
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

        p = Permutation(temp, calculate_distance_w_matrix(temp, matrix))
        if best_child == -1:
            best_child = p
        # p = Permutation(temp, new_dist)
        if (best_child == -1 or best_child.distance > p.distance) and p.cities not in tabu_list:
            best_child = p
        # elif best_child != -1 and best_child.distance > p.distance and p.cities not in tabu_list:
        #     best_child = p
        children_list.append(p)
    return best_child


def create_children_neighbours(start, children_list, tabu_list, matrix):
    best_child = -1
    global best_solution
    for i in range(len(start.cities)-1):
        temp = start.cities[:]
        t = temp[i]
        temp[i] = temp[i+1]
        temp[i+1] = t
        p = Permutation(temp, calculate_distance_w_matrix(temp, matrix))
        if (best_child == -1 or best_child.distance > p.distance) and p.cities not in tabu_list:
            best_child = p
        children_list.append(p)
    k = len(start.cities)-1
    temp = start.cities[:]
    t = temp[k]
    temp[k] = temp[0]
    temp[0] = t
    p = Permutation(temp, calculate_distance_w_matrix(temp, matrix))
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
            best_child = create_children_second_type(current, children, tabu_list, matrix)
        else:
            best_child = create_children_neighbours(current, children, tabu_list, matrix)
        # print("current")
        # print_permutation(current.cities)
        # print(current.distance)
        if best_child == -1:
            best_child = children[0]

        if current.distance < best_solution.distance:
            print("Nové minimum ", current.distance)
            print_permutation(best_solution.cities)
            print("Generácia ", count)
            best_solution = current
        # lokalny extrem nemam mensiu vzdialenost
        if current.distance <= best_child.distance:
            tabu_list.append(current.cities)
            #print("Lokalny extrem")
        current = best_child

        if len(tabu_list) > MAX_TABU_LENGTH:
            tabu_list = tabu_list[1:]
        count += 1
        #print("="*50)
    print_permutation(best_solution.cities)
    print("Celková vzdialenosť ", best_solution.distance)
    return best_solution


def draw_salesman(first_permutation, final_permutation):
    window = Tk()
    c = Canvas(window, width=500, height=400)
    c.pack()
    c2 = Canvas(window, width=500, height=400)
    c2.pack()
    #zadanie
    for city in first_permutation.cities:
        c.create_oval(city.x*2-5, city.y*2-5, city.x*2+5, city.y*2+5,fill="red")
        c.create_text(city.x*2, city.y*2-10, text=str(city.n))

    for i in range(len(first_permutation.cities) - 1):
        city1 = first_permutation.cities[i]
        city2 = first_permutation.cities[i + 1]
        c.create_line(city1.x*2, city1.y*2, city2.x*2, city2.y*2)
    last = len(first_permutation.cities) - 1
    city1 = first_permutation.cities[last]
    city2 = first_permutation.cities[0]
    c.create_line(city1.x*2, city1.y*2, city2.x*2, city2.y*2)


    # vysledok
    for city in final_permutation.cities:
        c2.create_oval(city.x*2-5, city.y*2-5, city.x*2+5, city.y*2+5,fill="red")
        c2.create_text(city.x*2, city.y*2-10, text=str(city.n))

    for i in range(len(final_permutation.cities) - 1):
        city1 = final_permutation.cities[i]
        city2 = final_permutation.cities[i + 1]
        c2.create_line(city1.x*2, city1.y*2, city2.x*2, city2.y*2)
    last = len(final_permutation.cities) - 1
    city1 = final_permutation.cities[last]
    city2 = final_permutation.cities[0]
    c2.create_line(city1.x*2 , city1.y*2 , city2.x*2 , city2.y*2 )

    window.mainloop()


def load_example():
    cities = [Point(60, 200, 1), Point(180, 200, 2), Point(100, 180, 3), Point(140, 180, 4), Point(20, 160, 5),
              Point(80, 160, 6), Point(200, 160, 7), Point(140, 140, 8), Point(40, 120, 9), Point(120, 120, 10),
              Point(180, 100, 11), Point(60, 80, 12), Point(100, 80, 13), Point(180, 60, 14), Point(20, 40, 15),
              Point(100, 40, 16), Point(200, 40, 17), Point(20, 20, 18), Point(60, 20, 19), Point(160, 20, 20)]
    return cities


def write_to_file(cities):
    name = input("Nazov suboru +.txt\n")
    f = open(name, "w")
    for city in cities:
        print(city.x, city.y, file=f)
    f.close()

def load_from_file(name):
    f = open(name, "r")
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

def calculate_distance_w_matrix(cities, matrix):
    length = len(cities)
    distance = 0
    for i in range(length - 1):
        distance += matrix[cities[i].n-1][cities[i+1].n-1]

    l = len(cities) - 1
    distance += matrix[cities[l].n-1][cities[0].n-1]
    #distance += math.sqrt(math.pow((cities[l].x - cities[0].x), 2) + math.pow((cities[l].y - cities[0].y), 2))
    return distance

def main():
    global MAX_TABU_LENGTH
    global MAX_STEPS
    global best_solution
    global children_type
    load_option = input("Čítať zo súboru, vygenerovať náhodné mestá alebo vzorový vstup zo zadania? 1/2/3 \n")
    cities = []
    if load_option == "1":
        name = input("Nazov suboru +.txt\n")
        cities = load_from_file(name)
    elif load_option == "2":
        number_cities = int(input("Počet miest "))
        cities = generate_cities(number_cities)
    else:
        cities = load_example()
    matrix = create_matrix(cities, len(cities))
    length_tabu = int(input("Dĺžka tabu listu "))
    MAX_TABU_LENGTH = length_tabu
    MAX_STEPS = int(input("Počet generácií (koľko krát generujem nasledovníkov) "))
    children_type = int(input("Typ generovania nasledovníkov 1 (zo zadania) /2 výmena náhodného mesta s ostatnými\n"))
    start_perm = Permutation(cities, calculate_distance_w_matrix(cities,matrix))
    dist = calculate_distance_w_matrix(cities, matrix)
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
    save = input("Uložiť túto permutáciu miest? ano/nie \n")
    if save=="ano":
        write_to_file(first.cities)


if __name__ == '__main__':
    main()

