import os
import numpy as np


def generate_weight(seed):
    # set random seed
    np.random.seed(seed)
    # get the number of non-zero weight value
    num_nonzero = np.random.randint(2, 5)
    # generate weight in lenght of num_nonzero
    weight = np.random.uniform(size=num_nonzero)
    # expand weight to full length of 24
    weight = np.concatenate((weight, [0] * (24-num_nonzero)))
    # random distribute non-zero weight values
    np.random.shuffle(weight)
    # normalization
    weight /= np.sum(weight)
    return weight


def generate_xopt(dim, ndim, seed):
    # set random seed
    np.random.seed(seed)
    # generate optima values that not near the boundaries
    xopt_a = np.random.uniform(-4.99, 4.99, size=ndim-dim)
    # generate optima values that near the boundaries
    xopt_b = np.random.uniform(-0.01, 0.01, size=dim)
    # adjust xopt_b to the real boundaries
    xopt_b = np.array([x_b-5. if x_b >= 0 else x_b+5. for x_b in xopt_b])
    # merge both type of values
    xopt = np.concatenate((xopt_a, xopt_b))
    # random distribute the optima values
    np.random.shuffle(xopt)
    return xopt


if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    # problems are 20-dimensional, 50 set of problems' weights
    ndim = 2
    nprob = 500
    # set random seed
    np.random.seed(0)
    # generate seeds for each problem
    seeds = [np.random.randint(1e8) for _ in range((ndim+1) * nprob)]
    # generate optima with near boundraies values
    xopts = np.array([generate_xopt(i, ndim, seeds[j * ndim + i])
                      for i in range(ndim+1) for j in range(nprob)])
    np.savetxt(f"data/xopts_{ndim}.txt", np.array(xopts))
    # generate 50 sets of weights
    weights = np.array([generate_weight(seeds[i]) for i in range(nprob)])
    np.savetxt(f"data/weights_{ndim}.txt", weights)
    # generate instance number
    iids = np.random.randint(100, size=(nprob, 24))
    np.savetxt(f"data/iids_{ndim}.txt", iids)
