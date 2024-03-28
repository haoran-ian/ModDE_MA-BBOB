import matplotlib
import numpy as np
# import pickle
import pandas as pd
# from functools import partial
# import glob
import seaborn as sns
import matplotlib.pyplot as plt
import ioh
import os

# from scipy.stats import kendalltau, rankdata

font = {'size': 24}

plt.rc('font', **font)

# Font-requirement for GECCO
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


def load_problems():
    problems = []
    iids = np.loadtxt("data/iids_2.txt").astype(np.int32)
    weights = np.loadtxt("data/weights_2.txt")
    xopts = np.loadtxt("data/xopts_2_split.txt")
    nprob = iids.shape[0]
    for xopt_index in range(xopts.shape[0]):
        problem = ioh.problem.ManyAffine(
            xopts[xopt_index],
            weights[xopt_index % nprob],
            iids[xopt_index % nprob], 2)
        problems += [problem]
    return problems


def geo_mean(iterable):
    a = np.array(iterable)
    return a.prod()**(1.0/len(a))


def create_scatter_avg_iid(fs, points):
    names = ["0", "1_0", "1_1", "1_2", "1_3", "2_0", "2_1", "2_2", "2_3"]
    for i in range(fs.shape[0]):
        l_fs = np.clip(np.log(fs[i]), -10, 25)
        mean_flog = np.mean(l_fs, axis=1)
        # mean_flog = np.mean(np.log(fs[i]), axis=1)
        dt = pd.DataFrame(points, columns=['x0', 'x1'])
        dt['f'] = mean_flog
        plt.figure(figsize=(6, 6))
        sns.scatterplot(data=dt, x='x0', y='x1',
                        hue='f', legend=None, alpha=0.2)
        plt.axhline(5, c='k', ls=':')
        plt.axhline(-5, c='k', ls=':')
        plt.axvline(5, c='k', ls=':')
        plt.axvline(-5, c='k', ls=':')
        plt.savefig(f"results/avg/{names[i]}.png")
        plt.cla()


if __name__ == "__main__":
    exp_data = "data/avg_iid.npy"
    if not os.path.exists("results/avg/"):
        os.mkdir("results/avg/")
    if not os.path.exists(exp_data):
        n_samples = 20000
        problems = load_problems()
        print(len(problems))
        num_instance = int(len(problems)/9)
        points = np.random.uniform(size=(n_samples, 2), low=-5, high=5)
        np.save("data/avg_iid_points.npy", points)
        fs = np.zeros((9, n_samples, num_instance))
        for restriction in range(9):
            for instance in range(num_instance):
                f = problems[num_instance*restriction+instance]
                for pidx, p in enumerate(points):
                    f(p)
                    fs[restriction, pidx, instance] = f.state.current_internal.y
        np.save(exp_data, fs)
    points = np.load("data/avg_iid_points.npy")
    fs = np.load(exp_data)
    create_scatter_avg_iid(fs, points)
