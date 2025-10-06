import random

def parse_ctt(file_path):
    """Parse comp02.ctt and extract sections."""
    with open(file_path, "r") as f:
        lines = f.readlines()

    return lines


def generate_courses(num_courses):
    courses = []
    num_teachers = max(1, num_courses // 2)
    for i in range(num_courses):
        course_id = f"c{i:04d}"
        teacher_id = f"t{random.randint(0, num_teachers-1):03d}"
        lectures = random.randint(2, 5)
        length = random.randint(1, 3)
        students = random.randint(20, 300)
        courses.append(f"{course_id} {teacher_id} {lectures} {length} {students}")
    return courses


def generate_rooms(num_rooms):
    rooms = []
    for i in range(num_rooms):
        room_id = f"R{i}"
        capacity = random.randint(40, 400)
        rooms.append(f"{room_id} {capacity}")
    return rooms


def scale_dataset(base_file, scale, out_file):
    lines = parse_ctt(base_file)

    # Extract metadata
    courses = rooms = days = periods = curricula = constraints = 0
    for line in lines:
        line = line.strip()
        if line.startswith("Courses:"):
            courses = int(line.split()[1])
        elif line.startswith("Rooms:"):
            rooms = int(line.split()[1])
        elif line.startswith("Days:"):
            days = int(line.split()[1])
        elif line.startswith("Periods_per_day:"):
            periods = int(line.split()[1])
        elif line.startswith("Curricula:"):
            curricula = int(line.split()[1])
        elif line.startswith("Constraints:"):
            constraints = int(line.split()[1])

    new_courses = courses * scale
    new_rooms = rooms * scale
    new_constraints = constraints * scale

    with open(out_file, "w") as f:
        # Header
        f.write(f"Courses: {new_courses}\n")
        f.write(f"Rooms: {new_rooms}\n")
        f.write(f"Days: {days}\n")
        f.write(f"Periods_per_day: {periods}\n")
        f.write(f"Curricula: {curricula}\n")
        f.write(f"Constraints: {new_constraints}\n\n")

        # Courses section
        f.write("COURSES:\n")
        courses_list = generate_courses(new_courses)
        for c in courses_list:
            f.write(c + "\n")
        f.write("\n")

        # Rooms section
        f.write("ROOMS:\n")
        rooms_list = generate_rooms(new_rooms)
        for r in rooms_list:
            f.write(r + "\n")
        f.write("\n")

        # Unavailability constraints
        f.write("UNAVAILABILITY_CONSTRAINTS:\n")
        constraints_set = set()

        while len(constraints_set) < min(new_constraints, new_courses * days * periods):
            course = f"c{random.randint(0, new_courses-1):04d}"
            day = random.randint(0, days-1)
            period = random.randint(0, periods-1)
            constraints_set.add(f"{course} {day} {period}")

        constraints_list = list(constraints_set)

        for c in constraints_list:
            f.write(c + "\n")
        print(f"Generated {len(constraints_list)} unique constraints")
        # End
        f.write("END.\n")

scale_dataset(r"DataSet\Hidden\comp16.ctt",
              scale=3,
              out_file=r"DataSet\Scalability\comp16_3.ctt")
print('Scale Done')
