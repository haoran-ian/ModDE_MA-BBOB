import ioh
import numpy as np


if __name__ == "__main__":
    weights = np.loadtxt("data/weights.txt")
    iids = np.loadtxt("data/iids.txt")
    ioh.problem.ManyAffine()
