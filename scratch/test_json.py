import json
import time

data = [{f"col_{i}": f"val_{i}" for i in range(15)} for _ in range(50000)]
start = time.time()
j = json.dumps(data)
print(f"Elapsed JSON: {time.time() - start:.2f}s, length: {len(j)}")
