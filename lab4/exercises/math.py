import math

# 1. Convert degrees to radians
def degrees_to_radians(degrees):
    return degrees * (math.pi / 180)

degree_input = 15
print(f"Input degree: {degree_input}")
print(f"Output radian: {degrees_to_radians(degree_input):.6f}")
print("\n")


# 2. Calculate the area of a trapezoid
def trapezoid_area(height, base1, base2):
    return 0.5 * (base1 + base2) * height

height = 5
base1 = 5
base2 = 6

print(f"Height: {height}")
print(f"Base, first value: {base1}")
print(f"Base, second value: {base2}")
print(f"Expected Output: {trapezoid_area(height, base1, base2)}")
print("\n")


# 3. Calculate the area of a regular polygon
def regular_polygon_area(n_sides, side_length):
    return (n_sides * side_length ** 2) / (4 * math.tan(math.pi / n_sides))

n_sides = 4
side_length = 25
print(f"Input number of sides: {n_sides}")
print(f"Input the length of a side: {side_length}")
print(f"The area of the polygon is: {regular_polygon_area(n_sides, side_length):.1f}")
print("\n")


# 4. Calculate the area of a parallelogram
def parallelogram_area(base, height):
    return base * height

base_length = 5
height_para = 6
print(f"Length of base: {base_length}")
print(f"Height of parallelogram: {height_para}")
print(f"Expected Output: {parallelogram_area(base_length, height_para)}")
