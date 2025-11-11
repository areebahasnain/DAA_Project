import random 
for i in range (1,11):
    n = random.randint(120,500)
    points = [(random.randint(0,1000), random.randint(0,1000)) for _ in range(n)]

    with open(f"points{i}.txt", "w") as f:
        for x , y  in points:
            f.write(f"{x} {y}\n")

print("10 random input files generated successfully!")