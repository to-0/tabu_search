import math
import random
import time
from tkinter import *
MAX_TABU_LENGTH = 50
MAX_STEPS = 50000
best_solution = None
time_compare = 0
time_create_val = 0

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

    l = len(cities)-1
    distance += math.sqrt(math.pow((cities[l].x - cities[0].x), 2) + math.pow((cities[l].y - cities[0].y), 2))
    return distance


def create_children(start, children_list, tabu_list, check_type):
    #children_list = []
    best_child = -1
    best_distance = -1
    global best_solution
    for i in range(len(start.cities)-1):
        temp = start.cities[:]
        t = temp[i]
        temp[i] = temp[i+1]
        temp[i+1] = t
        p = Permutation(temp, calculate_distance(temp))
        if best_child == -1:
            best_child = i
            best_distance = p.distance
        elif best_distance > p.distance and not find_in_tabu(tabu_list, p.cities, check_type):
            best_child = i
            best_distance = p.distance

        #elif p.cities in tabu_list:
            #print("Je v tabu liste", p.distance)
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


def create_tabu_value(cities):
    global time_create_val
    start = time.time()
    s = ""
    for city in cities:
        s += str(city.n)+ " "
    end = time.time()
    time_create_val += (end-start)
    return s

def find_in_tabu(tabu, cities_perm, check_type):
    global time_compare
    start = time.time()
    if check_type ==1:
        val = cities_perm in tabu
        end = time.time()
        time_compare += (end-start)
        return val

    val = create_tabu_value(cities_perm)
    for element in tabu:
        if element == val:
            end = time.time()
            time_compare += (end - start)
            return True
    end = time.time()
    time_compare += (end - start)
    return False

def tabu_search(permutation, tabu_list, check_type):
    count = 0
    current = permutation
    global best_solution
    while count < MAX_STEPS:
        children = []
        best_child_pos = create_children(current, children, tabu_list,check_type)
        #tabu_list.append(children[0].cities)
        #tabu_list.append(children[1].cities)
        # if children[3].cities not in tabu_list:
        #     print("Toto je dobre")
        # if children[0].cities in tabu_list:
        #     print("Aj toto")
        #print(len(children), "haha")
        #print(print_permutation(children[-1].cities))
        localBest = children[best_child_pos]
        # sme v lokalnom extreme
        if check_type == 2:
            val = create_tabu_value(current.cities)
        if localBest.distance > current.distance:
            if len(tabu_list) > MAX_TABU_LENGTH:
                #print("Max length exceeded ")
                tabu_list.pop(0)
            if check_type == 1:
                tabu_list.append(current.cities)
            else:
                tabu_list.append(val)
        current = localBest

        if current.distance < best_solution.distance:
            best_solution = current
        count += 1
        #print(localBest.distance)
    print_permutation(best_solution.cities)
    print("Distance ", best_solution.distance)
    return current


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
    c.create_line(city1.x * 2, city1.y * 2, city2.x * 2, city2.y * 2)


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
    c2.create_line(city1.x * 2, city1.y * 2, city2.x * 2, city2.y * 2)

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
    f = open("input.txt","r")
    lines = f.readlines()
    cities = []
    counter = 0
    for line in lines:
        line = line.split(" ")
        x = int(line[0])
        y = int(line[1])
        counter += 1
        cities.append(Point(x,y,counter))
    f.close()
    return cities

def main():
    global MAX_TABU_LENGTH
    global MAX_STEPS
    global best_solution
    load_option = input("Read from input file or generate random permutation? 1/2 \n")
    cities = []
    if load_option == "1":
        cities = load_from_file()
    else:
        number_cities = int(input("Number of cities "))
        cities = generate_cities(number_cities)

    #write_to_file(cities)
    #cities = load_example()
    length_tabu = int(input("Length of tabu list "))
    MAX_TABU_LENGTH = length_tabu
    MAX_STEPS = int(input("Number of generations "))
    start_perm = Permutation(cities, calculate_distance(cities))
    best_solution = start_perm
    first = start_perm
    check_type = int(input("Check type 1/2\n"))

    print_permutation(cities)
    print(start_perm.distance)
    print("-"*50)
    start = time.time()
    final = tabu_search(start_perm, [], check_type)
    end = time.time()
    print(end - start, "s")
    print("Compare time ", time_compare)
    print("Create val time", time_create_val)
    draw_salesman(first, final)
    save = input("Save this cities config? yes/no \n")
    if save=="yes":
        write_to_file(first.cities)


if __name__ == '__main__':
    main()

