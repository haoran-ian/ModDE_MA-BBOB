import os
import numpy as np


def generate_weight(seed):
    np.random.seed(seed)
    num_random = np.random.randint(2, 5)
    weight = np.random.uniform(size=num_random)
    weight = np.concatenate((weight, [0] * (24-num_random)))
    np.random.shuffle(weight)
    weight /= np.sum(weight)
    return weight


def generate_xopt(dim, id, seed):
    np.random.seed(seed)
    xopt_a = np.random.uniform(0.01, 0.99, size=20-dim)
    xopt_b = np.random.uniform(0. if id < 25 else 0.99,
                               0.01 if id < 25 else 1., size=dim)
    xopt = np.concatenate((xopt_a, xopt_b))
    np.random.shuffle(xopt)
    return xopt


if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")

    ndim = 20
    nprob = 50
    np.random.seed(0)
    seeds = [np.random.randint(1e8) for _ in range(ndim * nprob)]

    xopts = np.array([generate_xopt(i+1, j, seeds[j * 20 + i])
                      for i in range(ndim) for j in range(nprob)])
    np.savetxt("data/xopts.txt", np.array(xopts))

    weights = np.array([generate_weight(seeds[i]) for i in range(nprob)])
    np.savetxt("data/weights.txt", weights)

    iids = np.random.randint(100, size=(nprob, 24))
    np.savetxt("data/iids.txt", iids)
