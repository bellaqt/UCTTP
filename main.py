from function import genetic_algorithm
from function import simulated_annealing
import time

def main():

    print("Choose method:")
    print("1 - GA only")
    print("2 - SA only")
    print("3 - GA + SA (Hybrid)")
    choice = input("Your choice: ").strip()

    filename = "DataSet/Scalability/comp02_8.ctt"

    start_time = time.time()

    if choice == "1":
        # run 50 times, remain 30 items,mutation is 10%
        # generation -> population(Multiple complete curriculum) -> chromosome(A complete curriculum) -> gene(course)
        generations = 50
        population_size = 30
        mutation_rate = 0.1
        hybrid = False
        solution, fitness, courses = genetic_algorithm(filename, generations, population_size, mutation_rate, hybrid)
        end_time = time.time()
    elif choice == "2":
        initial_temp = 100
        cooling_rate = 0.97
        min_temp = 0.01
        max_iter = 30000
        solution, fitness, courses = simulated_annealing(filename, initial_temp, cooling_rate, min_temp, max_iter)
        end_time = time.time()
    elif choice == "3":
        generations = 50
        population_size = 30
        mutation_rate = 0.1
        hybrid = True
        solution, fitness, courses = genetic_algorithm(filename, generations, population_size, mutation_rate, hybrid)
        end_time = time.time()
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        exit()

    running_time = end_time - start_time
    print(running_time)
    output_file = "TestResult/Scalability/comp02_8_GA_50_30_0.1.txt"

    with open(output_file, "w") as f:
        f.write(f"Running on: {filename}\n")
        f.write(f"\nFinal Best Fitness: {fitness}\n")
        f.write("Best Solution (timeslot, room) per course:\n")
        for idx, (course, (timeslot, room)) in enumerate(solution.items()):
            f.write(f"{course}: Timeslot={timeslot}, Room={room}\n")

        f.write(f"\nTotal Run Time: {running_time:.3f} seconds\n")

    print(f"Results have been written to {output_file}")

    #chromsome example
    #{'c0001': (21, 'F'), 'c0002': (0, 'B'), 'c0004': (27, 'C'), 'c0005': (10, 'G'), 'c0014': (14, 'E'),
    # 'c0015': (7, 'G'), 'c0016': (16, 'E'), 'c0017': (3, 'S'), 'c0024': (11, 'F'), 'c0025': (26, 'B'),
    # 'c0078': (18, 'F'), 'c0030': (26, 'C'), 'c0031': (22, 'B'), 'c0032': (20, 'E'), 'c0033': (2, 'B'),
    # 'c0057': (18, 'S'), 'c0058': (23, 'E'), 'c0059': (21, 'F'), 'c0061': (14, 'B'), 'c0062': (15, 'G'),
    # 'c0063': (15, 'S'), 'c0064': (19, 'F'), 'c0065': (25, 'G'), 'c0066': (27, 'F'), 'c0067': (29, 'S'),
    # 'c0068': (16, 'G'), 'c0069': (4, 'G'), 'c0070': (9, 'E'), 'c0071': (17, 'F'), 'c0072': (17, 'E')}

if __name__ == "__main__":
    main()