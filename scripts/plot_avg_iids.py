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
    xopts = np.loadtxt("data/xopts_2.txt")
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
    for i in range(3):
        mean_flog = np.mean(np.log(fs[i]), axis=1)
        dt = pd.DataFrame(points, columns=['x0', 'x1'])
        dt['f'] = mean_flog
        plt.figure(figsize=(16, 16))
        sns.scatterplot(data=dt, x='x0', y='x1', hue='f')
        plt.axhline(5, c='k', ls=':')
        plt.axhline(-5, c='k', ls=':')
        plt.axvline(5, c='k', ls=':')
        plt.axvline(-5, c='k', ls=':')
        plt.savefig(f"results/scatter_avg_iid_{i}.png")
        plt.cla()


if __name__ == "__main__":
    exp_data = "data/avg_iid.npy"
    if not os.path.exists(exp_data):
        problems = load_problems()
        num_instance = int(len(problems)/3)
        points = np.random.uniform(size=(10000, 2), low=-5, high=5)
        np.save("data/avg_iid_points.npy", points)
        fs = np.zeros((3, 10000, num_instance))
        for restriction in range(3):
            for instance in range(num_instance):
                f = problems[num_instance*restriction+instance]
                for pidx, p in enumerate(points):
                    f(p)
                    fs[restriction, pidx, instance] = f.state.current_internal.y
        np.save(exp_data, fs)
    points = np.load("data/avg_iid_points.npy")
    fs = np.load(exp_data)
    create_scatter_avg_iid(fs, points)


# for fid in range(1, 25):
#     create_scatter_avg_iid(fid, 25000)

# # n_samples = 25000
# # fid = 7

# # points = np.random.uniform(size=(n_samples,2), low=-5, high=5)
# # fs = np.zeros((n_samples, 500))
# # for iid in range(500):
# #     f = ioh.get_problem(fid, dimension=2, instance=iid)
# #     for pidx, p in enumerate(points):

# #         fs[pidx, iid] = f(p) - f.optimum.y #f.state.current_internal.y


# # np.clip(mean_flog, 0, 10)

# # mean_flog = np.mean(np.log(fs), axis=1)
# # dt = pd.DataFrame(points, columns=['x0', 'x1'])
# # dt['f'] = np.clip(mean_flog, 0, 10)

# # plt.figure(figsize=(16,16))
# # sns.scatterplot(data = dt, x='x0', y='x1', hue='f')
# # plt.axhline(5, c='k', ls=':')
# # plt.axhline(-5, c='k', ls=':')
# # plt.axvline(5, c='k', ls=':')
# # plt.axvline(-5, c='k', ls=':')

# # plt.tight_layout()
# # plt.savefig(f"figs/F{fid}_scatter_avg.png")

# # f = ioh.get_problem(1, 0, 2)

# # f.optimum

# # f([0,0])

# # f([-0.6727999999999996, -3.2648])

# # f.state.current_best_internal

# # f.state.current_best_internal.y

# # xs = []
# # for iid in range(500):
# #     f = ioh.get_problem(4, iid, 5)
# #     x = f.optimum.x
# #     xs.append(x)
# #     f(x)
# #     if f.state.current_best_internal.y != 0:
# #         print(iid)

# # xs = []
# # for fid in range(1,25):
# #     f = ioh.get_problem(fid, 9, 2)
# #     x = f.optimum.x
# #     f(x)
# #     xs.append(f.state.current_best_internal.x)
# #     print(fid, f.state.current_best_internal)
# #     # if f.state.current_best_internal.y != 0:
# #     #     print(fid)

# # f = ioh.get_problem(20, 0, 2)

# # f.optimum

# # plt.figure(figsize=(16,9))
# # plt.scatter(np.array(xs)[:,4], np.array(xs)[:,2])
# # plt.xlim(-5,5)
# # plt.ylim(-5,5)

# # xs = []
# # for iid in range(500):
# #     f = ioh.get_problem(5, iid, 2)
# #     x = f.optimum.x
# #     xs.append(x)
# #     f(x)
# #     if f.state.current_best_internal.y != 0:
# #         print(iid)

# # pd.DataFrame(xs).value_counts()

# # x_try = np.array([[0,-5],[0,5], [-5,0], [5,0]])

# # f_vals = np.zeros((4,500))
# # for iid in range(500):
# #     f = ioh.get_problem(5, iid, 2)
# #     for pidx, p in enumerate(x_try):
# #         f(p)
# #         f_vals[pidx, iid] = f.state.current_internal.y
# #     # xtemp = [f(x) for x in x_try]
# #     # f_vals[:, iid] = xtemp
# #     # xs.append(x)
# #     # f(x)
# #     # if f.state.current_best_internal.y != 0:
# #     #     print(iid)

# # np.mean(np.log(f_vals), axis=1)

# # f_vals

# # np.max(f_vals[0,:])

# # a = np.log(f_vals[1,:])

# # f_vals

# # np.mean(a)

# # a.prod()**(1.0/len(a))

# # def geo_mean(iterable):
# #     a = np.array(iterable)
# #     return a.prod()**(1.0/len(a))

# # n_samples = 10000
# # fid = 5
# # iid = 1
# # points = np.random.uniform(size=(n_samples,2), low=-5, high=5)
# # fs = np.zeros((n_samples, 1))
# # # for iid_idx in [0]:
# # f = ioh.get_problem(fid, dimension=2, instance=iid)
# # for pidx, p in enumerate(points):
# #     f(p)
# #     fs[pidx, 0] = f.state.current_internal.y
# # mean_flog = np.mean(np.log(fs), axis=1)
# # dt = pd.DataFrame(points, columns=['x0', 'x1'])
# # dt['f'] = mean_flog

# # plt.figure(figsize=(16,16))
# # sns.scatterplot(data = dt, x='x0', y='x1', hue='f')
# # plt.axhline(5, c='k', ls=':')
# # plt.axhline(-5, c='k', ls=':')
# # plt.axvline(5, c='k', ls=':')
# # plt.axvline(-5, c='k', ls=':')

# # plt.tight_layout()
# # # plt.savefig(f"figs/F{fid}_scatter_avg.png")

# # n_samples = 20000
# # points = np.random.uniform(size=(n_samples,2), low=-5, high=5)
# # fig, axs = plt.subplots(nrows = 6, ncols= 4, figsize=(19,34), sharex=True, sharey=True)
# # for fidx, ax in enumerate(axs.flat):
# #     f = ioh.get_problem(fidx+1, dimension=2, instance=0)
# #     fs = np.zeros((n_samples, 500))
# #     for iid in range(500):
# #         f = ioh.get_problem(fidx+1, dimension=2, instance=iid)
# #         for pidx, p in enumerate(points):
# #             f(p)
# #             fs[pidx, iid] = f.state.current_internal.y
# #         mean_flog = np.mean(np.log(fs), axis=1)
# #     # for pidx, p in enumerate(points):
# #     #     f(p)
# #     #     fs[pidx, 0] = f.state.current_internal.y
# #     mean_flog = np.mean(np.log(fs), axis=1)
# #     dt = pd.DataFrame(points, columns=['x0', 'x1'])
# #     dt['f'] = mean_flog

# #     # plt.figure(figsize=(16,16))
# #     ax.scatter(data = dt, x='x0', y='x1', c='f', alpha=0.1)
# #     ax.axhline(5, c='k', ls=':')
# #     ax.axhline(-5, c='k', ls=':')
# #     ax.axvline(5, c='k', ls=':')
# #     ax.axvline(-5, c='k', ls=':')
# # # plt.subplots_adjust(left=0.01,right=0.01,up=0.01,down=0.01)
# # plt.tight_layout()
# # plt.savefig(f"figs/Overall_scatter_avg.png")

# #     points = np.random.uniform(size=(n_samples,2), low=-5, high=5)
# #     fs = np.zeros((n_samples, 500))
# #     for iid in range(500):
# #         f = ioh.get_problem(fid, dimension=2, instance=iid)
# #         for pidx, p in enumerate(points):
# #             f(p)
# #             fs[pidx, iid] = f.state.current_internal.y
# #         mean_flog = np.mean(np.log(fs), axis=1)
# #     dt = pd.DataFrame(points, columns=['x0', 'x1'])
# #     dt['f'] = mean_flog

# #     plt.figure(figsize=(16,16))
# #     sns.scatterplot(data = dt, x='x0', y='x1', hue='f')
# #     plt.axhline(5, c='k', ls=':')
# #     plt.axhline(-5, c='k', ls=':')
# #     plt.axvline(5, c='k', ls=':')
# #     plt.axvline(-5, c='k', ls=':')

# #     plt.tight_layout()
# #     plt.savefig(f"figs/F{fid}_scatter_avg.png")

# # n_samples = 25000

# # points = np.random.uniform(size=(n_samples,2), low=-5, high=5)

# # for fid in range(1,25):
# #     fs = np.zeros((n_samples, 500))
# #     for iid in range(500):
# #         f = ioh.get_problem(fid, dimension=2, instance=iid)
# #         for pidx, p in enumerate(points):

# #             fs[pidx, iid] = f(p) - f.optimum.y #f.state.current_internal.y
# #     np.save(f"data/F{fid}_full.npy", fs)

# # for fid in range(1,25):
# #     fs = np.load(f"data/F{fid}_full.npy")
# #     l_fs = np.clip(np.log(fs), -10, 25)
# #     mean_flog = np.mean(l_fs, axis=1)
# #     dt = pd.DataFrame(points, columns=['x0', 'x1'])
# #     dt['f'] = mean_flog
# #     dt.to_csv(f"data/F{fid}_dt.csv")

# # ?np.save

# # fig, axs = plt.subplots(nrows = 6, ncols= 4, figsize=(19,34), sharex=True, sharey=True)
# # for fidx, ax in enumerate(axs.flat):
# #     f = ioh.get_problem(fidx+1, dimension=2, instance=0)

# #     dt = pd.read_csv(f"data/F{fidx+1}_dt.csv")

# #     # plt.figure(figsize=(16,16))
# #     # ax.scatter(data = dt, x='x0', y='x1', c='f', alpha=0.1)
# #     sns.scatterplot(data = dt, x='x0', y='x1', hue='f', ax=ax, legend=None, alpha=0.2)
# #     ax.axhline(5, c='k', ls=':')
# #     ax.axhline(-5, c='k', ls=':')
# #     ax.axvline(5, c='k', ls=':')
# #     ax.axvline(-5, c='k', ls=':')
# # # plt.subplots_adjust(left=0.01,right=0.01,up=0.01,down=0.01)
# # plt.tight_layout()
# # plt.savefig(f"figs/Overall_scatter_avg_v3.png")
