import pandas as pd
import time

df = pd.DataFrame([{f"col_{i}": f"val_{i}" for i in range(15)} for _ in range(50000)])

start = time.time()
for index, row in df.iterrows():
    clean_row = {}
    for k, v in row.to_dict().items():
        pass
print(f"Elapsed: {time.time() - start:.2f}s")
