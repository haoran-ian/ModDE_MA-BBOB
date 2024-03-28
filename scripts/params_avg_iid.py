import numpy as np


if __name__ == "__main__":
    xopts = np.zeros((500*9, 2))
    for i in range(500):
        xopts[i][0] = np.random.uniform(-4.9, 4.9)
        xopts[i][1] = np.random.uniform(-4.9, 4.9)
        xopts[500+i][0] = np.random.uniform(-5, -4.9)
        xopts[500+i][1] = np.random.uniform(-4.9, 4.9)
        xopts[1000+i][0] = np.random.uniform(4.9, 5)
        xopts[1000+i][1] = np.random.uniform(-4.9, 4.9)
        xopts[1500+i][0] = np.random.uniform(-4.9, 4.9)
        xopts[1500+i][1] = np.random.uniform(-5, -4.9)
        xopts[2000+i][0] = np.random.uniform(-4.9, 4.9)
        xopts[2000+i][1] = np.random.uniform(4.9, 5)
        xopts[2500+i][0] = np.random.uniform(-5, -4.9)
        xopts[2500+i][1] = np.random.uniform(-5, -4.9)
        xopts[3000+i][0] = np.random.uniform(4.9, 5)
        xopts[3000+i][1] = np.random.uniform(4.9, 5)
        xopts[3500+i][0] = np.random.uniform(4.9, 5)
        xopts[3500+i][1] = np.random.uniform(-5, -4.9)
        xopts[4000+i][0] = np.random.uniform(-5, -4.9)
        xopts[4000+i][1] = np.random.uniform(4.9, 5)
    np.savetxt("data/xopts_2_split.txt", xopts)
