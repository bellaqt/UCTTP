import random

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

def initialize_population(courses, rooms, periods, days, periods_per_day,population_size, unavailability_constraints):
    population = []
    for i in range(population_size):
        chromosome = []
        for course in courses:
            valid_slots = []
            unavailable = unavailability_constraints.get(course, [])
            unavailable_indices = set(time_index(d, p, periods_per_day) for d, p in unavailable)
            for t in range(periods):
                if t not in unavailable_indices:
                    for room in rooms:
                        valid_slots.append((t, room))
            if valid_slots:
                timeslot, room = random.choice(valid_slots)
                chromosome.append((course, timeslot, room))
            else:
                chromosome.append((course, -1, None))
        population.append(chromosome)
    return population

# fitness
def fitness(chromosome, course_capacities, room_capacities):
    penalty = 0
    seen = set()
    for course, timeslot, room in chromosome:
        key = (timeslot, room)
        if key in seen:
            penalty += 1
        seen.add(key)

        course_size = course_capacities.get(course, 0)
        room_size = room_capacities.get(room, 0)
        #soft constraints, no need add penalty
        #if course_size > room_size:
        #    penalty += 1
    return -penalty

# ---------- roulette,pick a higher individual. ----------
def roulette_wheel_selection(population, fitnesses):
    #Pan
    min_fitness = min(fitnesses)
    adjusted_fitnesses = [f - min_fitness + 1 for f in fitnesses]
    total_fitness = sum(adjusted_fitnesses)
    pick = random.uniform(0, total_fitness)

    current = 0
    for i, fit in enumerate(adjusted_fitnesses):
        current += fit
        if current > pick:
            #print(f"Selected roulette chromosome index: {i}")
            return population[i]
    return population[-1]

# ---------- generate child ----------
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# ---------- mutate, mutation_rate=0.1----------
def mutate(chromosome, mutation_rate, rooms, periods):
    new_chromosome = chromosome[:]
    for i in range(len(chromosome)):
        course, timeslot, room = chromosome[i]
        if random.random() < mutation_rate:
            new_chromosome[i] = (course,random.randint(0, periods - 1),random.choice(rooms))
    return new_chromosome

# ---------- GA main function ----------
def genetic_algorithm(filename, generations, population_size, mutation_rate):
    #get course,room,timeslot,unavailable
    courses, rooms, periods,days, periods_per_day,unavailability_constraints,course_capacities, room_capacities = parse_ctt_file(filename)
    print(f"course account: {len(courses)}")
    print(f"room account: {len(rooms)}")
    print(f"timeslot(periodPerDay * Day): {periods}")
    print(f"unavailability_constraints: {unavailability_constraints}")

    population = initialize_population(courses, rooms, periods,days, periods_per_day, population_size,unavailability_constraints)

    best_solution = None
    best_fitness = float('-inf')

    for generation in range(generations):
        fitnesses = [fitness(chromo, course_capacities, room_capacities) for chromo in population]
        strong_index = fitnesses.index(max(fitnesses))
        #Keep the best individual to the next generation
        new_population = [population[strong_index]]

        while len(new_population) < population_size:
            parent1 = roulette_wheel_selection(population, fitnesses)
            parent2 = roulette_wheel_selection(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate, rooms, periods)
            child2 = mutate(child2, mutation_rate, rooms, periods)
            new_population.extend([child1, child2])

        #update population
        population = new_population[:population_size]

        gen_best = max(fitnesses)
        if gen_best > best_fitness:
            best_fitness = gen_best
            best_solution = population[fitnesses.index(gen_best)]

        #print(f"Generation {generation}: Best Solution = {best_solution} : Best Fitness = {best_fitness}")
    return best_solution, best_fitness, courses
