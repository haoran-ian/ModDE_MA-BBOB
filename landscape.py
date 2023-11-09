import ioh
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange


def landscape(problem):
    x = np.arange(-5, 5.1, 0.025)
    x1, x2 = np.meshgrid(x, x)
    solutions = np.column_stack((x1.ravel(), x2.ravel()))
    results = np.array(problem(solutions)).reshape((x.shape[0], x.shape[0]))
    return results


if __name__ == "__main__":
    xopts = np.loadtxt("data/xopts_2.txt")
    weights = np.loadtxt("data/weights.txt")
    iids = np.loadtxt("data/iids.txt").astype(np.int32)

    ndim = xopts.shape[1]
    nprob = weights.shape[0]

    problems = [ioh.problem.ManyAffine(
        xopts[i*nprob+j], weights[j], iids[j], ndim)
        for i in range(ndim) for j in range(nprob)]

    fig, axs = plt.subplots(10, 10, figsize=(20, 20))
    print("Generating 2D landscape figures.")
    for index in trange(ndim*nprob):
        i = int(index/nprob)
        j = index % nprob
        results = landscape(problems[index])
        min_index = np.unravel_index(np.argmin(results), results.shape)
        axs[int(index/10), index % 10].imshow(results, interpolation='nearest')
        axs[int(index/10), index % 10].scatter(min_index[1], min_index[0],
                                               s=100, marker='x', linewidths=3,
                                               color='red')
        axs[int(index/10), index % 10].axis("off")
    plt.tight_layout()
    plt.savefig("results/landscape_2D.png")
