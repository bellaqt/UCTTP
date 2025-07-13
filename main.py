from function import genetic_algorithm
import time

def main():
    filename = "DataSet/Early/comp01.ctt"
    #run 50 times, remain 30 items,mutation is 10%
    #generation -> population(Multiple complete curriculum) -> chromosome(A complete curriculum) -> gene(course)
    generations = 200
    population_size = 150
    mutation_rate = 0.3

    print("Running on:", filename)

    start_time = time.time()
    solution, fitness, courses = genetic_algorithm(filename, generations, population_size, mutation_rate)
    end_time = time.time()
    running_time = end_time - start_time
    print(f"\nTotal Run Time: {running_time:.2f} seconds")

    print("\nFinal Best Fitness:", fitness)
    print("Best Solution (timeslot, room) per course:")
    for idx, (course,timeslot, room) in enumerate(solution):
        print(f"{course}: Timeslot={timeslot}, Room={room}")

if __name__ == "__main__":
    main()