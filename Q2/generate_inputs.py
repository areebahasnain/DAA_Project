import random 
import os 
os.makedirs("points_inputs", exist_ok=True)

for i in range (1,11):
    n = random.randint(120,500)
    points = [(random.randint(0,1000), random.randint(0,1000)) for _ in range(n)]

    with open(f"points{i}.txt", "w") as f:
        for x , y  in points:
            f.write(f"{x} {y}\n")

print("10 random input files generated successfully!")



for i in range (1,11):
    n = random.randint(100,300)
    a = "".join(str(random.randint(0,9)) for _ in range(n))
    b = "".join(str(random.randint(0,9)) for _ in range(n))            
    
    with open(f"multiplication_inputs/mul{i}.txt", "w") as f:
        f.write(a+"\n"+b + "\n")
        print("10 random input files generated successfully!")