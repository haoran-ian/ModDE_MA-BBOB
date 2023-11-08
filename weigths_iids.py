import os
import numpy as np


def generate_array(seed):
    np.random.seed(seed)
    num_random = np.random.randint(2, 5)
    weight = [np.random.uniform() if i < num_random else 0 for i in range(24)]
    np.random.shuffle(weight)
    weight /= np.sum(weight)
    return weight


if not os.path.exists("data"):
    os.makedirs("data")

np.random.seed(0)
seeds = [np.random.randint(1e8) for _ in range(50)]
weights = np.array([generate_array(seeds[i]) for i in range(50)])
iids = np.random.randint(100, size=(50, 24))

np.savetxt("data/weights.txt", weights)
np.savetxt("data/iids.txt", iids)

for weight in weights:
    print(np.sum(weight))