
import random 
import math 
def distance(p1,p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def bruteforce(points):
    min_distance = float('inf')
    for i in range (len(points)):
        for j in range(i+1, len(points)):
            min_distance = min(min_distance, distance(points[i], points[j]))
    return min_distance
    
def Closest(strip , d):
    strip.sort(key=lambda point: point[1])
    min_distance = d
    for i in range(len(strip)):
        for j in range(i+1, len(strip)):
            if(strip[j][1]-strip[i][1]) >= min_distance:
             break
            min_distance = min (min_distance, distance(strip[i], strip[j]))
    return min_distance

def closestPairRec(points):
    if len(points) <= 3:
        return bruteforce(points)
    
    mid = len(points) // 2
    midPoint = points[mid]

    dl = closestPairRec(points[:mid])
    dr = closestPairRec(points[mid:])
    d = min(dl, dr)

    strip = [p for p in points if abs(p[0]-midPoint[0]) < d]
    return min(d, Closest(strip, d))

def ClosestPair(points):
    points.sort(key=lambda point: point[0])
    return closestPairRec(points)

def read_points(filename):
    with open(filename, "r") as f:
        return [tuple(map(int, line.strip().split())) for line in f]
    
def main():
    print("Closest Pair of Points Results:\n")
    for i in range(1,11):
        filename = f"points{i}.txt"
        points = read_points(filename)
        d = ClosestPair(points)
        print(f"{filename}: Closest Distance = {d:.4f}")

if __name__ == "__main__":
    main()
