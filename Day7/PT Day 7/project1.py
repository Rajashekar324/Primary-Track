import time
import math

def heavy_computation(iterations=20000000):
    print(f"Starting heavy computation with {iterations:,} iterations...")
    start_time = time.time()
    result = 0
    for i in range(1, iterations + 1):
        result += math.sqrt(i) * math.sin(i) + math.cos(i)
    
    end_time = time.time()
    print(f"Computation finished in {end_time - start_time:.4f} seconds.")
    return result

if __name__ == "__main__":
    heavy_computation()