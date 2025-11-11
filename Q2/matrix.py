import os
def mat(x,y):
    x, y = str(x), str(y)

    if len(x) == 1 or len(y) == 1:
        return int(x) * int(y)
    
    max_len = max(len(x), len(y))
    if len(x) < max_len:
        x = x.zfill(max_len)
    if len(y) < max_len:
        y = y.zfill(max_len)

    n = max_len
    half = n//2

    x_high, x_low = int(x[:-half] or 0), int(x[-half:])
    y_high, y_low = int(y[:-half] or 0), int(y[-half:])


    z0 = mat(x_low, y_low)
    z1 = mat(x_low + x_high, y_low+y_high)
    z2 = mat(x_high, y_high)

    return (z2 * 10 ** (2 * half)) + ((z1 - z2 - z0) * 10 ** half) + z0

def read_numbers(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        return lines[0], lines[1]
    
def main():
    for i in range(1,11):
        filename = f"multiplication_inputs/mul{i}.txt"
        num1, num2, = read_numbers(filename)
        result = mat(num1, num2)
        print(f"{filename}:")
        print(f" Number of digits: {len(num1)} x {len(num2)}")
        print(f" Result (first 30 digits): {str(result)[:30]}...\n")

if __name__ == "__main__":
    main()
    


