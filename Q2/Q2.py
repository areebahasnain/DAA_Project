import math
import random
import os

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def brute_force_closest(points):
    min_dist = float('inf')
    pair = None
    n = len(points)
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                pair = (points[i], points[j])
    
    return min_dist, pair

def strip_closest(strip, d):
    min_dist = d
    pair = None
    strip.sort(key=lambda p: p.y)
    
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j].y - strip[i].y) < min_dist:
            dist = distance(strip[i], strip[j])
            if dist < min_dist:
                min_dist = dist
                pair = (strip[i], strip[j])
            j += 1
    
    return min_dist, pair

def closest_pair_recursive(points_x, points_y):
    n = len(points_x)
    
    if n <= 3:
        return brute_force_closest(points_x)
    
    mid = n // 2
    mid_point = points_x[mid]
    
    points_y_left = [p for p in points_y if p.x <= mid_point.x]
    points_y_right = [p for p in points_y if p.x > mid_point.x]
    
    left_dist, left_pair = closest_pair_recursive(points_x[:mid], points_y_left)
    right_dist, right_pair = closest_pair_recursive(points_x[mid:], points_y_right)
    
    if left_dist < right_dist:
        min_dist = left_dist
        min_pair = left_pair
    else:
        min_dist = right_dist
        min_pair = right_pair
    
    strip = [p for p in points_y if abs(p.x - mid_point.x) < min_dist]
    
    if strip:
        strip_dist, strip_pair = strip_closest(strip, min_dist)
        if strip_dist < min_dist:
            min_dist = strip_dist
            min_pair = strip_pair
    
    return min_dist, min_pair

def closest_pair(points):
    points_x = sorted(points, key=lambda p: p.x)
    points_y = sorted(points, key=lambda p: p.y)
    return closest_pair_recursive(points_x, points_y)


def karatsuba_multiply(x, y):
    if x < 10 or y < 10:
        return x * y
    
    n = max(len(str(x)), len(str(y)))
    half = n // 2
    power = 10 ** half
    
    high1 = x // power
    low1 = x % power
    high2 = y // power
    low2 = y % power
    
    z0 = karatsuba_multiply(low1, low2)
    z1 = karatsuba_multiply(low1 + high1, low2 + high2)
    z2 = karatsuba_multiply(high1, high2)
    
    return z2 * (10 ** (2 * half)) + (z1 - z2 - z0) * power + z0


def generate_closest_pair_data(n, max_coord=10000.0):
    points = []
    for i in range(n):
        x = random.uniform(0, max_coord)
        y = random.uniform(0, max_coord)
        points.append(Point(x, y))
    return points

def generate_multiplication_data(digits):
    num1 = random.randint(10**(digits-1), 10**digits - 1)
    num2 = random.randint(10**(digits-1), 10**digits - 1)
    return num1, num2

def save_closest_pair_to_file(filename, points):
    with open(filename, 'w') as f:
        for point in points:
            f.write(f"{point.x},{point.y}\n")

def save_multiplication_to_file(filename, num1, num2):
    with open(filename, 'w') as f:
        f.write(f"{num1}\n{num2}\n")

def load_closest_pair_from_file(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            x, y = map(float, line.strip().split(','))
            points.append(Point(x, y))
    return points

def load_multiplication_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        num1 = int(lines[0].strip())
        num2 = int(lines[1].strip())
    return num1, num2


def generate_all_datasets():
    os.makedirs('datasets/closest_pair', exist_ok=True)
    os.makedirs('datasets/multiplication', exist_ok=True)
    
    print("generating datasets...")
    
    closest_pair_sizes = [100, 150, 200, 300, 500, 750, 1000, 1500, 2000, 3000]
    
    for i, size in enumerate(closest_pair_sizes, 1):
        points = generate_closest_pair_data(size)
        filename = f'datasets/closest_pair/input_{i:02d}_size{size}.txt'
        save_closest_pair_to_file(filename, points)
        print(f"created: {filename}")
    
    multiplication_sizes = [100, 150, 200, 300, 400, 500, 750, 1000, 1500, 2000]
    
    for i, size in enumerate(multiplication_sizes, 1):
        num1, num2 = generate_multiplication_data(size)
        filename = f'datasets/multiplication/input_{i:02d}_digits{size}.txt'
        save_multiplication_to_file(filename, num1, num2)
        print(f"created: {filename}")
    
    print("\ndone!")

def test_closest_pair(filename):
    print(f"\n{'='*60}")
    print(f"Testing Closest Pair")
    print(f"File: {filename}")
    print(f"{'='*60}")
    
    points = load_closest_pair_from_file(filename)
    print(f"points: {len(points)}")
    
    min_dist, pair = closest_pair(points)
    
    print(f"\nResult:")
    print(f"min distance: {min_dist:.6f}")
    print(f"pair: {pair[0]} and {pair[1]}")

def test_multiplication(filename):
    print(f"\n{'='*60}")
    print(f"Testing Karatsuba Multiplication")
    print(f"File: {filename}")
    print(f"{'='*60}")
    
    num1, num2 = load_multiplication_from_file(filename)
    print(f"num1 digits: {len(str(num1))}")
    print(f"num2 digits: {len(str(num2))}")
    print(f"num1: {str(num1)[:50]}..." if len(str(num1)) > 50 else f"num1: {num1}")
    print(f"num2: {str(num2)[:50]}..." if len(str(num2)) > 50 else f"num2: {num2}")
    
    result = karatsuba_multiply(num1, num2)
    
    print(f"\nResult:")
    result_str = str(result)
    if len(result_str) > 100:
        print(f"{result_str[:50]}...{result_str[-50:]}")
        print(f"total digits: {len(result_str)}")
    else:
        print(result)
    
    expected = num1 * num2
    print(f"\nverification: {'PASS' if result == expected else 'FAIL'}")

if __name__ == "__main__":
    print("Divide and Conquer Algorithms")
    print("=" * 60)
    
    print("\ngenerating datasets...")
    generate_all_datasets()
    
    print("\ntesting algorithms...")
    
    test_closest_pair('datasets/closest_pair/input_01_size100.txt')
    test_closest_pair('datasets/closest_pair/input_05_size500.txt')
    
    test_multiplication('datasets/multiplication/input_01_digits100.txt')
    test_multiplication('datasets/multiplication/input_05_digits400.txt')
    
    print("\n" + "="*60)
    print("done!")
    print("="*60)
