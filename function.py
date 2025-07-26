import random
import math

# parse ctt file
def parse_ctt_file(filename):
    courses = []
    rooms = []
    periods = 0
    days = 0
    periods_per_day = 0
    unavailability_constraints = {}

    course_capacities = {}
    room_capacities = {}

    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("Days:"):
            #get days
            days = int(line.split(":")[1].strip())
        elif line.startswith("Periods_per_day:"):
            #get periods per day
            periods_per_day = int(line.split(":")[1].strip())

    in_courses = False
    in_rooms = False
    in_unavailability = False

    for line in lines:
        line = line.strip()

        if line == "COURSES:":
            in_courses = True
            in_rooms = False
            continue
        elif line == "ROOMS:":
            in_courses = False
            in_rooms = True
            continue
        elif line == "UNAVAILABILITY_CONSTRAINTS:":
            in_courses = False
            in_rooms = False
            in_unavailability = True
            continue
        elif line.endswith(":"):
            in_courses = False
            in_rooms = False
            continue

        if in_courses:
            #get courses
            course = line.split()
            if len(course) >= 1:
                #get rooms
                courses.append(course[0])
                capacity = int(course[4])
                course_capacities[course[0]] = capacity
        elif in_rooms:
            parts = line.split()
            if len(parts) >= 1:
                #get rooms
                capacity = int(parts[1])
                rooms.append(parts[0])
                room_capacities[parts[0]] = capacity
        elif in_unavailability:
            # Example: c0001 4 0
            parts = line.split()
            if len(parts) == 3:
                course_id, day, period = parts[0], int(parts[1]), int(parts[2])
                if course_id not in unavailability_constraints:
                    unavailability_constraints[course_id] = []
                unavailability_constraints[course_id].append((day, period))

    periods = days * periods_per_day
    return courses, rooms, periods, days, periods_per_day, unavailability_constraints, course_capacities, room_capacities

# init population
def time_index(day, period, periods_per_day):
    return day * periods_per_day + period

def build_valid_assignment_map(courses, rooms, periods, periods_per_day, unavailability_constraints):
    assignment_map = {}
    for course in courses:
        unavailable = unavailability_constraints.get(course, [])
        unavailable_indices = set(time_index(d, p,periods_per_day) for d, p in unavailable)

        valid = []
        for t in range(periods):
            if t not in unavailable_indices:
                for r in rooms:
                    valid.append((t, r))
        assignment_map[course] = valid
    return assignment_map

def initialize_population(courses,population_size,valid_assignment_map):
    population = []
    for i in range(population_size):
        chromosome = {}
        for course in courses:
            valid_slots = valid_assignment_map.get(course, [])
            if valid_slots:
                timeslot, room = random.choice(valid_slots)
                chromosome[course] = (timeslot, room)
            else:
                chromosome[course] = (-1, None)
        population.append(chromosome)
    return population

# fitness
def fitness(chromosome, course_capacities, room_capacities):
    penalty = 0
    seen = set()
    for course, (timeslot, room) in chromosome.items():
        key = (timeslot, room)
        if key in seen:
            penalty += 1
        seen.add(key)

        course_size = course_capacities.get(course, 0)
        room_size = room_capacities.get(room, 0)
        #soft constraints, no need add penalty
        #if course_size > room_size:
        #    penalty += 1
    return penalty

# ---------- roulette,pick a higher individual. ----------
def roulette_wheel_selection(population, fitnesses):
    #Pan
    adjusted_fitnesses = [1 / (f + 1) for f in fitnesses]
    total_fitness = sum(adjusted_fitnesses)
    pick = random.uniform(0, total_fitness)
    current = 0
    for i, fit in enumerate(adjusted_fitnesses):
        current += fit
        if current > pick:
            return population[i]
    return population[-1]

# ---------- generate child ----------
def crossover(parent1, parent2, valid_assignment_map):
    point = random.randint(1, len(parent1) - 1)
    keys = list(parent1.keys())
    #parent is chromosome, which equals population[i]
    child1,child2 = {},{}
    used1, used2 = set(), set()

    for i in keys[:point]:
        slot1 = parent1[i]
        slot2 = parent2[i]
        if slot1 not in used1:
            child1[i] = slot1
            used1.add(child1[i])
        else:
            child1[i] = (-1, None)

        if slot2 not in used2:
            child2[i] = slot2
            used2.add(child2[i])
        else:
            child2[i] = (-1, None)

    for j in keys[point:]:
        slot1 = parent2[j]
        slot2 = parent1[j]
        if slot1 not in used1:
            child1[j] = slot1
            used1.add(child1[j])
        elif parent1[j] not in used1:
            child1[j] = parent1[j]
            used1.add(parent1[j])
        else:
            child1[j] = (-1, None)

        if slot2 not in used2:
            child2[j] = slot2
            used2.add(child2[j])
        elif parent2[j] not in used2:
            child2[j] = parent2[j]
            used2.add(parent2[j])
        else:
            child2[j] = (-1, None)
    return child1, child2

# ---------- mutate, mutation_rate=0.1----------
def mutate(chromosome, mutation_rate, valid_assignment_map):
    used_slots = set(chromosome.values())
    for course, (timeslot, room) in chromosome.items():
        if random.random() < mutation_rate:
            valid_slots = valid_assignment_map.get(course, [])
            available = [slot for slot in valid_slots if slot not in used_slots]

            if available:
                new_slot = random.choice(available)
                used_slots.add(new_slot)
                chromosome[course] = new_slot
                used_slots.remove(chromosome[course])
    return chromosome

# ---------- GA main function ----------
def genetic_algorithm(filename, generations, population_size, mutation_rate):
    #get course,room,timeslot,unavailable
    courses, rooms, periods,days, periods_per_day,unavailability_constraints,course_capacities, room_capacities = parse_ctt_file(filename)
    print(f"course account: {len(courses)}")
    print(f"room account: {len(rooms)}")
    print(f"timeslot(periodPerDay * Day): {periods}")
    print(f"unavailability_constraints: {unavailability_constraints}")

    valid_assignment_map = build_valid_assignment_map(
        courses, rooms, periods, periods_per_day, unavailability_constraints
    )

    population = initialize_population(courses, population_size, valid_assignment_map)
    best_solution = None
    best_fitness = float('inf')

    for generation in range(generations):
        fitnesses = [fitness(chromo, course_capacities, room_capacities) for chromo in population]
        strong_index = fitnesses.index(min(fitnesses))

        gen_best = min(fitnesses)
        if gen_best == 0:
            best_solution = population[strong_index]
            best_fitness = gen_best
            print(f"Best solution found at generation {generation}")
            return best_solution, best_fitness, courses

        #If not = 0, keep the best individual to the next generation
        new_population = [population[strong_index]]

        while len(new_population) < population_size:
            parent1 = roulette_wheel_selection(population, fitnesses)
            parent2 = roulette_wheel_selection(population, fitnesses)
            if parent1 != parent2:
                child1, child2 = crossover(parent1, parent2, valid_assignment_map)
                child1 = mutate(child1, mutation_rate, valid_assignment_map)
                child2 = mutate(child2, mutation_rate, valid_assignment_map)
                new_population.extend([child1, child2])

        #update population
        population = new_population[:population_size]

        gen_best = min(fitnesses)
        if gen_best < best_fitness:
            best_fitness = gen_best
            best_solution = population[fitnesses.index(gen_best)]

        #print(f"Generation {generation}: Best Solution = {best_solution} : Best Fitness = {best_fitness}")
    return best_solution, best_fitness, courses

def simulated_annealing(filename, initial_temp, cooling_rate, min_temp, max_iter):
    #Initial solution → Neighborhood generation → Acceptance criteria → Cooling mechanism → Termination condition
    courses, rooms, periods,days, periods_per_day,unavailability_constraints,course_capacities, room_capacities = parse_ctt_file(filename)
    print(f"course account: {len(courses)}")
    print(f"room account: {len(rooms)}")
    print(f"timeslot(periodPerDay * Day): {periods}")
    print(f"unavailability_constraints: {unavailability_constraints}")

    valid_assignment_map = build_valid_assignment_map(
        courses, rooms, periods, periods_per_day, unavailability_constraints
    )

    current_solution = {}
    for course in courses:
        valid_slots = valid_assignment_map.get(course, [])
        if valid_slots:
            current_solution[course] = random.choice(valid_slots)
        else:
            current_solution[course] = (-1, None)

    current_fitness = fitness(current_solution, course_capacities, room_capacities)

    if current_fitness == 0:
        return current_solution, current_fitness, courses

    T = initial_temp

    for iteration in range(max_iter):
        if T <= min_temp:
            break

        neighbor = current_solution.copy()
        course = random.choice(courses)
        if valid_assignment_map[course]:
            neighbor[course] = random.choice(valid_assignment_map[course])

        neighbor_fitness = fitness(neighbor, course_capacities, room_capacities)
        delta = neighbor_fitness - current_fitness

        #delta < 0 means neighbor better than current
        #e(0.01) ≈ 1.01005, e(-0.01) ≈ 0.99
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_solution = neighbor
            current_fitness = neighbor_fitness
            if current_fitness == 0:
                print('perfect')
                return current_solution, current_fitness, courses

        if iteration % 100 == 0:
            T *= cooling_rate

    return current_solution, current_fitness, courses