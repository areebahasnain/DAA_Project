import math
import os
import time

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


def run_all_closest_pair_tests():
    print("\n" + "="*70)
    print("CLOSEST PAIR OF POINTS - TESTING ALL DATASETS")
    print("="*70)
    
    folder = 'datasets/closest_pair'
    files = sorted([f for f in os.listdir(folder) if f.endswith('.txt')])
    
    results = []
    
    for filename in files:
        filepath = os.path.join(folder, filename)
        print(f"\nTesting: {filename}")
        
        points = load_closest_pair_from_file(filepath)
        num_points = len(points)
        
        start = time.time()
        min_dist, pair = closest_pair(points)
        end = time.time()
        
        exec_time = (end - start) * 1000
        
        print(f"  Points: {num_points}")
        print(f"  Min Distance: {min_dist:.6f}")
        print(f"  Closest Pair: {pair[0]} <-> {pair[1]}")
        print(f"  Time: {exec_time:.2f} ms")
        
        results.append({
            'file': filename,
            'points': num_points,
            'distance': min_dist,
            'time': exec_time
        })
    
    print("\n" + "="*70)
    print("SUMMARY - CLOSEST PAIR")
    print("="*70)
    print(f"{'File':<35} {'Points':<10} {'Distance':<15} {'Time (ms)':<10}")
    print("-"*70)
    for r in results:
        print(f"{r['file']:<35} {r['points']:<10} {r['distance']:<15.6f} {r['time']:<10.2f}")
    
    return results


def run_all_multiplication_tests():
    print("\n" + "="*70)
    print("KARATSUBA MULTIPLICATION - TESTING ALL DATASETS")
    print("="*70)
    
    folder = 'datasets/multiplication'
    files = sorted([f for f in os.listdir(folder) if f.endswith('.txt')])
    
    results = []
    
    for filename in files:
        filepath = os.path.join(folder, filename)
        print(f"\nTesting: {filename}")
        
        num1, num2 = load_multiplication_from_file(filepath)
        digits1 = len(str(num1))
        digits2 = len(str(num2))
        
        start = time.time()
        result = karatsuba_multiply(num1, num2)
        end = time.time()
        
        exec_time = (end - start) * 1000
        
        expected = num1 * num2
        verified = result == expected
        
        print(f"  Num1 Digits: {digits1}")
        print(f"  Num2 Digits: {digits2}")
        print(f"  Result Digits: {len(str(result))}")
        print(f"  Verified: {verified}")
        print(f"  Time: {exec_time:.2f} ms")
        
        results.append({
            'file': filename,
            'digits1': digits1,
            'digits2': digits2,
            'result_digits': len(str(result)),
            'verified': verified,
            'time': exec_time
        })
    
    print("\n" + "="*70)
    print("SUMMARY - KARATSUBA MULTIPLICATION")
    print("="*70)
    print(f"{'File':<35} {'Digits':<10} {'Result':<10} {'Verified':<10} {'Time (ms)':<10}")
    print("-"*70)
    for r in results:
        print(f"{r['file']:<35} {r['digits1']},{r['digits2']:<8} {r['result_digits']:<10} {str(r['verified']):<10} {r['time']:<10.2f}")
    
    return results


if __name__ == "__main__":
    print("\n" + "="*70)
    print("APPLYING ALGORITHMS ON ALL INPUT DATASETS")
    print("="*70)
    
    cp_results = run_all_closest_pair_tests()
    
    mult_results = run_all_multiplication_tests()
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED")
    print("="*70)
    print(f"\nTotal Closest Pair tests: {len(cp_results)}")
    print(f"Total Multiplication tests: {len(mult_results)}")
    
    avg_cp_time = sum(r['time'] for r in cp_results) / len(cp_results)
    avg_mult_time = sum(r['time'] for r in mult_results) / len(mult_results)
    
    print(f"\nAverage Closest Pair time: {avg_cp_time:.2f} ms")
    print(f"Average Multiplication time: {avg_mult_time:.2f} ms")
    
    print("\n" + "="*70)
