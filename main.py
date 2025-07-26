from function import genetic_algorithm
from function import simulated_annealing
import time

def main():

    print("Choose method:")
    print("1 - GA only")
    print("2 - SA only")
    print("3 - GA + SA (Hybrid)")
    choice = input("Your choice: ").strip()

    filename = "DataSet/Early/comp01.ctt"

    print("Running on:", filename)

    start_time = time.time()

    if choice == "1":
        # run 50 times, remain 30 items,mutation is 10%
        # generation -> population(Multiple complete curriculum) -> chromosome(A complete curriculum) -> gene(course)
        generations = 150
        population_size = 100
        mutation_rate = 0.1
        solution, fitness, courses = genetic_algorithm(filename, generations, population_size, mutation_rate)
        end_time = time.time()
    elif choice == "2":
        initial_temp = 100
        cooling_rate = 0.9
        min_temp = 0.01
        max_iter = 10000
        solution, fitness, courses = simulated_annealing(filename, initial_temp, cooling_rate, min_temp, max_iter)
        end_time = time.time()
    elif choice == "3":
        print('TODO')
        solution, fitness, courses = None,None,None
        end_time = time.time()
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        exit()

    running_time = end_time - start_time
    print(f"\nTotal Run Time: {running_time:.2f} seconds")

    print("\nFinal Best Fitness:", fitness)
    print("Best Solution (timeslot, room) per course:")
    for idx, (course, (timeslot, room)) in enumerate(solution.items()):
        print(f"{course}: Timeslot={timeslot}, Room={room}")

    #chromsome example
    #{'c0001': (21, 'F'), 'c0002': (0, 'B'), 'c0004': (27, 'C'), 'c0005': (10, 'G'), 'c0014': (14, 'E'),
    # 'c0015': (7, 'G'), 'c0016': (16, 'E'), 'c0017': (3, 'S'), 'c0024': (11, 'F'), 'c0025': (26, 'B'),
    # 'c0078': (18, 'F'), 'c0030': (26, 'C'), 'c0031': (22, 'B'), 'c0032': (20, 'E'), 'c0033': (2, 'B'),
    # 'c0057': (18, 'S'), 'c0058': (23, 'E'), 'c0059': (21, 'F'), 'c0061': (14, 'B'), 'c0062': (15, 'G'),
    # 'c0063': (15, 'S'), 'c0064': (19, 'F'), 'c0065': (25, 'G'), 'c0066': (27, 'F'), 'c0067': (29, 'S'),
    # 'c0068': (16, 'G'), 'c0069': (4, 'G'), 'c0070': (9, 'E'), 'c0071': (17, 'F'), 'c0072': (17, 'E')}

if __name__ == "__main__":
    main()